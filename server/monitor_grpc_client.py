"""The Python implementation of the GRPC gateway.Greeter client."""

from __future__ import print_function

import grpc
import sys
sys.path.append('../protos/')
import gateway_pb2
import gateway_pb2_grpc
import random

def run(request_type, host, port=50051):
    with open('key.txt') as f:
        key = int(f.readline())
    if request_type == 'certificate':
        key = random.randint(100000, 999999)
        with open('key.txt', 'w') as f:
            f.write(str(key))
    channel = grpc.insecure_channel(f'{host}:{port}')
    stub = gateway_pb2_grpc.MonitorStub(channel)
    response = stub.CheckServer(gateway_pb2.LineBotServerRequest(type=request_type, key=key))
    # print(f"Greeter client received: {response.key}")
    if key == response.key:
        return response.key, response.dict
    return 0, {}

if __name__ == '__main__':
    run('info', 'localhost')
