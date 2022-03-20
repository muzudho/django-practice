import grpc
import account_pb2
import account_pb2_grpc

with grpc.insecure_channel('0.0.0.0:8000') as channel:
    #                       ------- ----
    #                       1       2
    # 1. Docker を使っているときは localhost ではなく 0.0.0.0 にする
    # 2. ポート番号
    stub = account_pb2_grpc.UserControllerStub(channel)
    for user in stub.List(account_pb2.UserListRequest()):
        print(user, end='')
