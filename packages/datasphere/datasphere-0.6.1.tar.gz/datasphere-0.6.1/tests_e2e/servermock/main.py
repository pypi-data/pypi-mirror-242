import argparse
from concurrent import futures
import grpc

from yandex.cloud.datasphere.v2.jobs.project_job_service_pb2_grpc import add_ProjectJobServiceServicer_to_server
from yandex.cloud.operation.operation_service_pb2_grpc import add_OperationServiceServicer_to_server

from service import Service, OperationService
from storage import S3Client, storage_endpoint_url

parser = argparse.ArgumentParser(prog='DataSphere script executor server mock')
parser.add_argument(
    '-b', '--bucket', required=True,
    help=f'S3 bucket to store user script files using {storage_endpoint_url} S3 endpoint. Also export '
         f'AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY environment variables if this bucket is not public.',
)
parser.add_argument('-c', '--conda', required=True, help='Conda home path')  # TODO: use `conda activate` instead
parser.add_argument('-p', '--port', default='50051', help='TCP port')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    args = parser.parse_args()
    service = Service(S3Client(args.bucket), args.conda)
    op_service = OperationService()
    add_ProjectJobServiceServicer_to_server(service, server)
    add_OperationServiceServicer_to_server(op_service, server)
    server.add_insecure_port('[::]:' + args.port)
    server.start()
    print('Server started, listening on ' + args.port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
