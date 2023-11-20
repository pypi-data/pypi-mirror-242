# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from _qwak_proto.qwak.features_operator.v2 import features_operator_service_pb2 as qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2


class FeaturesOperatorServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ValidateDataSource = channel.unary_unary(
                '/qwak.features_operator.v2.FeaturesOperatorService/ValidateDataSource',
                request_serializer=qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidateDataSourceRequest.SerializeToString,
                response_deserializer=qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidationResponse.FromString,
                )
        self.ValidateFeatureSet = channel.unary_unary(
                '/qwak.features_operator.v2.FeaturesOperatorService/ValidateFeatureSet',
                request_serializer=qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidateFeatureSetRequest.SerializeToString,
                response_deserializer=qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidationResponse.FromString,
                )


class FeaturesOperatorServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ValidateDataSource(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidateFeatureSet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FeaturesOperatorServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ValidateDataSource': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateDataSource,
                    request_deserializer=qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidateDataSourceRequest.FromString,
                    response_serializer=qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidationResponse.SerializeToString,
            ),
            'ValidateFeatureSet': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateFeatureSet,
                    request_deserializer=qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidateFeatureSetRequest.FromString,
                    response_serializer=qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'qwak.features_operator.v2.FeaturesOperatorService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FeaturesOperatorService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ValidateDataSource(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.features_operator.v2.FeaturesOperatorService/ValidateDataSource',
            qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidateDataSourceRequest.SerializeToString,
            qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ValidateFeatureSet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qwak.features_operator.v2.FeaturesOperatorService/ValidateFeatureSet',
            qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidateFeatureSetRequest.SerializeToString,
            qwak_dot_features__operator_dot_v2_dot_features__operator__service__pb2.ValidationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
