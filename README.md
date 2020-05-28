# This project is in progress

This is a simple client-server chat application. The user can currently access the chat via a terminal-UI. I will also implement a PyQt-UI in the future. The client and the server use protobuf messages to communicate with each other. The server stores users, their friends and pending messages (messages received when recipient was not connected) in a Sqlite3 database.

Technologies used:
- Python3
- Sqlite3
- Protobuf

In progess:
- write unittests for Server

To do:
- write unittests for Client
- test and fix bugs
- create UI with PyQt
