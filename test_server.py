import unittest
from mock import Mock
import threading
import messages_pb2 as schema
from server import Server


class TestServer(unittest.TestCase):

    def setUp(self):
        self.server = Server()
        self.server.db = Mock()
        self.server.data_transfer = Mock()

    def test_initialize_data_transfer(self):
        self.server.initialize_data_transfer()
        self.server.data_transfer.set_up.assert_called_once()
        self.server.data_transfer.listen_for_connections.assert_called_once()
        self.server.data_transfer.register_callback_no_msg_received.assert_called_once_with(self.server.on_no_msg_received)

    def test_run(self):
        self.server.threading = Mock()
        threading.Thread(target=self.server.run).start()
        self.server.is_running = False
        self.server.data_transfer.new_connection.assert_called()
        connection = Mock()
        self.server.threading.Thread(target=self.server.handle_connection, args=(connection,)).start.assert_called()

    def test_handle_connection_login(self):
        connection = Mock()
        self.server.receive_msg = Mock()
        msg = self.create_protobuf_message_from_client('login')
        self.server.receive_msg.return_value = msg
        self.server.login = Mock()
        self.server.receive_loop = Mock()
        self.server.handle_connection(connection)
        self.server.receive_msg.assert_called_once_with(connection)
        self.assertEqual(self.server.connections[msg.username], connection)
        self.server.login.assert_called_once_with(msg, connection)
        self.server.receive_loop.assert_called_once_with(msg.username, connection)

    def test_handle_connection_sign_up(self):
        connection = Mock()
        self.server.receive_msg = Mock()
        msg = self.create_protobuf_message_from_client('sign up')
        self.server.receive_msg.return_value = msg
        self.server.sign_up = Mock()
        self.server.receive_loop = Mock()
        self.server.handle_connection(connection)
        self.server.receive_msg.assert_called_once_with(connection)
        self.assertEqual(self.server.connections[msg.username], connection)
        self.server.sign_up.assert_called_once_with(msg, connection)
        self.server.receive_loop.assert_called_once_with(msg.username, connection)

    def test_handle_close_request(self):
        msg = self.create_protobuf_message_from_client('close')
        connection = Mock()
        self.server.create_protobuf_message = Mock()
        self.server.delete_connection = Mock()
        self.server.handle_close_request(msg, connection)
        self.server.create_protobuf_message.assert_called_once_with('closed')
        self.server.data_transfer.send_data.assert_called_once()
        self.server.delete_connection.assert_called_once_with(connection, msg.username)

    def test_receive_loop_add_friend(self):
        username = 'test_username'
        connection = Mock()
        self.server.connections = {username: connection}
        self.server.add_friend = Mock()
        self.server.receive_msg = Mock()
        msg1 = self.create_protobuf_message_from_client('add friend')
        msg2 = self.create_protobuf_message_from_client('close')
        self.server.receive_msg.side_effect = [msg1, msg2]
        self.server.receive_loop(username, connection)
        self.server.add_friend.assert_called_once_with(msg1, connection)

    def test_receive_loop_delete_friend(self):
        username = 'test_username'
        connection = Mock()
        self.server.connections = {username: connection}
        self.server.delete_friend = Mock()
        self.server.receive_msg = Mock()
        msg1 = self.create_protobuf_message_from_client('delete friend')
        msg2 = self.create_protobuf_message_from_client('close')
        self.server.receive_msg.side_effect = [msg1, msg2]
        self.server.receive_loop(username, connection)
        self.server.delete_friend.assert_called_once_with(msg1, connection)

    def test_receive_loop_list_friends(self):
        username = 'test_username'
        connection = Mock()
        self.server.connections = {username: connection}
        self.server.list_friends = Mock()
        self.server.receive_msg = Mock()
        msg1 = self.create_protobuf_message_from_client('list friends')
        msg2 = self.create_protobuf_message_from_client('close')
        self.server.receive_msg.side_effect = [msg1, msg2]
        self.server.receive_loop(username, connection)
        self.server.list_friends.assert_called_once_with(msg1, connection)

    def test_receive_loop_message(self):
        username = 'test_username'
        connection = Mock()
        self.server.connections = {username: connection}
        self.server.send_message_to_friend = Mock()
        self.server.receive_msg = Mock()
        msg1 = self.create_protobuf_message_from_client('message')
        msg2 = self.create_protobuf_message_from_client('close')
        self.server.receive_msg.side_effect = [msg1, msg2]
        self.server.receive_loop(username, connection)
        self.server.send_message_to_friend.assert_called_once_with(msg1, connection)

    def test_receive_message(self):
        connection = Mock()
        protobuf_message = self.create_protobuf_message_from_client('test_message')
        bytes_string = protobuf_message.SerializeToString()
        self.server.data_transfer.receive_data.return_value = bytes_string
        self.assertEqual(self.server.receive_msg(connection), protobuf_message)

    def test_login_is_user(self):
        msg = self.create_protobuf_message_from_client('test_message')
        connection = Mock()
        self.server.db = Mock()
        self.server.db.is_user.return_value = True
        self.server.create_protobuf_message = Mock()
        self.server.send_pending_messages = Mock()
        self.server.login(msg, connection)
        self.server.create_protobuf_message.assert_called_once_with('logged in')
        self.server.data_transfer.send_data.assert_called_once()
        self.server.send_pending_messages.assert_called_once_with(msg.username, connection)

    def test_login_not_a_user(self):
        msg = self.create_protobuf_message_from_client('test_message')
        connection = Mock()
        self.server.db = Mock()
        self.server.db.is_user.return_value = False
        self.server.create_protobuf_message = Mock()
        self.server.delete_connection = Mock()
        self.server.login(msg, connection)
        self.server.create_protobuf_message.assert_called_once_with('not a name/username: login failed')
        self.server.data_transfer.send_data.assert_called_once()
        self.server.delete_connection.assert_called_once_with(connection, msg.username)

    @staticmethod
    def create_protobuf_message_from_client(request, username_friend='', text='', name_friend=''):
        protobuf_message = schema.MessageFromClient()
        protobuf_message.request = request
        protobuf_message.username = 'test_username'
        protobuf_message.name = 'test_name'
        protobuf_message.username_friend = username_friend
        protobuf_message.name_friend = name_friend
        protobuf_message.text = text
        return protobuf_message


if __name__ == '__main__':
    unittest.main()
