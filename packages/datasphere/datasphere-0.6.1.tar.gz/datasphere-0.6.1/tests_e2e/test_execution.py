import os
import time
import re
from pathlib import Path
from pytest import approx, fixture, mark
import subprocess
import sys
from typing import Tuple, List

from datasphere.auth import env, ServerEnv
from datasphere.config import parse_config


@fixture(autouse=True)
def server_mock():
    if env != ServerEnv.DEV:
        yield None
        return

    server_process = subprocess.Popen([
        sys.executable,
        Path(__file__).parent / 'servermock' / 'main.py',
        '-b', os.environ['BUCKET'],
        '-c', os.environ['CONDA_HOME'],
    ])
    time.sleep(2)  # give server process some time to startup
    yield server_process
    server_process.kill()


@fixture
def scenario(request) -> Tuple[str, List[Path]]:
    name = request.node.get_closest_marker('scenario_name').args[0]
    os.chdir(f'scenarios/{name}')

    cfg_path = Path('config.yaml')
    cfg = parse_config(cfg_path)

    output_files = [Path(f.path) for f in cfg.outputs]

    yield cfg_path.absolute(), output_files

    for f in output_files:
        f.unlink(missing_ok=True)

    os.chdir('../..')


project_id = 'bt146eeguefuqa2fgfl9' if env == ServerEnv.PROD else 'b3pbocd5dua07ojecibq'


def create_exec_proc(cfg_path: str, capture_stdout: bool = False):
    kwargs = {}
    if capture_stdout:
        kwargs['stdout'] = subprocess.PIPE
    return subprocess.Popen(
        [
            'datasphere', 'project', 'job', 'execute',
            '--project-id', project_id, '-c', cfg_path,
        ],
        **kwargs,
    )


def create_list_proc():
    return subprocess.Popen(
        [
            'datasphere', 'project', 'job', 'list',
            '--project-id', project_id,
        ],
        stdout=subprocess.PIPE,
    )


def create_attach_proc(job_id: str):
    return subprocess.Popen(
        [
            'datasphere', 'project', 'job', 'attach',
            '--id', job_id,
        ],
    )


def execute(cfg_path: str, expected_return_code: int = 0):
    proc = create_exec_proc(cfg_path)
    proc.wait(timeout=600)
    assert proc.returncode == expected_return_code


job_id_log_pattern = re.compile('.*created job `(?P<job_id>.*)`.*')


def execute_with_reattach(cfg_path: str):
    exec_proc = create_exec_proc(cfg_path, capture_stdout=True)
    time.sleep(10)  # give some time to create operation for job, `simple_python` script sleeps overall for 30 seconds
    exec_proc.kill()
    exec_stdout = [line.decode('utf-8').strip() for line in exec_proc.stdout.readlines()]

    matches = [match for match in [job_id_log_pattern.match(line) for line in exec_stdout] if match is not None]
    assert len(matches) == 1
    job_id = matches[0].groupdict()['job_id']
    print(f'parsed job_id={job_id} from log file for reattach')

    # After attach we should download output files
    attach_proc = create_attach_proc(job_id)
    attach_proc.wait(timeout=600)
    assert attach_proc.returncode == 0


@mark.scenario_name('simple_python')
def test_simple_python(scenario):
    cfg_path, (result_file, metrics_file) = scenario
    execute(cfg_path)

    assert result_file.exists()
    assert metrics_file.exists()
    assert float(result_file.read_text()) == approx(sum([1, 2, 4]) / 3)


@mark.scenario_name('simple_bash')
def test_simple_bash(scenario):
    cfg_path, (output_file,) = scenario
    execute(cfg_path)

    assert output_file.exists()
    assert output_file.read_text() == 'line with duck\nsecond duck line\n'


@mark.scenario_name('manual_py_env')
def test_manual_py_env(scenario):
    cfg_path, (result_file,) = scenario
    execute(cfg_path)

    assert result_file.exists()
    assert float(result_file.read_text()) == approx(sum([1, 2, 4]) / 3)


@mark.scenario_name('resources_usage')
def test_resources_usage(scenario):
    cfg_path, (files_in_texts_directory_file, dataset_size_file, secret_file) = scenario
    execute(cfg_path)

    assert files_in_texts_directory_file.exists()
    assert files_in_texts_directory_file.read_text().strip() == '2'

    assert dataset_size_file.exists()
    assert dataset_size_file.read_text().split('\t')[0] == '178M'

    assert secret_file.exists()
    assert secret_file.read_text().strip() == 'my-secret-value'


@mark.scenario_name('program_error')
def test_program_error(scenario):
    cfg_path, (debug_file, result_file) = scenario
    execute(cfg_path, expected_return_code=1)

    assert debug_file.exists()
    assert not result_file.exists()


@mark.scenario_name('simple_python')
def test_attach_to_execution(scenario):
    cfg_path, (result_file, metrics_file) = scenario
    execute_with_reattach(cfg_path)

    assert result_file.exists()
    assert metrics_file.exists()


def test_invalid_oauth_token():
    if env == ServerEnv.DEV:
        return

    proc = subprocess.Popen(
        [
            'datasphere', '-t', 'invalid', 'project', 'job', 'get',
            '--id', 'nevermind',
        ],
        stderr=subprocess.PIPE,
    )
    proc.wait(30)
    assert proc.returncode == 1
    stderr_lines = proc.stderr.readlines()
    assert stderr_lines[-5:-2] == [
        b'grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:\n',
        b'\tstatus = StatusCode.UNAUTHENTICATED\n',
        b'\tdetails = "OAuth token is invalid or expired"\n',
    ]


def test_job_not_found():
    proc = subprocess.Popen(
        [
            'datasphere', 'project', 'job', 'get',
            '--id', 'invalid',
        ],
        stderr=subprocess.PIPE,
    )
    proc.wait(30)
    assert proc.returncode == 1
    stderr_lines = proc.stderr.readlines()
    assert stderr_lines[-5:-2] == [
        b'grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:\n',
        b'\tstatus = StatusCode.NOT_FOUND\n',
        b'\tdetails = "Job not found"\n',
    ]
