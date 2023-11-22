import queue
import grpc


class NewsprofileChannelPool(object):
    def __init__(self, host, port, pool_size, timeout):
        self.host = host
        self.port = port
        self.pool_size = pool_size
        self.timeout = timeout
        self.pool = queue.Queue(self.pool_size)
        self.create_pool()

    def create_pool(self):
        if self.pool_size - self.pool.qsize() <= 0:
            return
        for i in range(self.pool_size - self.pool.qsize()):
            channel = self.create_channel()
            self.pool.put(channel)

    def create_channel(self):
        channel = grpc.insecure_channel(self.host + ":" + str(self.port))
        print("create channel end: " + str(id(channel)))
        return channel

    def borrow_channel(self):
        channel = self.pool.get(self.timeout)
        if channel is None:
            channel = self.create_channel()
        return channel

    def return_channel(self, channel):
        if channel is not None:
            self.pool.put(channel)

    def shut_down(self):
        if self.pool:
            while self.pool.qsize() > 0:
                channel = self.pool.get()
                channel.close()

    def qsize(self):
        return self.pool.qsize()