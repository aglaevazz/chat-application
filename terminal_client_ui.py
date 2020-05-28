import sys
import threading
import time

from client import Client


class TerminalUI:
    def __init__(self):
        self.client = Client()
        self.register_callbacks()
        self.request_thread = threading.Thread(target=self.request)
        self.request_thread.daemon = True
        self.login_or_signup()

    def register_callbacks(self):
        # Register general-fail callback:
        self.client.register_callback_fail(self.on_fail)
        # Register sign_up callbacks:
        self.client.register_callback_sign_up_success(self.on_sign_up_success)
        self.client.register_callback_sign_up_failed_occupied_username(self.on_sign_up_failed_occupied_username)
        # Register sign_up callbacks:
        self.client.register_callback_login_success(self.on_login_success)
        self.client.register_callback_login_failed_not_a_user(self.on_login_failed_not_a_user)
        self.client.register_callback_login_failed_already_logged_in(self.on_login_failed_already_logged_in)
        # Register other request callbacks:
        self.client.register_callback_new_message(self.on_new_message)
        self.client.register_callback_friends_list(self.on_friends_list)
        self.client.register_callback_is_friend(self.on_is_friend)
        self.client.register_callback_friend_added(self.on_friend_added)
        self.client.register_callback_not_a_friend(self.on_not_a_friend)
        self.client.register_callback_friend_deleted(self.on_friend_deleted)
        self.client.register_callback_friend_is_not_a_user(self.on_friend_is_not_a_user)
        self.client.register_callback_connection_closed(self.on_connection_closed)

    def login_or_signup(self):
        request = input('''
        If you wish to sign up, please enter s
        If you wish to login please enter l
        If you wish to exit the program enter e\n
        ''')
        if request == 's':
            username, name = self.get_user_info()
            self.client.sign_up(username, name)
        elif request == 'l':
            username, name = self.get_user_info()
            self.client.login(username, name)
        elif request == 'e':
            sys.exit()
        else:
            print("Sorry, I didn't understand this input...\n")
            self.login_or_signup()

    @staticmethod
    def get_user_info():
        name = input('Please enter your first name: ')
        username = input('Please chose and enter a username: ')
        return username, name

    def request(self):
        running = True
        while running:
            print('''
            Send a message: enter 'm'
            Add a new friend: enter 'a'
            Delete a friend:  enter 'd'
            Get a list of your friends: enter 'l'
            Close the connection: enter 'c'\n
            ''')
            command = input()
            if command == 'm':
                self.send_message()
            elif command == 'a':
                self.add_friend()
            elif command == 'l':
                self.client.request_friends_list()
            elif command == 'd':
                self.delete_friend()
            elif command == 'c':
                self.client.logout()
                running = False
            else:
                print("Sorry, I didn't understand your input...")
            time.sleep(2)
        return

    # Additional functions to execute user-requests:
    def send_message(self):
        friends_username = input('Please enter the username of the recipient: ')
        message = input('Please enter your message: ')
        self.client.send_message(friends_username, message)

    def add_friend(self):
        friends_username = input('please enter the username of your friend: ')
        friends_name = input('please enter the name of your friend: ')
        self.client.add_friend(friends_username, friends_name)

    def delete_friend(self):
        friends_username = input('please enter the username of the friend you want to delete: ')
        self.client.delete_friend(friends_username)

    # Callback functions that will be called by the Client upon incoming messages from the Server:
    @staticmethod
    def on_fail():
        print('Sorry, there has been a problem. Please restart the program.')
        sys.exit()

    @staticmethod
    def on_new_message(msg):
        print(f'{msg.sender}: {msg.text}')

    @staticmethod
    def on_friends_list(msg):
        print('Your friends are:\n')
        for friend in msg.friends:
            print(friend)

    @staticmethod
    def on_is_friend(msg):
        print(f'{msg.username_friend} is already your friend.')

    @staticmethod
    def on_friend_added(msg):
        print(f'Your friend {msg.username_friend} has been added')

    @staticmethod
    def on_not_a_friend(msg):
        print(f'Sorry, {msg.username_friend} is not your friend.')

    @staticmethod
    def on_friend_deleted(msg):
        print(f'{msg.username_friend} has been deleted from your friends-list.')

    @staticmethod
    def on_friend_is_not_a_user(msg):
        print(f"Sorry, {msg.username_friend} is not a user and couldn’t be added.")

    def on_connection_closed(self):
        self.request_thread.join()
        print('The connection has been closed.')
        sys.exit()

    def on_sign_up_success(self):
        print('You are now signed up!')
        self.request_thread.start()

    def on_sign_up_failed_occupied_username(self):
        print('This username is already in use.')
        self.login_or_signup()

    def on_login_success(self):
        print('You are now logged in!')
        self.request_thread.start()

    def on_login_failed_not_a_user(self):
        print('This is not a registered name or username.')
        self.login_or_signup()

    def on_login_failed_already_logged_in(self):
        print('You are already logged in on an other device.')
        self.login_or_signup()


if __name__ == '__main__':
    TerminalUI()