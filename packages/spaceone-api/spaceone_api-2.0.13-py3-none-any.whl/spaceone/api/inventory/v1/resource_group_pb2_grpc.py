# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.inventory.v1 import resource_group_pb2 as spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2


class ResourceGroupStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.inventory.v1.ResourceGroup/create',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.CreateResourceGroupRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.inventory.v1.ResourceGroup/update',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.UpdateResourceGroupRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.inventory.v1.ResourceGroup/delete',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.inventory.v1.ResourceGroup/get',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.GetResourceGroupRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.inventory.v1.ResourceGroup/list',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupsInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.inventory.v1.ResourceGroup/stat',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class ResourceGroupServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Creates a new ResourceGroup. You can integrate `resource`s from different `provider`s by specifying the cloud resources to be grouped in the `resources` parameter.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Updates a specific ResourceGroup. You can make changes in ResourceGroup settings, including `name`, `tags`, and grouped resources in the ResourceGroup.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Deletes a specific ResourceGroup. You must specify the `resource_group_id` of the ResourceGroup to delete.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Gets a specific ResourceGroup. Prints detailed information about the ResourceGroup, including the information of the grouped cloud resources.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Gets a list of all ResourceGroups. You can use a query to get a filtered list of ResourceGroups.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ResourceGroupServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.CreateResourceGroupRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.UpdateResourceGroupRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.GetResourceGroupRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.inventory.v1.ResourceGroup', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ResourceGroup(object):
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.ResourceGroup/create',
            spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.CreateResourceGroupRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.ResourceGroup/update',
            spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.UpdateResourceGroupRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.ResourceGroup/delete',
            spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupRequest.SerializeToString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.ResourceGroup/get',
            spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.GetResourceGroupRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.ResourceGroup/list',
            spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupQuery.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupsInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.ResourceGroup/stat',
            spaceone_dot_api_dot_inventory_dot_v1_dot_resource__group__pb2.ResourceGroupStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
