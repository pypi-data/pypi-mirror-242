# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/statistics/plugin/storage.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,spaceone/api/statistics/plugin/storage.proto\x12\x1dspaceone.api.inventory.plugin\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\"7\n\x0bInitRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"w\n\rVerifyRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0e\n\x06schema\x18\x02 \x01(\t\x12,\n\x0bsecret_data\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x9e\x01\n\rExportRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0e\n\x06schema\x18\x02 \x01(\t\x12,\n\x0bsecret_data\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04\x64\x61ta\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\"7\n\nPluginInfo\x12)\n\x08metadata\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct2\x8e\x02\n\x07Storage\x12_\n\x04init\x12*.spaceone.api.inventory.plugin.InitRequest\x1a).spaceone.api.inventory.plugin.PluginInfo\"\x00\x12P\n\x06verify\x12,.spaceone.api.inventory.plugin.VerifyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12P\n\x06\x65xport\x12,.spaceone.api.inventory.plugin.ExportRequest\x1a\x16.google.protobuf.Empty\"\x00\x42\x45ZCgithub.com/cloudforet-io/api/dist/go/spaceone/api/statistics/pluginb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.statistics.plugin.storage_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZCgithub.com/cloudforet-io/api/dist/go/spaceone/api/statistics/plugin'
  _globals['_INITREQUEST']._serialized_start=138
  _globals['_INITREQUEST']._serialized_end=193
  _globals['_VERIFYREQUEST']._serialized_start=195
  _globals['_VERIFYREQUEST']._serialized_end=314
  _globals['_EXPORTREQUEST']._serialized_start=317
  _globals['_EXPORTREQUEST']._serialized_end=475
  _globals['_PLUGININFO']._serialized_start=477
  _globals['_PLUGININFO']._serialized_end=532
  _globals['_STORAGE']._serialized_start=535
  _globals['_STORAGE']._serialized_end=805
# @@protoc_insertion_point(module_scope)
