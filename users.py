# The following functions serve to interact with the sqlite3 database 'users.db'.
# 'users.db' is initialized in server.py and maintained within the server class in server.py.
# 'users.db' stores the information about users of this chat application.
# The database stores the users in one table and the pending messages for users in a separate table for each user.

import sqlite3


def set_up_database():
    create_table('users', 'username text, first_name text')


def add_user(username, name):
    add_to_table('users', (username, name))
    # table of users friends
    create_table(username, 'friends_username text, friends_name text')
    # table of pending messages for user
    # todo: rename table from 'username + _m' to 'username + pending_messages' or something else more descriptive
    create_table(username + '_m', 'friends_username text, message text')


def is_user(username, first_name):
    # todo: as usernames are unique the second condition is obsolete
    return is_in_table('users', 'username', username) and is_in_table('users', 'first_name', first_name)


def add_pending_message(recipient_username, sender_username, message):
    # todo: rename to 'username + pending_messages' or something else more descriptive
    add_to_table(recipient_username + '_m', (sender_username, message))


def retrieve_pending_messages(username):
    # todo: replace logic with context-manager ('with db: )
    db = sqlite3.connect('users.db')
    c = db.cursor()
    # todo: rename to 'username + pending_messages' or something else more descriptive
    c.execute(f"select * from {username + '_m'};")
    result = c.fetchall()
    # todo: rename to 'username + pending_messages' or something else more descriptive
    c.execute(f"delete from {username + '_m'};")
    db.commit()
    db.close()
    return result


def add_friend(username, username_friend, name_friend):
    add_to_table(username, (username_friend, name_friend))


def is_friend(username, username_friend):
    return is_in_table(username, 'friends_username', username_friend)


def list_friends(username):
    # todo: replace logic with context-manager ('with db: )
    db = sqlite3.connect('users.db')
    c = db.cursor()
    query = f"select * from {username};"
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def delete_friend(username, friend):
    delete_from_table(username, friend)


def create_table(table_name, columns):
    # todo: replace logic with context-manager ('with db: )
    db = sqlite3.connect('users.db')
    c = db.cursor()
    c.execute(f'create table {table_name} ({columns})')
    db.commit()
    db.close()


def add_to_table(table, values):
    # todo: replace logic with context-manager ('with db: )
    db = sqlite3.connect('users.db')
    c = db.cursor()
    query = f"insert into {table} values {values}"
    c.execute(query)
    db.commit()
    db.close()


def is_in_table(table, column, element):
    # todo: replace logic with context-manager ('with db: )
    db = sqlite3.connect('users.db')
    c = db.cursor()
    query = f"select count(*) from {table} where {column} = '{element}';"
    c.execute(query)
    result = c.fetchall()[0][0]
    db.close()
    return result


def delete_from_table(table, username):
    # todo: replace logic with context-manager ('with db: )
    db = sqlite3.connect('users.db')
    c = db.cursor()
    query = f"delete from {table} where friends_username = '{username}'"
    c.execute(query)
    db.commit()
    db.close()
