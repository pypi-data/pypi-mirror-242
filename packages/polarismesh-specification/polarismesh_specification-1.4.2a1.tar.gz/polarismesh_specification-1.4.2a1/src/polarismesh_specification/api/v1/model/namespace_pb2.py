# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: namespace.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fnamespace.proto\x12\x02v1\x1a\x1egoogle/protobuf/wrappers.proto\"\xc9\x07\n\tNamespace\x12*\n\x04name\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12-\n\x07\x63omment\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12,\n\x06owners\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12+\n\x05token\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12+\n\x05\x63time\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12+\n\x05mtime\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12N\n\x13total_service_count\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueR\x13total_service_count\x12^\n\x1btotal_health_instance_count\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueR\x1btotal_health_instance_count\x12P\n\x14total_instance_count\x18\t \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueR\x14total_instance_count\x12\x38\n\x08user_ids\x18\n \x03(\x0b\x32\x1c.google.protobuf.StringValueR\x08user_ids\x12:\n\tgroup_ids\x18\x0b \x03(\x0b\x32\x1c.google.protobuf.StringValueR\tgroup_ids\x12\x46\n\x0fremove_user_ids\x18\r \x03(\x0b\x32\x1c.google.protobuf.StringValueR\x0fremove_user_ids\x12H\n\x10remove_group_ids\x18\x0e \x03(\x0b\x32\x1c.google.protobuf.StringValueR\x10remove_group_ids\x12(\n\x02id\x18\x0c \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12,\n\x08\x65\x64itable\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12J\n\x11service_export_to\x18\x10 \x03(\x0b\x32\x1c.google.protobuf.StringValueR\x11service_export_toB}\n.com.tencent.polaris.specification.api.v1.modelB\x0eNamespaceProtoZ;github.com/polarismesh/specification/source/go/api/v1/modelb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'namespace_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n.com.tencent.polaris.specification.api.v1.modelB\016NamespaceProtoZ;github.com/polarismesh/specification/source/go/api/v1/model'
  _globals['_NAMESPACE']._serialized_start=56
  _globals['_NAMESPACE']._serialized_end=1025
# @@protoc_insertion_point(module_scope)
