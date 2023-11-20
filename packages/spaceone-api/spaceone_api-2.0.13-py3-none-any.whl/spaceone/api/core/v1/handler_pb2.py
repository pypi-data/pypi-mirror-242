# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/core/v1/handler.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"spaceone/api/core/v1/handler.proto\x12\x14spaceone.api.core.v1\x1a\x1cgoogle/protobuf/struct.proto\"\xc7\x03\n\x14\x41uthorizationRequest\x12\x0f\n\x07service\x18\x01 \x01(\t\x12\x10\n\x08resource\x18\x02 \x01(\t\x12\x0c\n\x04verb\x18\x03 \x01(\t\x12?\n\x05scope\x18\x04 \x01(\x0e\x32\x30.spaceone.api.core.v1.AuthorizationRequest.Scope\x12\x11\n\tdomain_id\x18\x05 \x01(\t\x12\x12\n\nproject_id\x18\x06 \x01(\t\x12\x18\n\x10project_group_id\x18\x07 \x01(\t\x12\x0f\n\x07user_id\x18\x08 \x01(\t\x12\x1a\n\x12require_project_id\x18\t \x01(\x08\x12 \n\x18require_project_group_id\x18\n \x01(\x08\x12\x17\n\x0frequire_user_id\x18\x0b \x01(\x08\x12\x19\n\x11require_domain_id\x18\x0c \x01(\x08\"y\n\x05Scope\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06SYSTEM\x10\x01\x12\n\n\x06\x44OMAIN\x10\x02\x12\x0b\n\x07PROJECT\x10\x03\x12\x08\n\x04USER\x10\x04\x12\n\n\x06PUBLIC\x10\x05\x12\x14\n\x10PUBLIC_OR_DOMAIN\x10\x06\x12\x15\n\x11\x44OMAIN_OR_PROJECT\x10\x07\"T\n\x15\x41uthorizationResponse\x12\x11\n\trole_type\x18\x01 \x01(\t\x12\x10\n\x08projects\x18\x02 \x03(\t\x12\x16\n\x0eproject_groups\x18\x03 \x03(\t\"*\n\x15\x41uthenticationRequest\x12\x11\n\tdomain_id\x18\x01 \x01(\t\"?\n\x16\x41uthenticationResponse\x12\x11\n\tdomain_id\x18\x01 \x01(\t\x12\x12\n\npublic_key\x18\x02 \x01(\t\"y\n\x0c\x45ventRequest\x12\x0f\n\x07service\x18\x01 \x01(\t\x12\x10\n\x08resource\x18\x02 \x01(\t\x12\x0c\n\x04verb\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\x12(\n\x07message\x18\x05 \x01(\x0b\x32\x17.google.protobuf.StructB;Z9github.com/cloudforet-io/api/dist/go/spaceone/api/core/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.core.v1.handler_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z9github.com/cloudforet-io/api/dist/go/spaceone/api/core/v1'
  _globals['_AUTHORIZATIONREQUEST']._serialized_start=91
  _globals['_AUTHORIZATIONREQUEST']._serialized_end=546
  _globals['_AUTHORIZATIONREQUEST_SCOPE']._serialized_start=425
  _globals['_AUTHORIZATIONREQUEST_SCOPE']._serialized_end=546
  _globals['_AUTHORIZATIONRESPONSE']._serialized_start=548
  _globals['_AUTHORIZATIONRESPONSE']._serialized_end=632
  _globals['_AUTHENTICATIONREQUEST']._serialized_start=634
  _globals['_AUTHENTICATIONREQUEST']._serialized_end=676
  _globals['_AUTHENTICATIONRESPONSE']._serialized_start=678
  _globals['_AUTHENTICATIONRESPONSE']._serialized_end=741
  _globals['_EVENTREQUEST']._serialized_start=743
  _globals['_EVENTREQUEST']._serialized_end=864
# @@protoc_insertion_point(module_scope)
