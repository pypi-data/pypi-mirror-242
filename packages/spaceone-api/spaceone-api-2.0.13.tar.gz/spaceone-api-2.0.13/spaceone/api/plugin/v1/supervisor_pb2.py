# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/plugin/v1/supervisor.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'spaceone/api/plugin/v1/supervisor.proto\x12\x16spaceone.api.plugin.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\xfd\x01\n\x18PublishSupervisorRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08hostname\x18\x02 \x01(\t\x12\x12\n\nsecret_key\x18\x03 \x01(\t\x12\x37\n\x0bplugin_info\x18\x04 \x03(\x0b\x32\".spaceone.api.plugin.v1.PluginInfo\x12%\n\x04tags\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tis_public\x18\x06 \x01(\x08\x12\x11\n\tdomain_id\x18\x07 \x01(\t\x12\'\n\x06labels\x18\x08 \x01(\x0b\x32\x17.google.protobuf.Struct\"\xc8\x01\n\x19RegisterSupervisorRequest\x12\x15\n\rsupervisor_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tis_public\x18\x03 \x01(\x08\x12\x10\n\x08priority\x18\x04 \x01(\x05\x12\'\n\x06labels\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x07 \x01(\t\"=\n\x11SupervisorRequest\x12\x15\n\rsupervisor_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"N\n\x14GetSupervisorRequest\x12\x15\n\rsupervisor_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"d\n\x14RecoverPluginRequest\x12\x15\n\rsupervisor_id\x18\x01 \x01(\t\x12\x11\n\tplugin_id\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x11\n\tdomain_id\x18\x04 \x01(\t\"\xef\x02\n\x0eSupervisorInfo\x12\x15\n\rsupervisor_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08hostname\x18\x03 \x01(\t\x12;\n\x05state\x18\x04 \x01(\x0e\x32,.spaceone.api.plugin.v1.SupervisorInfo.State\x12\x11\n\tis_public\x18\x05 \x01(\x08\x12\x11\n\tdomain_id\x18\x07 \x01(\t\x12%\n\x04tags\x18\x08 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\'\n\x06labels\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x12\n\ncreated_at\x18\n \x01(\t\x12\x12\n\nupdated_at\x18\x0b \x01(\t\"K\n\x05State\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\x12\x0b\n\x07PENDING\x10\x03\x12\x10\n\x0c\x44ISCONNECTED\x10\x04\"\x88\x01\n\x0fSupervisorQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x15\n\rsupervisor_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x11\n\tis_public\x18\x04 \x01(\x08\x12\x11\n\tdomain_id\x18\x05 \x01(\t\"_\n\x0fSupervisorsInfo\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32&.spaceone.api.plugin.v1.SupervisorInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"^\n\x13SupervisorStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"\xb6\x02\n\x0bPluginQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x15\n\rsupervisor_id\x18\x02 \x01(\t\x12\x10\n\x08hostname\x18\x03 \x01(\t\x12\x11\n\tplugin_id\x18\x04 \x01(\t\x12\x0f\n\x07version\x18\x05 \x01(\t\x12\x38\n\x05state\x18\x06 \x01(\x0e\x32).spaceone.api.plugin.v1.PluginQuery.State\x12\x10\n\x08\x65ndpoint\x18\x07 \x01(\t\x12\x11\n\tdomain_id\x18\x08 \x01(\t\"O\n\x05State\x12\x08\n\x04NONE\x10\x00\x12\x10\n\x0cPROVISIONING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02\x12\x13\n\x0fRE_PROVISIONING\x10\x03\x12\t\n\x05\x45RROR\x10\x04\"\xb3\x02\n\nPluginInfo\x12\x11\n\tplugin_id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x37\n\x05state\x18\x03 \x01(\x0e\x32(.spaceone.api.plugin.v1.PluginInfo.State\x12\x10\n\x08\x65ndpoint\x18\x04 \x01(\t\x12\x15\n\rsupervisor_id\x18\x05 \x01(\t\x12\x17\n\x0fsupervisor_name\x18\x06 \x01(\t\x12\x0f\n\x07managed\x18\x07 \x01(\x08\x12\x11\n\tendpoints\x18\x08 \x03(\t\x12\x11\n\tdomain_id\x18\t \x01(\t\"O\n\x05State\x12\x08\n\x04NONE\x10\x00\x12\x10\n\x0cPROVISIONING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02\x12\x13\n\x0fRE_PROVISIONING\x10\x03\x12\t\n\x05\x45RROR\x10\x04\"W\n\x0bPluginsInfo\x12\x33\n\x07results\x18\x01 \x03(\x0b\x32\".spaceone.api.plugin.v1.PluginInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x32\xe6\x0b\n\nSupervisor\x12\x8d\x01\n\x07publish\x12\x30.spaceone.api.plugin.v1.PublishSupervisorRequest\x1a&.spaceone.api.plugin.v1.SupervisorInfo\"(\x82\xd3\xe4\x93\x02\"\"\x1d/plugin/v1/supervisor/publish:\x01*\x12\x90\x01\n\x08register\x12\x31.spaceone.api.plugin.v1.RegisterSupervisorRequest\x1a&.spaceone.api.plugin.v1.SupervisorInfo\")\x82\xd3\xe4\x93\x02#\"\x1e/plugin/v1/supervisor/register:\x01*\x12\x8c\x01\n\x06update\x12\x31.spaceone.api.plugin.v1.RegisterSupervisorRequest\x1a&.spaceone.api.plugin.v1.SupervisorInfo\"\'\x82\xd3\xe4\x93\x02!\"\x1c/plugin/v1/supervisor/update:\x01*\x12|\n\nderegister\x12).spaceone.api.plugin.v1.SupervisorRequest\x1a\x16.google.protobuf.Empty\"+\x82\xd3\xe4\x93\x02%\" /plugin/v1/supervisor/deregister:\x01*\x12\x84\x01\n\x06\x65nable\x12).spaceone.api.plugin.v1.SupervisorRequest\x1a&.spaceone.api.plugin.v1.SupervisorInfo\"\'\x82\xd3\xe4\x93\x02!\"\x1c/plugin/v1/supervisor/enable:\x01*\x12\x86\x01\n\x07\x64isable\x12).spaceone.api.plugin.v1.SupervisorRequest\x1a&.spaceone.api.plugin.v1.SupervisorInfo\"(\x82\xd3\xe4\x93\x02\"\"\x1d/plugin/v1/supervisor/disable:\x01*\x12\x93\x01\n\x0erecover_plugin\x12,.spaceone.api.plugin.v1.RecoverPluginRequest\x1a\".spaceone.api.plugin.v1.PluginInfo\"/\x82\xd3\xe4\x93\x02)\"$/plugin/v1/supervisor/recover-plugin:\x01*\x12\x81\x01\n\x03get\x12,.spaceone.api.plugin.v1.GetSupervisorRequest\x1a&.spaceone.api.plugin.v1.SupervisorInfo\"$\x82\xd3\xe4\x93\x02\x1e\"\x19/plugin/v1/supervisor/get:\x01*\x12\x7f\n\x04list\x12\'.spaceone.api.plugin.v1.SupervisorQuery\x1a\'.spaceone.api.plugin.v1.SupervisorsInfo\"%\x82\xd3\xe4\x93\x02\x1f\"\x1a/plugin/v1/supervisor/list:\x01*\x12s\n\x04stat\x12+.spaceone.api.plugin.v1.SupervisorStatQuery\x1a\x17.google.protobuf.Struct\"%\x82\xd3\xe4\x93\x02\x1f\"\x1a/plugin/v1/supervisor/stat:\x01*\x12\x87\x01\n\x0clist_plugins\x12#.spaceone.api.plugin.v1.PluginQuery\x1a#.spaceone.api.plugin.v1.PluginsInfo\"-\x82\xd3\xe4\x93\x02\'\"\"/plugin/v1/supervisor/list-plugins:\x01*B=Z;github.com/cloudforet-io/api/dist/go/spaceone/api/plugin/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.plugin.v1.supervisor_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z;github.com/cloudforet-io/api/dist/go/spaceone/api/plugin/v1'
  _SUPERVISOR.methods_by_name['publish']._options = None
  _SUPERVISOR.methods_by_name['publish']._serialized_options = b'\202\323\344\223\002\"\"\035/plugin/v1/supervisor/publish:\001*'
  _SUPERVISOR.methods_by_name['register']._options = None
  _SUPERVISOR.methods_by_name['register']._serialized_options = b'\202\323\344\223\002#\"\036/plugin/v1/supervisor/register:\001*'
  _SUPERVISOR.methods_by_name['update']._options = None
  _SUPERVISOR.methods_by_name['update']._serialized_options = b'\202\323\344\223\002!\"\034/plugin/v1/supervisor/update:\001*'
  _SUPERVISOR.methods_by_name['deregister']._options = None
  _SUPERVISOR.methods_by_name['deregister']._serialized_options = b'\202\323\344\223\002%\" /plugin/v1/supervisor/deregister:\001*'
  _SUPERVISOR.methods_by_name['enable']._options = None
  _SUPERVISOR.methods_by_name['enable']._serialized_options = b'\202\323\344\223\002!\"\034/plugin/v1/supervisor/enable:\001*'
  _SUPERVISOR.methods_by_name['disable']._options = None
  _SUPERVISOR.methods_by_name['disable']._serialized_options = b'\202\323\344\223\002\"\"\035/plugin/v1/supervisor/disable:\001*'
  _SUPERVISOR.methods_by_name['recover_plugin']._options = None
  _SUPERVISOR.methods_by_name['recover_plugin']._serialized_options = b'\202\323\344\223\002)\"$/plugin/v1/supervisor/recover-plugin:\001*'
  _SUPERVISOR.methods_by_name['get']._options = None
  _SUPERVISOR.methods_by_name['get']._serialized_options = b'\202\323\344\223\002\036\"\031/plugin/v1/supervisor/get:\001*'
  _SUPERVISOR.methods_by_name['list']._options = None
  _SUPERVISOR.methods_by_name['list']._serialized_options = b'\202\323\344\223\002\037\"\032/plugin/v1/supervisor/list:\001*'
  _SUPERVISOR.methods_by_name['stat']._options = None
  _SUPERVISOR.methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\037\"\032/plugin/v1/supervisor/stat:\001*'
  _SUPERVISOR.methods_by_name['list_plugins']._options = None
  _SUPERVISOR.methods_by_name['list_plugins']._serialized_options = b'\202\323\344\223\002\'\"\"/plugin/v1/supervisor/list-plugins:\001*'
  _globals['_PUBLISHSUPERVISORREQUEST']._serialized_start=191
  _globals['_PUBLISHSUPERVISORREQUEST']._serialized_end=444
  _globals['_REGISTERSUPERVISORREQUEST']._serialized_start=447
  _globals['_REGISTERSUPERVISORREQUEST']._serialized_end=647
  _globals['_SUPERVISORREQUEST']._serialized_start=649
  _globals['_SUPERVISORREQUEST']._serialized_end=710
  _globals['_GETSUPERVISORREQUEST']._serialized_start=712
  _globals['_GETSUPERVISORREQUEST']._serialized_end=790
  _globals['_RECOVERPLUGINREQUEST']._serialized_start=792
  _globals['_RECOVERPLUGINREQUEST']._serialized_end=892
  _globals['_SUPERVISORINFO']._serialized_start=895
  _globals['_SUPERVISORINFO']._serialized_end=1262
  _globals['_SUPERVISORINFO_STATE']._serialized_start=1187
  _globals['_SUPERVISORINFO_STATE']._serialized_end=1262
  _globals['_SUPERVISORQUERY']._serialized_start=1265
  _globals['_SUPERVISORQUERY']._serialized_end=1401
  _globals['_SUPERVISORSINFO']._serialized_start=1403
  _globals['_SUPERVISORSINFO']._serialized_end=1498
  _globals['_SUPERVISORSTATQUERY']._serialized_start=1500
  _globals['_SUPERVISORSTATQUERY']._serialized_end=1594
  _globals['_PLUGINQUERY']._serialized_start=1597
  _globals['_PLUGINQUERY']._serialized_end=1907
  _globals['_PLUGINQUERY_STATE']._serialized_start=1828
  _globals['_PLUGINQUERY_STATE']._serialized_end=1907
  _globals['_PLUGININFO']._serialized_start=1910
  _globals['_PLUGININFO']._serialized_end=2217
  _globals['_PLUGININFO_STATE']._serialized_start=1828
  _globals['_PLUGININFO_STATE']._serialized_end=1907
  _globals['_PLUGINSINFO']._serialized_start=2219
  _globals['_PLUGINSINFO']._serialized_end=2306
  _globals['_SUPERVISOR']._serialized_start=2309
  _globals['_SUPERVISOR']._serialized_end=3819
# @@protoc_insertion_point(module_scope)
