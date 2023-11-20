# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.notification.v1 import protocol_pb2 as spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2


class ProtocolStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.notification.v1.Protocol/create',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.CreateProtocolRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.notification.v1.Protocol/update',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.UpdateProtocolRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
                )
        self.update_plugin = channel.unary_unary(
                '/spaceone.api.notification.v1.Protocol/update_plugin',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.UpdateProtocolPluginRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
                )
        self.enable = channel.unary_unary(
                '/spaceone.api.notification.v1.Protocol/enable',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
                )
        self.disable = channel.unary_unary(
                '/spaceone.api.notification.v1.Protocol/disable',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.notification.v1.Protocol/delete',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.notification.v1.Protocol/get',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.GetProtocolRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.notification.v1.Protocol/list',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolsInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.notification.v1.Protocol/stat',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class ProtocolServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Creates a new Protocol. When creating a protocol, you must specify the plugins provided from the repository, and you must also set the credentials to be set in the plugin if necessary.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Updates a specific Protocol. The method `update` can update the name and tags only. If you want to update the plugin version or options, you can use `update_plugin` method.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_plugin(self, request, context):
        """Updates a plugin for a Protocol. It is usually used when redeploying a plugin to a new version.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enable(self, request, context):
        """Enables a specific Protocol. If the Protocol is enabled, the Protocol can be used and the Notification can be dispatched.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable(self, request, context):
        """Disables a specific Protocol. If a Protocol is disabled, the Notification will not be dispatched, even if it is created.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Deletes a specific Protocol. If there exists a channel using the Protocol, it cannot be deleted.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Gets a specific Protocol. Prints detailed information about the Protocol.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Gets a list of Protocols. You can use a query to get a filtered list of Protocols.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProtocolServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.CreateProtocolRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.UpdateProtocolRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.SerializeToString,
            ),
            'update_plugin': grpc.unary_unary_rpc_method_handler(
                    servicer.update_plugin,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.UpdateProtocolPluginRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.SerializeToString,
            ),
            'enable': grpc.unary_unary_rpc_method_handler(
                    servicer.enable,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.SerializeToString,
            ),
            'disable': grpc.unary_unary_rpc_method_handler(
                    servicer.disable,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.GetProtocolRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.notification.v1.Protocol', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Protocol(object):
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.Protocol/create',
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.CreateProtocolRequest.SerializeToString,
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.Protocol/update',
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.UpdateProtocolRequest.SerializeToString,
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_plugin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.Protocol/update_plugin',
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.UpdateProtocolPluginRequest.SerializeToString,
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.Protocol/enable',
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolRequest.SerializeToString,
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.Protocol/disable',
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolRequest.SerializeToString,
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.Protocol/delete',
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolRequest.SerializeToString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.Protocol/get',
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.GetProtocolRequest.SerializeToString,
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.Protocol/list',
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolQuery.SerializeToString,
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolsInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.Protocol/stat',
            spaceone_dot_api_dot_notification_dot_v1_dot_protocol__pb2.ProtocolStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
