# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.inventory.v1 import cloud_service_stats_pb2 as spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2


class CloudServiceStatsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.list = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceStats/list',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsInfo.FromString,
                )
        self.analyze = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceStats/analyze',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsAnalyzeQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceStats/stat',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class CloudServiceStatsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def list(self, request, context):
        """Gets a list of raw statistics data.
        You can use a query to get a filtered list of statistics data.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def analyze(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CloudServiceStatsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsInfo.SerializeToString,
            ),
            'analyze': grpc.unary_unary_rpc_method_handler(
                    servicer.analyze,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsAnalyzeQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.inventory.v1.CloudServiceStats', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CloudServiceStats(object):
    """Missing associated documentation comment in .proto file."""

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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceStats/list',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsQuery.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def analyze(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceStats/analyze',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsAnalyzeQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceStats/stat',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__stats__pb2.CloudServiceStatsStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
