import grpc
import NewsprofileService_pb2
import NewsprofileService_pb2_grpc

class NewsprofileGrpcClient(object):
    def __init__(self, host, port, pool_size, timeout):
        self.pool = NewsprofileChannelPool(host, port, pool_size, timeout)

    def apply(self, func, *args, **kwargs):
        channel = self.pool.borrow_channel
        stub = NewsprofileService_pb2_grpc.NewsprofileServiceStub(channel)
