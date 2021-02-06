from data_transfer import DataTransfer
import messages_pb2 as schema


class Client:
    def __init__(self):
        self.username = None
        self.name = None
        self.connected = False
        self.data_transfer = None
        self.initiate_data_transfer()

        # register callbacks
        # todo: rename fail_callback to 'general_error' or something else more descriptive
        self.fail_callback = None
        self.sign_up_success_callback = None
        self.sign_up_failed_occupied_username_callback = None
        self.login_success_callback = None
        self.login_failed_not_a_user_callback = None
        self.login_failed_already_logged_in_callback = None
        # todo: rename new_message_callback to 'new_message_for_user_callback' or something else more descriptive
        self.new_message_callback = None
        # todo: rename friends_list_callback to 'list_of_friends_callback' or something else more descriptive
        self.friends_list_callback = None
        self.is_friend_callback = None
        self.friend_added_callback = None
        self.not_a_friend_callback = None
        self.friend_deleted_callback = None
        self.friend_is_not_a_user_callback = None
        self.connection_closed_callback = None

    def initiate_data_transfer(self):
        self.data_transfer = DataTransfer()
        self.data_transfer.set_up()

    # The receive-loop is running in the UI's-Main-Thread.
    def receive_loop(self):
        while self.connected:
            bytes_string = self.data_transfer.receive_data()
            if bytes_string:
                msg = schema.MessageFromServer()
                msg.ParseFromString(bytes_string)
                if msg.subject == 'logged in':
                    if self.login_success_callback:
                        self.login_success_callback()
                elif msg.subject == 'already logged in':
                    if self.login_failed_already_logged_in_callback:
                        self.login_failed_already_logged_in_callback()
                elif msg.subject == 'not a name/username: login failed':
                    if self.login_failed_not_a_user_callback:
                        self.login_failed_not_a_user_callback()
                elif msg.subject == 'signed up':
                    # todo: rename to 'sign_up_succeeded'
                    if self.sign_up_success_callback:
                        self.sign_up_success_callback()
                elif msg.subject == 'occupied username':
                    if self.sign_up_failed_occupied_username_callback:
                        self.sign_up_failed_occupied_username_callback()
                elif msg.subject == 'message':
                    # todo: rename see line 21
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
                # no message received or message is unknown
                else:
                    if self.fail_callback:
                        self.fail_callback()
            else:
                print('not working')

    # Requests the Client sends to the server:
    def sign_up(self, username, name):
        self.username, self.name = username, name
        protobuf_message = self.create_protobuf_message('sign up')
        self.connect(protobuf_message)

    def login(self, username, name):
        self.username, self.name = username, name
        protobuf_message = self.create_protobuf_message('login')
        self.connect(protobuf_message)

    def connect(self, protobuf_message):
        bytes_string = protobuf_message.SerializeToString()
        self.data_transfer.connect_to_server(bytes_string)
        self.connected = True
        self.receive_loop()

    def logout(self):
        protobuf_message = self.create_protobuf_message('close')
        bytes_string = protobuf_message.SerializeToString()
        self.data_transfer.send_data(bytes_string)

    def add_friend(self, username_friend, name_friend):
        protobuf_message = self.create_protobuf_message('add friend', username_friend, name_friend=name_friend)
        bytes_string = protobuf_message.SerializeToString()
        self.data_transfer.send_data(bytes_string)

    def delete_friend(self, username_friend):
        protobuf_message = self.create_protobuf_message('delete friend', username_friend)
        bytes_string = protobuf_message.SerializeToString()
        self.data_transfer.send_data(bytes_string)

    def request_friends_list(self):
        protobuf_message = self.create_protobuf_message('list friends')
        bytes_string = protobuf_message.SerializeToString()
        self.data_transfer.send_data(bytes_string)

    def send_message(self, username_friend, message):
        protobuf_message = self.create_protobuf_message('message', username_friend, message)
        bytes_string = protobuf_message.SerializeToString()
        self.data_transfer.send_data(bytes_string)

    def create_protobuf_message(self, request, username_friend='', text='', name_friend=''):
        protobuf_message = schema.MessageFromClient()
        protobuf_message.request = request
        protobuf_message.username = self.username
        protobuf_message.name = self.name
        protobuf_message.username_friend = username_friend
        protobuf_message.name_friend = name_friend
        protobuf_message.text = text
        return protobuf_message

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
