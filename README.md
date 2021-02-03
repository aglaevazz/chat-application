# This project is in progress

This is a multi-platform client-server chat application. The client and the server use protobuf messages to communicate language-independently. The server connects to an SQLite database that stores user-information and pending messages (messages received when the recipient was not connected). The user can currently access the chat via a terminal-UI. I will also implement a UI with Java using Swing in the future.

Technologies used:
- Python3
- Sqlite3
- Protobuf3

In progess:
- write unit tests for server

To do:
- write unit tests for client
- optimize code (see todos in code)
- create UI with Java using Swing
