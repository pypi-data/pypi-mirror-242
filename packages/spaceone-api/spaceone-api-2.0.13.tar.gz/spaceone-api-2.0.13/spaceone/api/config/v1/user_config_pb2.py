# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/config/v1/user_config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(spaceone/api/config/v1/user_config.proto\x12\x16spaceone.api.config.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\x85\x01\n\x14SetUserConfigRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12%\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x04 \x01(\t\"4\n\x11UserConfigRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"E\n\x14GetUserConfigRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"o\n\x0fUserConfigQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07user_id\x18\x03 \x01(\t\x12\x11\n\tdomain_id\x18\x04 \x01(\t\"\xb8\x01\n\x0eUserConfigInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12%\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0f\n\x07user_id\x18\x04 \x01(\t\x12\x11\n\tdomain_id\x18\x05 \x01(\t\x12\x12\n\ncreated_at\x18\x06 \x01(\t\x12\x12\n\nupdated_at\x18\x07 \x01(\t\"_\n\x0fUserConfigsInfo\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32&.spaceone.api.config.v1.UserConfigInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"^\n\x13UserConfigStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\x9c\x07\n\nUserConfig\x12\x88\x01\n\x06\x63reate\x12,.spaceone.api.config.v1.SetUserConfigRequest\x1a&.spaceone.api.config.v1.UserConfigInfo\"(\x82\xd3\xe4\x93\x02\"\"\x1d/config/v1/user-config/create:\x01*\x12\x88\x01\n\x06update\x12,.spaceone.api.config.v1.SetUserConfigRequest\x1a&.spaceone.api.config.v1.UserConfigInfo\"(\x82\xd3\xe4\x93\x02\"\"\x1d/config/v1/user-config/update:\x01*\x12\x82\x01\n\x03set\x12,.spaceone.api.config.v1.SetUserConfigRequest\x1a&.spaceone.api.config.v1.UserConfigInfo\"%\x82\xd3\xe4\x93\x02\x1f\"\x1a/config/v1/user-config/set:\x01*\x12u\n\x06\x64\x65lete\x12).spaceone.api.config.v1.UserConfigRequest\x1a\x16.google.protobuf.Empty\"(\x82\xd3\xe4\x93\x02\"\"\x1d/config/v1/user-config/delete:\x01*\x12\x82\x01\n\x03get\x12,.spaceone.api.config.v1.GetUserConfigRequest\x1a&.spaceone.api.config.v1.UserConfigInfo\"%\x82\xd3\xe4\x93\x02\x1f\"\x1a/config/v1/user-config/get:\x01*\x12\x80\x01\n\x04list\x12\'.spaceone.api.config.v1.UserConfigQuery\x1a\'.spaceone.api.config.v1.UserConfigsInfo\"&\x82\xd3\xe4\x93\x02 \"\x1b/config/v1/user-config/list:\x01*\x12t\n\x04stat\x12+.spaceone.api.config.v1.UserConfigStatQuery\x1a\x17.google.protobuf.Struct\"&\x82\xd3\xe4\x93\x02 \"\x1b/config/v1/user-config/stat:\x01*B=Z;github.com/cloudforet-io/api/dist/go/spaceone/api/config/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.config.v1.user_config_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z;github.com/cloudforet-io/api/dist/go/spaceone/api/config/v1'
  _USERCONFIG.methods_by_name['create']._options = None
  _USERCONFIG.methods_by_name['create']._serialized_options = b'\202\323\344\223\002\"\"\035/config/v1/user-config/create:\001*'
  _USERCONFIG.methods_by_name['update']._options = None
  _USERCONFIG.methods_by_name['update']._serialized_options = b'\202\323\344\223\002\"\"\035/config/v1/user-config/update:\001*'
  _USERCONFIG.methods_by_name['set']._options = None
  _USERCONFIG.methods_by_name['set']._serialized_options = b'\202\323\344\223\002\037\"\032/config/v1/user-config/set:\001*'
  _USERCONFIG.methods_by_name['delete']._options = None
  _USERCONFIG.methods_by_name['delete']._serialized_options = b'\202\323\344\223\002\"\"\035/config/v1/user-config/delete:\001*'
  _USERCONFIG.methods_by_name['get']._options = None
  _USERCONFIG.methods_by_name['get']._serialized_options = b'\202\323\344\223\002\037\"\032/config/v1/user-config/get:\001*'
  _USERCONFIG.methods_by_name['list']._options = None
  _USERCONFIG.methods_by_name['list']._serialized_options = b'\202\323\344\223\002 \"\033/config/v1/user-config/list:\001*'
  _USERCONFIG.methods_by_name['stat']._options = None
  _USERCONFIG.methods_by_name['stat']._serialized_options = b'\202\323\344\223\002 \"\033/config/v1/user-config/stat:\001*'
  _globals['_SETUSERCONFIGREQUEST']._serialized_start=192
  _globals['_SETUSERCONFIGREQUEST']._serialized_end=325
  _globals['_USERCONFIGREQUEST']._serialized_start=327
  _globals['_USERCONFIGREQUEST']._serialized_end=379
  _globals['_GETUSERCONFIGREQUEST']._serialized_start=381
  _globals['_GETUSERCONFIGREQUEST']._serialized_end=450
  _globals['_USERCONFIGQUERY']._serialized_start=452
  _globals['_USERCONFIGQUERY']._serialized_end=563
  _globals['_USERCONFIGINFO']._serialized_start=566
  _globals['_USERCONFIGINFO']._serialized_end=750
  _globals['_USERCONFIGSINFO']._serialized_start=752
  _globals['_USERCONFIGSINFO']._serialized_end=847
  _globals['_USERCONFIGSTATQUERY']._serialized_start=849
  _globals['_USERCONFIGSTATQUERY']._serialized_end=943
  _globals['_USERCONFIG']._serialized_start=946
  _globals['_USERCONFIG']._serialized_end=1870
# @@protoc_insertion_point(module_scope)
