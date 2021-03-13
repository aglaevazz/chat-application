import socket


class DataTransfer:

    def __init__(self, port=10000):
        self.port = port
        self.sock = None
        self.no_msg_received_callback = None

    def register_callback_no_msg_received(self, callback):
        self.no_msg_received_callback = callback

    def set_up(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen_for_connections(self):
        # The following line is to reuse the port after it closed without a waiting time.
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # todo: set socket to be non-blocking
        self.sock.bind(('localhost', self.port))
        self.sock.listen(5)

    def new_connection(self):
        connection, address = self.sock.accept()
        return connection

    def connect_to_server(self, bytes_string):
        self.sock.connect(('localhost', self.port))
        # request is 'login' for login or 'sign up' for sign up.
        self.send_data(bytes_string, self.sock)

    def send_data(self, bytes_string, connection=None):
        if not connection:
            connection = self.sock
        # Serializes data (protobuf message) to a binary string
        # bytes_string = protobuf_msg.SerializeToString()
        # todo: Should check for errors sending the data. E.g. connection could be broken.
        #  Also 'sendall' returns None on success.
        connection.sendall(bytes_string)

    def receive_data(self, connection=None, username=None):
        if not connection:
            connection = self.sock
        # todo: solve problem if message is bigger than 1024
        bytes_string = connection.recv(1024)
        if bytes_string:
            return bytes_string
        elif self.no_msg_received_callback:
            self.no_msg_received_callback(connection, username)

    def close(self):
        # SHUT_RDWR = further sends and receives are not allowed.
        self.sock.shutdown(socket.SHUT_RDWR)
        # Releases the resource.
        self.sock.close()

