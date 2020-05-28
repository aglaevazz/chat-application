import os.path
import socket
import threading

import messages_pb2 as schema
import users


class Server:
    def __init__(self, host='0.0.0.0', port=10000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.connections = {}
        if __name__ == '__main__':
            if not os.path.isfile('users.db'):
                users.set_up_database()
            self.run()

    def run(self):
        while True:
            connection, address = self.sock.accept()
            msg = self.receive_data(connection)
            if msg.request == 'login':
                self.login(msg, connection)
            elif msg.request == 'sign up':
                self.sign_up(msg, connection)

    def login(self, msg, connection):
        if users.is_user(msg.username, msg.name):
            if msg.username in self.connections:
                data = self.create_protobuf_message('already logged in')
                self.send_data(connection, data)
                connection.close()
            else:
                self.connections[msg.username] = connection
                data = self.create_protobuf_message('logged in')
                self.send_data(connection, data)
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
                self.handle_close_request(msg, username)
        return

    def add_friend(self, msg, connection):
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
            data = self.create_protobuf_message('not a friend', username_friend=msg.username_friend)
            self.send_data(connection, data)

    def handle_close_request(self, msg, connection):
        data = self.create_protobuf_message('closed')
        self.send_data(connection, data)
        del self.connections[msg.username]
        connection.close()

    @staticmethod
    def create_protobuf_message(subject, sender='server', text='', username_friend='', friends=''):
        msg = schema.MessageFromServer()
        msg.subject = subject
        msg.sender = sender
        msg.text = text
        msg.username_friend = username_friend
        for friend in friends:
            proto_friend = schema.Friend()
            proto_friend.username = friend[0]
            proto_friend.name = friend[1]
            msg.friends.extend([proto_friend])
        return msg

    @staticmethod
    def send_data(connection, data):
        bytes_string = data.SerializeToString()
        connection.sendall(bytes_string)

    def receive_data(self, connection, username=None):
        bytes_string = connection.recv(1024)
        if bytes_string:
            msg = schema.MessageFromClient()
            msg.ParseFromString(bytes_string)
            return msg
        elif username in self.connections:
            del self.connections[username]
        connection.close()


if __name__ == '__main__':
    server = Server()







