# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.inventory.v1 import cloud_service_query_set_pb2 as spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2


class CloudServiceQuerySetStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceQuerySet/create',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CreateCloudServiceQuerySetRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceQuerySet/update',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.UpdateCloudServiceQuerySetRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceQuerySet/delete',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.run = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceQuerySet/run',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.test = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceQuerySet/test',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )
        self.enable = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceQuerySet/enable',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.FromString,
                )
        self.disable = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceQuerySet/disable',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceQuerySet/get',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.GetCloudServiceQuerySetRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceQuerySet/list',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetsInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.inventory.v1.CloudServiceQuerySet/stat',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class CloudServiceQuerySetServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Create a new query set. Periodic statistics data is created based on the query set.
        `query` parameters refer to AnalyzeQuery.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Update a specific query set. You can only update the query set of custom type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Delete a specific query set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def run(self, request, context):
        """Run a specific query set and store the result in the statistics data.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def test(self, request, context):
        """Run a specific query set and store the result in the statistics data.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enable(self, request, context):
        """Enable a specific query set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable(self, request, context):
        """Disable a specific query set. query set is not executed when disabled.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Get a specific query set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Gets a list of all query sets.
        You can use a query to get a filtered list of query sets.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CloudServiceQuerySetServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CreateCloudServiceQuerySetRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.UpdateCloudServiceQuerySetRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'run': grpc.unary_unary_rpc_method_handler(
                    servicer.run,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'test': grpc.unary_unary_rpc_method_handler(
                    servicer.test,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
            'enable': grpc.unary_unary_rpc_method_handler(
                    servicer.enable,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.SerializeToString,
            ),
            'disable': grpc.unary_unary_rpc_method_handler(
                    servicer.disable,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.GetCloudServiceQuerySetRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.inventory.v1.CloudServiceQuerySet', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CloudServiceQuerySet(object):
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceQuerySet/create',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CreateCloudServiceQuerySetRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceQuerySet/update',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.UpdateCloudServiceQuerySetRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceQuerySet/delete',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def run(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceQuerySet/run',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def test(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceQuerySet/test',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def enable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceQuerySet/enable',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def disable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceQuerySet/disable',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceQuerySet/get',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.GetCloudServiceQuerySetRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceQuerySet/list',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetQuery.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetsInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.CloudServiceQuerySet/stat',
            spaceone_dot_api_dot_inventory_dot_v1_dot_cloud__service__query__set__pb2.CloudServiceQuerySetStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
