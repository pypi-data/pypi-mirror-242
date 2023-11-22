import queue

class NewsprofileChannelPool(object):
    def __init__(self, host, port, pool_size, timeout):
        self.host = host
        self.port = port
        self.pool_size = pool_size
        self.timeout = timeout
        self.pool = queue.Queue(self.pool_size)

    def create_pool(self):
        for i in self.pool_size:
            channel = create_channel()
            self.pool.put(channel)

    def create_channel(self):
        channel = grpc.insecure_channel(host + ":" + str(port))
        return channel

    def borrow_channel(self):
        channel = self.pool.get(self.timeout)
        if channel is None or channel.isShutDown():
            channel = create_channel
        return channel

    def return_channel(self):
        if channel is not None and not channel.isShutDown():
            self.pool.put(channel)