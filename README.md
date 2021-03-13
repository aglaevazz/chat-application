# This project is in progress

This is a multi-platform client-server chat application. The client and the server use protobuf messages to communicate language-independently. The server connects to an SQLite database that stores user-information and pending messages (messages received when the recipient was not connected). The user can currently access the chat via a terminal-UI. I will also implement a UI with Java using Swing in the future.

Technologies used:
- Python3
- Sqlite3
- Protobuf3

To do:
- users.py: wrap functions in class
- unit tests for Server, Client and users.db
- optimize code (todo's in code)
- write Java-Client and create UI with Java using Swing
