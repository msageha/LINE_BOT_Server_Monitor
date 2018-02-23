"""The Python implementation of the GRPC gateway.Greeter server."""

from concurrent import futures
import time
import random

import grpc

import sys
sys.path.append('../protos/')
import gateway_pb2
import gateway_pb2_grpc

from get_pc_info import Info

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Monitor(gateway_pb2_grpc.MonitorServicer):
    def __init__(self):
        self.response = Response()

    def CheckServer(self, request, context):
        response_key, response_dict = self.response(request.type, request.key)
        return gateway_pb2.MonitorReply(key=response_key, dict=response_dict)

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

class Response:
    def __init__(self):
        self.info = Info()
        with open('key.txt', 'r') as f:
            key = f.readline()
        self.key = int(key)

    def __call__(self, request_type, request_key):
        if request_type == 'certificate':
            self.key = request_key
            print('認証キー：{0}'.format(self.key))
            with open('key.txt', 'w') as f:
                f.write(str(self.key))
            return self.key, {}

        elif request_key == self.key:
            if request_type == 'info':
                return self.key, self.info()
        
        return 0, {}

if __name__ == '__main__':
    serve()
