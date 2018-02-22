"""The Python implementation of the GRPC gateway.Greeter server."""

from concurrent import futures
import time

import grpc

import sys
sys.path.append('../protos/')
import gateway_pb2
import gateway_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Monitor(gateway_pb2_grpc.MonitorServicer):

    def CheckServer(self, request, context):
        return gateway_pb2.MonitorReply(message='Hello, %s!' % request.type)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gateway_pb2_grpc.add_MonitorServicer_to_server(Monitor(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
