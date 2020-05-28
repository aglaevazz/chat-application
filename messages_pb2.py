# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x0emessages.proto\"\x80\x01\n\x11MessageFromClient\x12\x0f\n\x07request\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x17\n\x0fusername_friend\x18\x04 \x01(\t\x12\x13\n\x0bname_friend\x18\x05 \x01(\t\x12\x0c\n\x04text\x18\x06 \x01(\t\"(\n\x06\x46riend\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"u\n\x11MessageFromServer\x12\x0f\n\x07subject\x18\x01 \x01(\t\x12\x0e\n\x06sender\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\x17\n\x0fusername_friend\x18\x04 \x01(\t\x12\x18\n\x07\x66riends\x18\x05 \x03(\x0b\x32\x07.Friendb\x06proto3'
)




_MESSAGEFROMCLIENT = _descriptor.Descriptor(
  name='MessageFromClient',
  full_name='MessageFromClient',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request', full_name='MessageFromClient.request', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='username', full_name='MessageFromClient.username', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='MessageFromClient.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='username_friend', full_name='MessageFromClient.username_friend', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name_friend', full_name='MessageFromClient.name_friend', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='text', full_name='MessageFromClient.text', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=147,
)


_FRIEND = _descriptor.Descriptor(
  name='Friend',
  full_name='Friend',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='Friend.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='Friend.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=149,
  serialized_end=189,
)


_MESSAGEFROMSERVER = _descriptor.Descriptor(
  name='MessageFromServer',
  full_name='MessageFromServer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='subject', full_name='MessageFromServer.subject', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sender', full_name='MessageFromServer.sender', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='text', full_name='MessageFromServer.text', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='username_friend', full_name='MessageFromServer.username_friend', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='friends', full_name='MessageFromServer.friends', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=191,
  serialized_end=308,
)

_MESSAGEFROMSERVER.fields_by_name['friends'].message_type = _FRIEND
DESCRIPTOR.message_types_by_name['MessageFromClient'] = _MESSAGEFROMCLIENT
DESCRIPTOR.message_types_by_name['Friend'] = _FRIEND
DESCRIPTOR.message_types_by_name['MessageFromServer'] = _MESSAGEFROMSERVER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MessageFromClient = _reflection.GeneratedProtocolMessageType('MessageFromClient', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGEFROMCLIENT,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:MessageFromClient)
  })
_sym_db.RegisterMessage(MessageFromClient)

Friend = _reflection.GeneratedProtocolMessageType('Friend', (_message.Message,), {
  'DESCRIPTOR' : _FRIEND,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:Friend)
  })
_sym_db.RegisterMessage(Friend)

MessageFromServer = _reflection.GeneratedProtocolMessageType('MessageFromServer', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGEFROMSERVER,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:MessageFromServer)
  })
_sym_db.RegisterMessage(MessageFromServer)


# @@protoc_insertion_point(module_scope)
