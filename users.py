# The following functions serve to interact with the sqlite3 database 'users.db'.
# 'users.db' is initialized in server.py and maintained within the server class in server.py.
# 'users.db' stores the information about users of this chat application.
# The database stores the users in one table and the pending messages for users in a separate table for each user.

import sqlite3


class Database:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name

    def set_up_database(self):
        self.create_table('users', 'username text, first_name text')

    def add_user(self, username, name):
        self.add_to_table('users', (username, name))
        # table of users friends
        self.create_table(username, 'friends_username text, friends_name text')
        # table of pending messages for user
        # todo: rename table from 'username + _m' to 'username + pending_messages' or something else more descriptive
        self.create_table(username + '_m', 'friends_username text, message text')

    def is_user(self, username, first_name):
        # todo: as usernames are unique the second condition is obsolete
        return self.is_in_table('users', 'username', username) and self.is_in_table('users', 'first_name', first_name)

    def add_pending_message(self, recipient_username, sender_username, message):
        # todo: rename to 'username + pending_messages' or something else more descriptive
        self.add_to_table(recipient_username + '_m', (sender_username, message))

    def retrieve_pending_messages(self, username):
        # todo: replace logic with context-manager ('with db: )
        db = sqlite3.connect(self.db_name)
        c = db.cursor()
        # todo: rename to 'username + pending_messages' or something else more descriptive
        c.execute(f"select * from {username + '_m'};")
        result = c.fetchall()
        # todo: rename to 'username + pending_messages' or something else more descriptive
        c.execute(f"delete from {username + '_m'};")
        db.commit()
        db.close()
        return result

    def add_friend(self, username, username_friend, name_friend):
        self.add_to_table(username, (username_friend, name_friend))

    def is_friend(self, username, username_friend):
        return self.is_in_table(username, 'friends_username', username_friend)

    def list_friends(self, username):
        # todo: replace logic with context-manager ('with db: )
        db = sqlite3.connect(self.db_name)
        c = db.cursor()
        c.execute(f"select * from {username};")
        result = c.fetchall()
        db.close()
        return result

    def delete_friend(self, username, friend):
        self.delete_from_table(username, friend)

    def create_table(self, table_name, columns):
        # todo: replace logic with context-manager ('with db: )
        db = sqlite3.connect(self.db_name)
        c = db.cursor()
        c.execute(f'create table {table_name} ({columns})')
        db.commit()
        db.close()

    def add_to_table(self, table, values):
        # todo: replace logic with context-manager ('with db: )
        db = sqlite3.connect(self.db_name)
        c = db.cursor()
        c.execute(f"insert into {table} values {values}")
        db.commit()
        db.close()

    def is_in_table(self, table, column, element):
        # todo: replace logic with context-manager ('with db: )
        db = sqlite3.connect(self.db_name)
        c = db.cursor()
        c.execute(f"select count(*) from {table} where {column} = '{element}';")
        result = c.fetchall()[0][0]
        db.close()
        return result

    def delete_from_table(self, table, username):
        # todo: replace logic with context-manager ('with db: )
        db = sqlite3.connect(self.db_name)
        c = db.cursor()
        c.execute(f"delete from {table} where friends_username = '{username}'")
        db.commit()
        db.close()
