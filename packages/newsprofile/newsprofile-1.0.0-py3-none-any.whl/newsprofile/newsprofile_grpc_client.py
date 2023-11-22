import grpc
from newsprofile.newsprofile_channel_pool import NewsprofileChannelPool
from newsprofile.NewsprofileService_pb2_grpc import NewsprofileServiceStub
from newsprofile.NewsprofileService_pb2 import NewsprofileRequest


class NewsprofileGrpcClient(object):
    _instance = None

    def __init__(self, host, port, pool_size, timeout):
        if not hasattr(self, "channel_pool"):
            self.channel_pool = NewsprofileChannelPool(host, port, pool_size, timeout)

    def __new__(cls, host, port, pool_size, timeout, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NewsprofileGrpcClient, cls).__new__(cls)
        return cls._instance

    def get_newsprofile_documents(self, aids, *args, **kwargs):
        channel = self.channel_pool.borrow_channel()
        result = {}
        try:
            stub = NewsprofileServiceStub(channel)
            request = NewsprofileRequest(aids=aids)
            response = stub.GetNewsprofiles(request)
            result = response.document_map
        except Exception as e:
            print(e)
        finally:
            if channel is not None:
                self.channel_pool.return_channel(channel)
        return result
