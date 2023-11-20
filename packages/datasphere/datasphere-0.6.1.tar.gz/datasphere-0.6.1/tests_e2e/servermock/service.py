from dataclasses import dataclass, field
from datetime import datetime
import os
import uuid
from random import shuffle
import subprocess
import tempfile
from threading import Thread, Event
from typing import List, Dict, Optional, Union, Iterable
import zipfile

import grpc

from google.protobuf.timestamp_pb2 import Timestamp
from google.rpc.status_pb2 import Status
from yandex.cloud.operation.operation_pb2 import Operation
from yandex.cloud.datasphere.v2.jobs.jobs_pb2 import FileDesc, JobParameters, Job, JobStatus, StorageFile, JobResult
from yandex.cloud.datasphere.v2.jobs.project_job_service_pb2 import (
    CreateProjectJobRequest, CreateProjectJobResponse,
    ExecuteProjectJobRequest, ExecuteProjectJobResponse, ExecuteProjectJobMetadata,
    ReadProjectJobStdLogsRequest, ReadProjectJobStdLogsResponse, StdLog,
    ListProjectJobRequest, ListProjectJobResponse,
    GetProjectJobRequest, CancelProjectJobRequest,
)
from yandex.cloud.datasphere.v2.jobs.project_job_service_pb2_grpc import ProjectJobServiceServicer
from yandex.cloud.operation.operation_service_pb2 import GetOperationRequest
from yandex.cloud.operation.operation_service_pb2_grpc import OperationServiceServicer

from datasphere.config import var_tpl_pattern

from storage import S3Client


class FileHolder:
    var_to_path: Dict[str, str]

    def __init__(self):
        self.var_to_path = {}

    def register_file(self, desc: FileDesc) -> str:
        if desc.var:
            path = str(uuid.uuid4())
            self.var_to_path[desc.var] = path
            return path
        elif desc.path:
            return desc.path
        else:
            raise ValueError(f'file desc has no var or path: {desc}')

    def get_path(self, desc: FileDesc) -> str:
        if desc.var:
            return self.var_to_path[desc.var]
        elif desc.path:
            return desc.path
        else:
            raise ValueError(f'file desc has no var or path: {desc}')

    def get_var_path(self, var: str) -> str:
        assert var in self.var_to_path, f'var {var} is not found in config'
        return self.var_to_path[var]


@dataclass
class JobData:
    @dataclass
    class Execution:
        op_id: Optional[str]
        thread: Thread
        cancel_event: Event

    params: JobParameters
    config: str
    name: str
    desc: str

    job_id: str
    created_at: datetime

    finished_at: Optional[datetime] = None
    status: JobStatus = JobStatus.CREATING

    execution: Optional[Execution] = None

    result: Optional[Union[ExecuteProjectJobResponse, Status]] = None
    std_logs: List[StdLog] = field(default_factory=list)

    @staticmethod
    def find_by_job_id(job_id: str) -> 'JobData':
        return next(j for j in jobs if j.job_id == job_id)

    @staticmethod
    def find_by_op_id(op_id: str) -> 'JobData':
        return next(j for j in jobs if j.execution.op_id == op_id)

    @property
    def job(self) -> Job:
        def get_ts(dt: Optional[datetime]) -> Optional[Timestamp]:
            if dt is None:
                return None
            ts = Timestamp()
            ts.FromDatetime(dt)
            return ts

        return Job(
            id=self.job_id,
            name=self.name,
            desc=self.desc,
            created_at=get_ts(self.created_at),
            finished_at=get_ts(self.finished_at),
            status=self.status,
            config=self.config,
            created_by_id='user',
        )


jobs: List[JobData] = []


class Service(ProjectJobServiceServicer):
    s3_client: S3Client
    conda_home: str

    def __init__(self, s3_client: S3Client, conda_home: str):
        self.s3_client = s3_client
        self.conda_home = conda_home

    def Create(self, request: CreateProjectJobRequest, context) -> Operation:
        params = request.job_parameters
        files = list(params.input_files)

        python_env = params.env.python_env
        if python_env:
            files += python_env.local_modules

        shuffle(files)  # to test client doesn't rely on any files order

        job_id = str(uuid.uuid4())
        jobs.append(JobData(
            params=params,
            config=request.config,
            name=request.name,
            desc=request.desc,
            job_id=job_id,
            created_at=datetime.now(),
        ))

        upload_files = []
        for f in files:
            url = self.s3_client.generate_presigned_post(f.sha256)
            if url:
                upload_files.append(StorageFile(file=f, url=url))

        op = Operation(id=str(uuid.uuid4()), done=True)  # TODO: simulate not instantaneous done=True
        op.response.Pack(CreateProjectJobResponse(job_id=job_id, upload_files=upload_files))
        return op

    def Execute(self, request: ExecuteProjectJobRequest, context) -> Operation:
        job_data = JobData.find_by_job_id(request.job_id)

        op_id = str(uuid.uuid4())
        thread = Thread(target=self._execute, args=[op_id])

        job_data.execution = JobData.Execution(
            op_id=op_id,
            thread=thread,
            cancel_event=Event(),
        )

        thread.start()

        return Operation(id=op_id)

    def _execute(self, op_id: str):
        job_data = JobData.find_by_op_id(op_id)
        conda_env_name = None
        try:
            with tempfile.TemporaryDirectory('_executor') as tmpdir:
                print(f'executor working directory: {tmpdir}')
                os.chdir(tmpdir)

                file_holder = FileHolder()

                job_params = job_data.params

                conda_env_name = self._install_env(job_params, tmpdir, file_holder)

                for f in job_params.output_files:
                    file_holder.register_file(f)

                cmd = self._prepare_cmd(job_params.cmd, file_holder, conda_env_name)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                while True:
                    if job_data.execution.cancel_event.is_set():
                        print('operation was canceled by user, killing process')
                        process.kill()
                        print('process killed')
                        job_data.result = Status(code=grpc.StatusCode.CANCELLED.value[0], message='Canceled by user')
                        return

                    try:
                        process.wait(timeout=1)
                    except subprocess.TimeoutExpired:
                        print('process is still running...')
                        self._capture_logs(job_data, process)
                        continue

                    files = []
                    for f in job_params.output_files:
                        path = file_holder.get_path(f)
                        try:
                            with open(path, 'rb') as fd:
                                files.append(self.s3_client.upload_file(f, fd))
                        except FileNotFoundError:
                            print(f'output file {path} was not generated')

                    shuffle(files)  # to test client doesn't rely on any files order

                    job_data.finished_at = datetime.now()
                    job_data.status = JobStatus.SUCCESS
                    job_data.result = ExecuteProjectJobResponse(
                        output_files=files,
                        result=JobResult(return_code=process.returncode)
                    )
                    return
        except Exception:
            job_data.result = Status(code=grpc.StatusCode.INTERNAL.value[0], message='Unexpected error')
            raise
        finally:
            if conda_env_name:
                self._remove_env(conda_env_name)

    # Download input files, in case of python also activate python environment with conda and return its name.
    def _install_env(self, job_params: JobParameters, tmpdir: str, file_holder: FileHolder) -> Optional[str]:
        conda_env_name = None
        download_files = list(job_params.input_files)

        if job_params.env.HasField('python_env'):
            download_files += list(job_params.env.python_env.local_modules)

            conda_yaml = job_params.env.python_env.conda_yaml
            print(f'conda yaml:\n{conda_yaml}')

            conda_yaml_f = f'{tmpdir}/conda.yaml'
            with open(conda_yaml_f, 'w') as f:
                f.write(conda_yaml)

            conda_env_name = f'datasphere_{str(uuid.uuid4())}'
            try:
                # TODO: should we capture conda std logs for CLI?
                # TODO: make it cancelable (Popen and listen to cancel_event)
                subprocess.run(['conda', 'env', 'create', '-n', conda_env_name, '--file', conda_yaml_f])
            except FileNotFoundError:
                raise RuntimeError('you need conda to install python environment')

        for i, f in enumerate(download_files):
            path = file_holder.register_file(f.desc)
            self.s3_client.download_file(f, path)

            # local modules are zipped
            if i >= len(job_params.input_files):
                with zipfile.ZipFile(path) as ar:
                    ar.extractall('.')

        return conda_env_name

    @staticmethod
    def _remove_env(conda_env_name: str):
        subprocess.run(['conda', 'env', 'remove', '-n', conda_env_name])

    def _prepare_cmd(self, cmd: str, file_holder: FileHolder, conda_env_name: Optional[str]) -> str:
        old_cmd = cmd
        for var in var_tpl_pattern.findall(cmd):
            path = file_holder.get_var_path(var)
            cmd = cmd.replace('${%s}' % var, path)

        if conda_env_name:
            # TODO: use `conda activate` instead
            conda_python_path = f'{self.conda_home}/envs/{conda_env_name}/bin/python'
            cmd = cmd.replace('python', conda_python_path)

        print(f'cmd vars substitution\nbefore: {old_cmd}\nafter: {cmd}')

        return cmd

    @staticmethod
    def _capture_logs(job_data: JobData, process):
        def read(stream, is_stdout: bool):
            if stream is None:
                return
            t = StdLog.Type.OUT if is_stdout else StdLog.Type.ERR
            for line in iter(stream.readline, b''):
                log = StdLog(content=line[:-1], type=t)  # trim newline
                job_data.std_logs.append(log)

        # TODO: write std logs in order of their appearance
        read(process.stderr, is_stdout=False)
        read(process.stdout, is_stdout=True)

    def ReadStdLogs(self, request: ReadProjectJobStdLogsRequest, context) -> Iterable[ReadProjectJobStdLogsResponse]:
        job_data = JobData.find_by_job_id(request.job_id)

        for i, line in enumerate(job_data.std_logs[request.offset:]):
            # TODO: buffer multiple lines
            yield ReadProjectJobStdLogsResponse(logs=[line], offset=i + request.offset + 1)

    def List(self, request: ListProjectJobRequest, context) -> ListProjectJobResponse:
        # We ignore page_size from request and set it to 1, to simplify paging tests.
        job_i = 0
        if request.page_token:
            job_i = int(request.page_token)
        page_token = None
        if job_i < len(jobs) - 1:  # Concurrency is not supported.
            page_token = str(job_i + 1)
        return ListProjectJobResponse(jobs=[jobs[job_i].job], page_token=page_token)

    def Get(self, request: GetProjectJobRequest, context) -> Job:
        try:
            return JobData.find_by_job_id(request.job_id).job
        except StopIteration:
            context.abort(code=grpc.StatusCode.NOT_FOUND, details='Unknown job')  # message as in real server

    def Cancel(self, request: CancelProjectJobRequest, context) -> None:
        job_data = JobData.find_by_job_id(request.job_id)
        job_data.execution.cancel_event.set()
        job_data.execution.thread.join(timeout=60)  # conda env install is not interruptable


class OperationService(OperationServiceServicer):
    def Get(self, request: GetOperationRequest, context) -> Operation:
        op = Operation()
        op.id = request.operation_id
        job_data = JobData.find_by_op_id(op.id)
        job = Job(config=job_data.config)  # TODO: fill other fields
        op.metadata.Pack(ExecuteProjectJobMetadata(job=job))
        if job_data.result:
            op.done = True
            if isinstance(job_data.result, ExecuteProjectJobResponse):
                op.response.Pack(job_data.result)
            else:
                op.error.CopyFrom(job_data.result)
        return op
