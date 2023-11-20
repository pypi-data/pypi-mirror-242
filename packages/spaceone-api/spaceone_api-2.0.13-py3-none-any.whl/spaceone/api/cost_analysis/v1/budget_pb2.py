# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/cost_analysis/v1/budget.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*spaceone/api/cost_analysis/v1/budget.proto\x12\x1dspaceone.api.cost_analysis.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"+\n\x0cPlannedLimit\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\r\n\x05limit\x18\x02 \x01(\x02\"\xcc\x02\n\x12\x42udgetNotification\x12\x11\n\tthreshold\x18\x01 \x01(\x02\x12\x44\n\x04unit\x18\x02 \x01(\x0e\x32\x36.spaceone.api.cost_analysis.v1.BudgetNotification.Unit\x12]\n\x11notification_type\x18\x03 \x01(\x0e\x32\x42.spaceone.api.cost_analysis.v1.BudgetNotification.NotificationType\"3\n\x04Unit\x12\r\n\tUNIT_NONE\x10\x00\x12\x0b\n\x07PERCENT\x10\x01\x12\x0f\n\x0b\x41\x43TUAL_COST\x10\x02\"I\n\x10NotificationType\x12\x1a\n\x16NOTIFICATION_TYPE_NONE\x10\x00\x12\x0c\n\x08\x43RITICAL\x10\x01\x12\x0b\n\x07WARNING\x10\x02\"\x9b\x01\n\x0eProviderFilter\x12\x42\n\x05state\x18\x01 \x01(\x0e\x32\x33.spaceone.api.cost_analysis.v1.ProviderFilter.State\x12\x11\n\tproviders\x18\x02 \x03(\t\"2\n\x05State\x12\x0e\n\nSTATE_NONE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\"\xa3\x04\n\x13\x43reateBudgetRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05limit\x18\x02 \x01(\x02\x12\x43\n\x0eplanned_limits\x18\x03 \x03(\x0b\x32+.spaceone.api.cost_analysis.v1.PlannedLimit\x12\x46\n\x0fprovider_filter\x18\x04 \x01(\x0b\x32-.spaceone.api.cost_analysis.v1.ProviderFilter\x12N\n\ttime_unit\x18\x05 \x01(\x0e\x32;.spaceone.api.cost_analysis.v1.CreateBudgetRequest.TimeUnit\x12\r\n\x05start\x18\x06 \x01(\t\x12\x0b\n\x03\x65nd\x18\x07 \x01(\t\x12H\n\rnotifications\x18\x08 \x03(\x0b\x32\x31.spaceone.api.cost_analysis.v1.BudgetNotification\x12%\n\x04tags\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x12\n\nproject_id\x18\x0b \x01(\t\x12\x18\n\x10project_group_id\x18\x0c \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18\r \x01(\t\x12\x11\n\tdomain_id\x18\x0e \x01(\t\",\n\x08TimeUnit\x12\x08\n\x04NONE\x10\x00\x12\t\n\x05TOTAL\x10\x01\x12\x0b\n\x07MONTHLY\x10\x02\"\xc4\x01\n\x13UpdateBudgetRequest\x12\x11\n\tbudget_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05limit\x18\x03 \x01(\x02\x12\x43\n\x0eplanned_limits\x18\x04 \x03(\x0b\x32+.spaceone.api.cost_analysis.v1.PlannedLimit\x12%\n\x04tags\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"\x8e\x01\n\x1cSetBudgetNotificationRequest\x12\x11\n\tbudget_id\x18\x01 \x01(\t\x12H\n\rnotifications\x18\x02 \x03(\x0b\x32\x31.spaceone.api.cost_analysis.v1.BudgetNotification\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"5\n\rBudgetRequest\x12\x11\n\tbudget_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"F\n\x10GetBudgetRequest\x12\x11\n\tbudget_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\xa9\x02\n\x0b\x42udgetQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x11\n\tbudget_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nproject_id\x18\x04 \x01(\t\x12\x18\n\x10project_group_id\x18\x05 \x01(\t\x12\x46\n\ttime_unit\x18\x06 \x01(\x0e\x32\x33.spaceone.api.cost_analysis.v1.BudgetQuery.TimeUnit\x12\x16\n\x0e\x64\x61ta_source_id\x18\x07 \x01(\t\x12\x11\n\tdomain_id\x18\x0b \x01(\t\",\n\x08TimeUnit\x12\x08\n\x04NONE\x10\x00\x12\t\n\x05TOTAL\x10\x01\x12\x0b\n\x07MONTHLY\x10\x02\"\xde\x04\n\nBudgetInfo\x12\x11\n\tbudget_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05limit\x18\x03 \x01(\x02\x12\x43\n\x0eplanned_limits\x18\x04 \x03(\x0b\x32+.spaceone.api.cost_analysis.v1.PlannedLimit\x12\x10\n\x08\x63urrency\x18\x05 \x01(\t\x12\x46\n\x0fprovider_filter\x18\x06 \x01(\x0b\x32-.spaceone.api.cost_analysis.v1.ProviderFilter\x12\x45\n\ttime_unit\x18\x07 \x01(\x0e\x32\x32.spaceone.api.cost_analysis.v1.BudgetInfo.TimeUnit\x12\r\n\x05start\x18\x08 \x01(\t\x12\x0b\n\x03\x65nd\x18\t \x01(\t\x12H\n\rnotifications\x18\n \x03(\x0b\x32\x31.spaceone.api.cost_analysis.v1.BudgetNotification\x12%\n\x04tags\x18\x15 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x12\n\nproject_id\x18\x1f \x01(\t\x12\x18\n\x10project_group_id\x18  \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18! \x01(\t\x12\x11\n\tdomain_id\x18\" \x01(\t\x12\x12\n\ncreated_at\x18) \x01(\t\x12\x12\n\nupdated_at\x18* \x01(\t\",\n\x08TimeUnit\x12\x08\n\x04NONE\x10\x00\x12\t\n\x05TOTAL\x10\x01\x12\x0b\n\x07MONTHLY\x10\x02\"^\n\x0b\x42udgetsInfo\x12:\n\x07results\x18\x01 \x03(\x0b\x32).spaceone.api.cost_analysis.v1.BudgetInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"Z\n\x0f\x42udgetStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xf6\x07\n\x06\x42udget\x12\x93\x01\n\x06\x63reate\x12\x32.spaceone.api.cost_analysis.v1.CreateBudgetRequest\x1a).spaceone.api.cost_analysis.v1.BudgetInfo\"*\x82\xd3\xe4\x93\x02$\"\x1f/cost-analysis/v1/budget/create:\x01*\x12\x93\x01\n\x06update\x12\x32.spaceone.api.cost_analysis.v1.UpdateBudgetRequest\x1a).spaceone.api.cost_analysis.v1.BudgetInfo\"*\x82\xd3\xe4\x93\x02$\"\x1f/cost-analysis/v1/budget/update:\x01*\x12\xb0\x01\n\x10set_notification\x12;.spaceone.api.cost_analysis.v1.SetBudgetNotificationRequest\x1a).spaceone.api.cost_analysis.v1.BudgetInfo\"4\x82\xd3\xe4\x93\x02.\")/cost-analysis/v1/budget/set-notification:\x01*\x12z\n\x06\x64\x65lete\x12,.spaceone.api.cost_analysis.v1.BudgetRequest\x1a\x16.google.protobuf.Empty\"*\x82\xd3\xe4\x93\x02$\"\x1f/cost-analysis/v1/budget/delete:\x01*\x12\x8a\x01\n\x03get\x12/.spaceone.api.cost_analysis.v1.GetBudgetRequest\x1a).spaceone.api.cost_analysis.v1.BudgetInfo\"\'\x82\xd3\xe4\x93\x02!\"\x1c/cost-analysis/v1/budget/get:\x01*\x12\x88\x01\n\x04list\x12*.spaceone.api.cost_analysis.v1.BudgetQuery\x1a*.spaceone.api.cost_analysis.v1.BudgetsInfo\"(\x82\xd3\xe4\x93\x02\"\"\x1d/cost-analysis/v1/budget/list:\x01*\x12y\n\x04stat\x12..spaceone.api.cost_analysis.v1.BudgetStatQuery\x1a\x17.google.protobuf.Struct\"(\x82\xd3\xe4\x93\x02\"\"\x1d/cost-analysis/v1/budget/stat:\x01*BDZBgithub.com/cloudforet-io/api/dist/go/spaceone/api/cost_analysis/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.cost_analysis.v1.budget_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZBgithub.com/cloudforet-io/api/dist/go/spaceone/api/cost_analysis/v1'
  _BUDGET.methods_by_name['create']._options = None
  _BUDGET.methods_by_name['create']._serialized_options = b'\202\323\344\223\002$\"\037/cost-analysis/v1/budget/create:\001*'
  _BUDGET.methods_by_name['update']._options = None
  _BUDGET.methods_by_name['update']._serialized_options = b'\202\323\344\223\002$\"\037/cost-analysis/v1/budget/update:\001*'
  _BUDGET.methods_by_name['set_notification']._options = None
  _BUDGET.methods_by_name['set_notification']._serialized_options = b'\202\323\344\223\002.\")/cost-analysis/v1/budget/set-notification:\001*'
  _BUDGET.methods_by_name['delete']._options = None
  _BUDGET.methods_by_name['delete']._serialized_options = b'\202\323\344\223\002$\"\037/cost-analysis/v1/budget/delete:\001*'
  _BUDGET.methods_by_name['get']._options = None
  _BUDGET.methods_by_name['get']._serialized_options = b'\202\323\344\223\002!\"\034/cost-analysis/v1/budget/get:\001*'
  _BUDGET.methods_by_name['list']._options = None
  _BUDGET.methods_by_name['list']._serialized_options = b'\202\323\344\223\002\"\"\035/cost-analysis/v1/budget/list:\001*'
  _BUDGET.methods_by_name['stat']._options = None
  _BUDGET.methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\"\"\035/cost-analysis/v1/budget/stat:\001*'
  _globals['_PLANNEDLIMIT']._serialized_start=200
  _globals['_PLANNEDLIMIT']._serialized_end=243
  _globals['_BUDGETNOTIFICATION']._serialized_start=246
  _globals['_BUDGETNOTIFICATION']._serialized_end=578
  _globals['_BUDGETNOTIFICATION_UNIT']._serialized_start=452
  _globals['_BUDGETNOTIFICATION_UNIT']._serialized_end=503
  _globals['_BUDGETNOTIFICATION_NOTIFICATIONTYPE']._serialized_start=505
  _globals['_BUDGETNOTIFICATION_NOTIFICATIONTYPE']._serialized_end=578
  _globals['_PROVIDERFILTER']._serialized_start=581
  _globals['_PROVIDERFILTER']._serialized_end=736
  _globals['_PROVIDERFILTER_STATE']._serialized_start=686
  _globals['_PROVIDERFILTER_STATE']._serialized_end=736
  _globals['_CREATEBUDGETREQUEST']._serialized_start=739
  _globals['_CREATEBUDGETREQUEST']._serialized_end=1286
  _globals['_CREATEBUDGETREQUEST_TIMEUNIT']._serialized_start=1242
  _globals['_CREATEBUDGETREQUEST_TIMEUNIT']._serialized_end=1286
  _globals['_UPDATEBUDGETREQUEST']._serialized_start=1289
  _globals['_UPDATEBUDGETREQUEST']._serialized_end=1485
  _globals['_SETBUDGETNOTIFICATIONREQUEST']._serialized_start=1488
  _globals['_SETBUDGETNOTIFICATIONREQUEST']._serialized_end=1630
  _globals['_BUDGETREQUEST']._serialized_start=1632
  _globals['_BUDGETREQUEST']._serialized_end=1685
  _globals['_GETBUDGETREQUEST']._serialized_start=1687
  _globals['_GETBUDGETREQUEST']._serialized_end=1757
  _globals['_BUDGETQUERY']._serialized_start=1760
  _globals['_BUDGETQUERY']._serialized_end=2057
  _globals['_BUDGETQUERY_TIMEUNIT']._serialized_start=1242
  _globals['_BUDGETQUERY_TIMEUNIT']._serialized_end=1286
  _globals['_BUDGETINFO']._serialized_start=2060
  _globals['_BUDGETINFO']._serialized_end=2666
  _globals['_BUDGETINFO_TIMEUNIT']._serialized_start=1242
  _globals['_BUDGETINFO_TIMEUNIT']._serialized_end=1286
  _globals['_BUDGETSINFO']._serialized_start=2668
  _globals['_BUDGETSINFO']._serialized_end=2762
  _globals['_BUDGETSTATQUERY']._serialized_start=2764
  _globals['_BUDGETSTATQUERY']._serialized_end=2854
  _globals['_BUDGET']._serialized_start=2857
  _globals['_BUDGET']._serialized_end=3871
# @@protoc_insertion_point(module_scope)
