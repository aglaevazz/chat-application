import os.path
import socket
import threading

import messages_pb2 as schema
import users


class Server:
    def __init__(self, port=10000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following line is to reuse the port after it closed without a waiting time.
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # todo: set socket to be non-blocking
        self.sock.bind(('localhost', port))
        # todo: socket should listen to max 5 connection requests (5 = normal max)
        self.sock.listen(1)
        self.connections = {}

    def run(self):
        while True:
            connection, address = self.sock.accept()
            # todo: handling of the messages is better placed in function 'handle_connection'(line 66)
            msg = self.receive_data(connection)
            if msg and msg.request == 'login':
                self.login(msg, connection)
            elif msg and msg.request == 'sign up':
                self.sign_up(msg, connection)
            # todo: third condition unknown message: close the connection

    def login(self, msg, connection):
        if users.is_user(msg.username, msg.name):
            if msg.username in self.connections:
                data = self.create_protobuf_message('already logged in')
                self.send_data(connection, data)
                # User cannot login from two devices.
                connection.close()
            else:
                self.connections[msg.username] = connection
                data = self.create_protobuf_message('logged in')
                self.send_data(connection, data)
                # todo: thread should be started inside handle_connection?
                threading.Thread(target=self.handle_connection, args=(connection, msg.username)).start()
        else:
            data = self.create_protobuf_message('not a name/username: login failed')
            self.send_data(connection, data)
            connection.close()

    def sign_up(self, msg, connection):
        if not users.is_user(msg.username, msg.name):
            users.add_user(msg.username, msg.name)
            self.connections[msg.username] = connection
            data = self.create_protobuf_message('signed up')
            self.send_data(connection, data)
            # todo: thread should be started inside handle_connection?
            threading.Thread(target=self.handle_connection, args=(connection, msg.username)).start()
        else:
            data = self.create_protobuf_message('occupied username')
            self.send_data(connection, data)
            connection.close()

    def handle_connection(self, connection, username):
        pending_messages = users.retrieve_pending_messages(username)
        for pending_message in pending_messages:
            sender, text = pending_message
            data = self.create_protobuf_message('message', sender=sender, text=text)
            self.send_data(connection, data)
        while username in self.connections:
            msg = self.receive_data(connection, username)
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
                self.send_data(connection, data)
            else:
                users.add_friend(msg.username, msg.username_friend, msg.name_friend)
                data = self.create_protobuf_message('friend added', username_friend=msg.username_friend)
                self.send_data(connection, data)
        else:
            data = self.create_protobuf_message('friend is not a user', username_friend=msg.username_friend)
            self.send_data(connection, data)

    def delete_friend(self, msg, connection):
        if users.is_friend(msg.username, msg.username_friend):
            users.delete_friend(msg.username, msg.username_friend)
            data = self.create_protobuf_message('friend deleted', username_friend=msg.username_friend)
            self.send_data(connection, data)
        else:
            data = self.create_protobuf_message('not a friend', username_friend=msg.username_friend)
            self.send_data(connection, data)

    def list_friends(self, msg, connection):
        friends = users.list_friends(msg.username)
        data = self.create_protobuf_message('friends list', friends=friends)
        self.send_data(connection, data)

    def send_message_to_friend(self, msg, connection):
        if users.is_friend(msg.username, msg.username_friend):
            if msg.username_friend in self.connections:
                data = self.create_protobuf_message('message', msg.username, msg.text)
                self.send_data(self.connections[msg.username_friend], data)
            else:
                users.add_pending_message(msg.username_friend, msg.username, msg.text)
        else:
            # messages can only be send to friends
            data = self.create_protobuf_message('not a friend', username_friend=msg.username_friend)
            self.send_data(connection, data)

    def handle_close_request(self, msg, connection):
        data = self.create_protobuf_message('closed')
        self.send_data(connection, data)
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

    @staticmethod
    def send_data(connection, data):
        # Serializes data (protobuf message) to a binary string
        bytes_string = data.SerializeToString()
        # todo: Should check for errors sending the data. E.g. connection could be broken.
        #  Also 'sendall' returns None on success.
        connection.sendall(bytes_string)

    def receive_data(self, connection, username=None):
        # todo: solve problem if message is bigger than 1024
        bytes_string = connection.recv(1024)
        if bytes_string:
            msg = schema.MessageFromClient()
            msg.ParseFromString(bytes_string)
            return msg
        elif username in self.connections:
            # delete connection from current connections if no message has been received.
            del self.connections[username]
        connection.close()

    def close(self):
        # SHUT_RDWR = further sends and receives are not allowed.
        self.sock.shutdown(socket.SHUT_RDWR)
        # Releases the resource.
        self.sock.close()


if __name__ == '__main__':
    server = Server()
    if not os.path.isfile('users.db'):
        users.set_up_database()
    server.run()







