import socket

import messages_pb2 as schema


class Client:
    def __init__(self):
        self.username = None
        self.name = None
        self.sock = None
        self.connected = False

        # register callbacks
        self.fail_callback = None
        self.sign_up_success_callback = None
        self.sign_up_failed_occupied_username_callback = None
        self.login_success_callback = None
        self.login_failed_not_a_user_callback = None
        self.login_failed_already_logged_in_callback = None
        self.new_message_callback = None
        self.friends_list_callback = None
        self.is_friend_callback = None
        self.friend_added_callback = None
        self.not_a_friend_callback = None
        self.friend_deleted_callback = None
        self.friend_is_not_a_user_callback = None
        self.connection_closed_callback = None

    # The receive-loop is running in the UI's-Main-Thread.
    def receive_loop(self):
        while self.connected:
            msg = self.receive_data()
            if msg.subject == 'logged in':
                self.login_success_callback()
            elif msg.subject == 'already logged in':
                self.login_failed_already_logged_in_callback()
            elif msg.subject == 'not a name/username: login failed':
                self.login_failed_not_a_user_callback()
            elif msg.subject == 'signed up':
                self.sign_up_success_callback()
            elif msg.subject == 'occupied username':
                self.sign_up_failed_occupied_username_callback()
            elif msg.subject == 'message':
                if self.new_message_callback:
                    self.new_message_callback(msg)
            elif msg.subject == 'friends list':
                if self.friends_list_callback:
                    self.friends_list_callback(msg)
            elif msg.subject == 'is friend':
                if self.is_friend_callback:
                    self.is_friend_callback(msg)
            elif msg.subject == 'friend added':
                if self.friend_added_callback:
                    self.friend_added_callback(msg)
            elif msg.subject == 'not a friend':
                if self.not_a_friend_callback:
                    self.not_a_friend_callback(msg)
            elif msg.subject == 'friend is not a user':
                if self.friend_is_not_a_user_callback:
                    self.friend_is_not_a_user_callback(msg)
            elif msg.subject == 'friend deleted':
                if self.friend_deleted_callback:
                    self.friend_deleted_callback(msg)
            elif msg.subject == 'closed':
                self.connected = False
                if self.connection_closed_callback:
                    self.connection_closed_callback()
            else:
                if self.fail_callback:
                    self.fail_callback()

# Requests the Client sends to the server:
    def sign_up(self, username, name):
        self.username, self.name = username, name
        self.connect_to_server('sign up')

    def login(self, username, name):
        self.username, self.name = username, name
        self.connect_to_server('login')

    def logout(self):
        protobuf_message = self.create_protobuf_message('close')
        self.send_data(protobuf_message)

    def add_friend(self, username_friend, name_friend):
        protobuf_message = self.create_protobuf_message('add friend', username_friend, name_friend=name_friend)
        self.send_data(protobuf_message)

    def delete_friend(self, username_friend):
        protobuf_message = self.create_protobuf_message('delete friend', username_friend)
        self.send_data(protobuf_message)

    def request_friends_list(self):
        protobuf_message = self.create_protobuf_message('list friends')
        self.send_data(protobuf_message)

    def send_message(self, username_friend, message):
        protobuf_message = self.create_protobuf_message('message', username_friend, message)
        self.send_data(protobuf_message)

    # Basic functions to connect and send data to the server.
    def connect_to_server(self, request):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('0.0.0.0', 10000))
        protobuf_message = self.create_protobuf_message(request, self.username, self.name)
        self.send_data(protobuf_message)
        self.connected = True
        self.receive_loop()

    def create_protobuf_message(self, request, username_friend='', text='', name_friend=''):
        protobuf_message = schema.MessageFromClient()
        protobuf_message.request = request
        protobuf_message.username = self.username
        protobuf_message.name = self.name
        protobuf_message.username_friend = username_friend
        protobuf_message.name_friend = name_friend
        protobuf_message.text = text
        return protobuf_message

    def send_data(self, protobuf_message):
        bytes_string = protobuf_message.SerializeToString()
        self.sock.sendall(bytes_string)

    def receive_data(self):
        bytes_string = self.sock.recv(1024)
        msg = schema.MessageFromServer()
        msg.ParseFromString(bytes_string)
        return msg

# Register the callback-functions to the Client.
    def register_callback_fail(self, callback):
        self.fail_callback = callback

    def register_callback_sign_up_success(self, callback):
        self.sign_up_success_callback = callback

    def register_callback_sign_up_failed_occupied_username(self, callback):
        self.sign_up_failed_occupied_username_callback = callback

    def register_callback_login_success(self, callback):
        self.login_success_callback = callback

    def register_callback_login_failed_not_a_user(self, callback):
        self.login_failed_not_a_user_callback = callback

    def register_callback_login_failed_already_logged_in(self, callback):
        self.login_failed_already_logged_in_callback = callback

    def register_callback_new_message(self, callback):
        self.new_message_callback = callback

    def register_callback_friends_list(self, callback):
        self.friends_list_callback = callback

    def register_callback_is_friend(self, callback):
        self.is_friend_callback = callback

    def register_callback_friend_added(self, callback):
        self.friend_added_callback = callback

    def register_callback_not_a_friend(self, callback):
        self.not_a_friend_callback = callback

    def register_callback_friend_deleted(self, callback):
        self.friend_deleted_callback = callback

    def register_callback_friend_is_not_a_user(self, callback):
        self.friend_is_not_a_user_callback = callback

    def register_callback_connection_closed(self, callback):
        self.connection_closed_callback = callback
