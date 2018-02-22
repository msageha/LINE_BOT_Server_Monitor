"""The Python implementation of the GRPC gateway.Greeter client."""

from __future__ import print_function

import grpc
import sys
sys.path.append('../protos/')
import gateway_pb2
import gateway_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = gateway_pb2_grpc.MonitorStub(channel)
    response = stub.CheckServer(gateway_pb2.LineBotServerRequest(type='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()
