import unittest
from data_transfer import DataTransfer
from mock import Mock
import socket
import messages_pb2 as schema


class TestDataTransfer(unittest.TestCase):

    def setUp(self):
        self.data_transfer = DataTransfer()
        self.data_transfer.sock = Mock()
        self.protobuf_msg = Mock()
        self.connection = Mock()

    def test_register_callback(self):
        self.data_transfer.register_callback_no_msg_received('Test')
        self.assertEqual(self.data_transfer.no_msg_received_callback, 'Test')

    def test_set_up(self):
        socket.socket = Mock()
        self.data_transfer.set_up()
        socket.socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)

    def test_listen_for_connections_1(self):
        self.data_transfer.listen_for_connections()
        self.data_transfer.sock.setsockopt.assert_called_once_with(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def test_listen_for_connections_2(self):
        self.data_transfer.listen_for_connections()
        self.data_transfer.sock.bind.assert_called_once_with(('localhost', self.data_transfer.port))

    def test_listen_for_connections_3(self):
        self.data_transfer.listen_for_connections()
        self.data_transfer.sock.listen.assert_called_once_with(5)

    def test_connect_to_server_1(self):
        self.data_transfer.connect_to_server(self.protobuf_msg)
        self.data_transfer.sock.connect.assert_called_once_with(('localhost', 10000))

    def test_connect_to_server_2(self):
        self.data_transfer.send_data = Mock()
        data = self.protobuf_msg.SerializeToString()
        self.data_transfer.connect_to_server(data)
        self.data_transfer.send_data.assert_called_once_with(data, self.data_transfer.sock)

    def test_send_data(self):
        data = self.protobuf_msg.SerializeToString()
        self.data_transfer.send_data(data, self.connection)
        self.connection.sendall.assert_called_once_with(data)

    def test_receive_data_1(self):
        self.connection.recv.return_value = schema.MessageFromServer().SerializeToString()
        self.data_transfer.receive_data(self.connection)
        self.connection.recv.assert_called_once_with(1024)

    def test_receive_data_2(self):
        self.connection.recv.return_value = schema.MessageFromServer().SerializeToString()
        self.data_transfer.receive_data = Mock()
        self.data_transfer.receive_data.return_value = schema.MessageFromServer()
        self.assertEqual(self.data_transfer.receive_data(self.connection), schema.MessageFromServer())

    def test_receive_data_3(self):
        self.data_transfer.sock.recv.return_value = None
        self.data_transfer.no_msg_received_callback = Mock()
        self.data_transfer.receive_data()
        self.data_transfer.no_msg_received_callback.assert_called_once()

    def test_close_1(self):
        self.data_transfer.close()
        self.data_transfer.sock.shutdown.assert_called_once_with(socket.SHUT_RDWR)

    def test_close_2(self):
        self.data_transfer.close()
        self.data_transfer.sock.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
