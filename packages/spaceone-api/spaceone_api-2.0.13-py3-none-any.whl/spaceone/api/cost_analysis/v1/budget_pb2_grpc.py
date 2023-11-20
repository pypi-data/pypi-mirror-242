# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.cost_analysis.v1 import budget_pb2 as spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2


class BudgetStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.Budget/create',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.CreateBudgetRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.Budget/update',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.UpdateBudgetRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.FromString,
                )
        self.set_notification = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.Budget/set_notification',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.SetBudgetNotificationRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.Budget/delete',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.Budget/get',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.GetBudgetRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.Budget/list',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetsInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.Budget/stat',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class BudgetServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Creates a new Budget. When creating a Budget, it should be set for a specific ProjectGroup or Project. The budgeted amount and date of the `planned_limits` should be specified on a monthly or yearly basis.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Updates a specific Budget. You can make changes in the budgeted amount of the time period specified while creating the resource.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def set_notification(self, request, context):
        """Sets a notification on a specific Budget. Sets a threshold on the budget, and if the cost exceeds the threshold, a notification is raised.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Deletes a specific Budget. You must specify the `budget_id` of the Budget to delete.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Gets a specific Budget. Prints detailed information about the Budget, including `planned_limits` of the project group or project for the pre-defined period.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Gets a list of all Budgets. You can use a query to get a filtered list of Budgets.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BudgetServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.CreateBudgetRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.UpdateBudgetRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.SerializeToString,
            ),
            'set_notification': grpc.unary_unary_rpc_method_handler(
                    servicer.set_notification,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.SetBudgetNotificationRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.GetBudgetRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.cost_analysis.v1.Budget', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Budget(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.Budget/create',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.CreateBudgetRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.Budget/update',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.UpdateBudgetRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def set_notification(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.Budget/set_notification',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.SetBudgetNotificationRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.Budget/delete',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.Budget/get',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.GetBudgetRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.Budget/list',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetQuery.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetsInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.cost_analysis.v1.Budget/stat',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_budget__pb2.BudgetStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
