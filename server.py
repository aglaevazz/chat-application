import os.path
import threading

import messages_pb2 as schema
import users
from data_transfer import DataTransfer


class Server:
    def __init__(self):
        self.connections = {}
        self.data_transfer = self.initialize_data_transfer()

    def initialize_data_transfer(self):
        data_transfer = DataTransfer()
        data_transfer.set_up()
        data_transfer.listen_for_connections()
        data_transfer.register_callback_no_msg_received(self.on_no_msg_received)
        return data_transfer

    def run(self):
        while True:
            connection = self.data_transfer.new_connection()
            # todo: handling of the messages is better placed in function 'handle_connection'(line 66)
            bytes_string = self.data_transfer.receive_data(connection)
            msg = schema.MessageFromClient()
            msg.ParseFromString(bytes_string)
            if msg and msg.request == 'login':
                self.login(msg, connection)
            elif msg and msg.request == 'sign up':
                self.sign_up(msg, connection)
            # todo: third condition unknown message: close the connection

    def login(self, msg, connection):
        if users.is_user(msg.username, msg.name):
            if msg.username in self.connections:
                data = self.create_protobuf_message('already logged in')
                data = data.SerializeToString()
                self.data_transfer.send_data(data, connection)
                # User cannot login from two devices.
                connection.close()
            else:
                self.connections[msg.username] = connection
                data = self.create_protobuf_message('logged in')
                data = data.SerializeToString()
                self.data_transfer.send_data(data, connection)
                # todo: thread should be started inside handle_connection?
                threading.Thread(target=self.handle_connection, args=(connection, msg.username)).start()
        else:
            data = self.create_protobuf_message('not a name/username: login failed')
            data = data.SerializeToString()
            self.data_transfer.send_data(data, connection)
            connection.close()

    def sign_up(self, msg, connection):
        if not users.is_user(msg.username, msg.name):
            users.add_user(msg.username, msg.name)
            self.connections[msg.username] = connection
            data = self.create_protobuf_message('signed up')
            data = data.SerializeToString()
            self.data_transfer.send_data(data, connection)
            # todo: thread should be started inside handle_connection?
            threading.Thread(target=self.handle_connection, args=(connection, msg.username)).start()
        else:
            data = self.create_protobuf_message('occupied username')
            data = data.SerializeToString()
            self.data_transfer.send_data(data, connection)
            connection.close()

    def handle_connection(self, connection, username):
        pending_messages = users.retrieve_pending_messages(username)
        for pending_message in pending_messages:
            sender, text = pending_message
            data = self.create_protobuf_message('message', sender=sender, text=text)
            data = data.SerializeToString()
            self.data_transfer.send_data(data, connection)
        while username in self.connections:
            bytes_string = self.data_transfer.receive_data(connection, username)
            msg = schema.MessageFromClient()
            msg.ParseFromString(bytes_string)
            if msg.request == 'add friend':
                self.add_friend(msg, connection)
            elif msg.request == 'delete friend':
                self.delete_friend(msg, connection)
            elif msg.request == 'list friends':
                self.list_friends(msg, connection)
            elif msg.request == 'message':
                self.send_message_to_friend(msg, connection)
            elif msg.request == 'close':
                self.handle_close_request(msg, connection)
            # todo: else message is unknown and connection should be closed
        return

    def add_friend(self, msg, connection):
        # todo: rename username_friend to friends_username, name_friend to friends_name
        if users.is_user(msg.username_friend, msg.name_friend):
            if users.is_friend(msg.username, msg.username_friend):
                data = self.create_protobuf_message('is friend', username_friend=msg.username_friend)
                data = data.SerializeToString()
                self.data_transfer.send_data(data, connection)
            else:
                users.add_friend(msg.username, msg.username_friend, msg.name_friend)
                data = self.create_protobuf_message('friend added', username_friend=msg.username_friend)
                data = data.SerializeToString()
                self.data_transfer.send_data(data, connection)
        else:
            data = self.create_protobuf_message('friend is not a user', username_friend=msg.username_friend)
            data = data.SerializeToString()
            self.data_transfer.send_data(data, connection)

    def delete_friend(self, msg, connection):
        if users.is_friend(msg.username, msg.username_friend):
            users.delete_friend(msg.username, msg.username_friend)
            data = self.create_protobuf_message('friend deleted', username_friend=msg.username_friend)
            data = data.SerializeToString()
            self.data_transfer.send_data(data, connection)
        else:
            data = self.create_protobuf_message('not a friend', username_friend=msg.username_friend)
            data = data.SerializeToString()
            self.data_transfer.send_data(data, connection)

    def list_friends(self, msg, connection):
        friends = users.list_friends(msg.username)
        data = self.create_protobuf_message('friends list', friends=friends)
        data = data.SerializeToString()
        self.data_transfer.send_data(data, connection)

    def send_message_to_friend(self, msg, connection):
        if users.is_friend(msg.username, msg.username_friend):
            if msg.username_friend in self.connections:
                data = self.create_protobuf_message('message', msg.username, msg.text)
                data = data.SerializeToString()
                self.data_transfer.send_data(data, self.connections[msg.username_friend])
            else:
                users.add_pending_message(msg.username_friend, msg.username, msg.text)
        else:
            # messages can only be send to friends
            data = self.create_protobuf_message('not a friend', username_friend=msg.username_friend)
            data = data.SerializeToString()
            self.data_transfer.send_data(data, connection)

    def handle_close_request(self, msg, connection):
        data = self.create_protobuf_message('closed')
        data = data.SerializeToString()
        self.data_transfer.send_data(data, connection)
        del self.connections[msg.username]

    @staticmethod
    def create_protobuf_message(subject, sender='server', text='', username_friend='', friends=''):
        msg = schema.MessageFromServer()
        msg.subject = subject
        msg.sender = sender
        msg.text = text
        msg.username_friend = username_friend
        # If list of friends was requested the field friends will hold it.
        # Each friend is represented as a protobuf message.
        # todo: this could be done without creating a protobuf message for each friend
        for friend in friends:
            proto_friend = schema.Friend()
            proto_friend.username = friend[0]
            proto_friend.name = friend[1]
            msg.friends.extend([proto_friend])
        return msg

    def on_no_msg_received(self, connection, username):
        if username in self.connections:
            # delete connection from current connections if no message has been received.
            del self.connections[username]
        connection.close()


if __name__ == '__main__':
    server = Server()
    if not os.path.isfile('users.db'):
        users.set_up_database()
    server.run()







