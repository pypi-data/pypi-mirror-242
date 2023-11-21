# -*- coding: utf-8 -*-
from base64 import b64encode
from typing import TYPE_CHECKING, Optional, Sequence, Tuple

import grpc
import grpc.aio

from esdbclient.connection_spec import ConnectionSpec
from esdbclient.exceptions import (
    AbortedByServer,
    CancelledByClient,
    ConsumerTooSlow,
    DeadlineExceeded,
    EventStoreDBClientException,
    ExceptionThrownByHandler,
    GrpcError,
    NodeIsNotLeader,
    NotFound,
    ServiceUnavailable,
)

if TYPE_CHECKING:  # pragma: no cover
    from grpc import Metadata

else:
    Metadata = Tuple[Tuple[str, str], ...]

__all__ = ["handle_rpc_error", "BasicAuthCallCredentials", "ESDBService", "Metadata"]


DEFAULT_CHECKPOINT_INTERVAL_MULTIPLIER = 5
DEFAULT_BATCH_APPEND_REQUEST_DEADLINE = 315576000000
DEFAULT_WINDOW_SIZE = 30


class BasicAuthCallCredentials(grpc.AuthMetadataPlugin):
    def __init__(self, username: str, password: str):
        credentials = b64encode(f"{username}:{password}".encode())
        self._metadata = (("authorization", (b"Basic " + credentials)),)

    def __call__(
        self,
        context: grpc.AuthMetadataContext,
        callback: grpc.AuthMetadataPluginCallback,
    ) -> None:
        callback(self._metadata, None)


def handle_rpc_error(e: grpc.RpcError) -> EventStoreDBClientException:
    """
    Converts gRPC errors to client exceptions.
    """
    if isinstance(e, (grpc.Call, grpc.aio.AioRpcError)):
        if (
            e.code() == grpc.StatusCode.UNKNOWN
            and "Exception was thrown by handler" in str(e.details())
        ):
            return ExceptionThrownByHandler(e)
        elif e.code() == grpc.StatusCode.ABORTED:
            details = e.details()
            if isinstance(details, str) and "Consumer too slow" in details:
                return ConsumerTooSlow()
            else:
                return AbortedByServer()
        elif (
            e.code() == grpc.StatusCode.CANCELLED
            and e.details() == "Locally cancelled by application!"
        ):
            return CancelledByClient(e)
        elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            return DeadlineExceeded(e)
        elif e.code() == grpc.StatusCode.UNAVAILABLE:
            return ServiceUnavailable(e)
        elif (
            e.code() == grpc.StatusCode.NOT_FOUND
            and e.details() == "Leader info available"
        ):
            return NodeIsNotLeader(e)
        elif e.code() == grpc.StatusCode.NOT_FOUND:
            return NotFound()
    return GrpcError(e)


class ESDBService:
    def __init__(self, connection_spec: ConnectionSpec):
        self.connection_spec = connection_spec

    def _metadata(
        self, metadata: Optional[Metadata], requires_leader: bool = False
    ) -> Metadata:
        default = (
            "true"
            if self.connection_spec.options.NodePreference == "leader"
            else "false"
        )
        requires_leader_metadata: Metadata = (
            ("requires-leader", "true" if requires_leader else default),
        )
        metadata = tuple() if metadata is None else metadata
        return metadata + requires_leader_metadata


def construct_filter_include_regex(patterns: Sequence[str]) -> str:
    patterns = [patterns] if isinstance(patterns, str) else patterns
    return "^" + "|".join(patterns) + "$"


def construct_filter_exclude_regex(patterns: Sequence[str]) -> str:
    patterns = [patterns] if isinstance(patterns, str) else patterns
    return "^(?!(" + "|".join([s + "$" for s in patterns]) + "))"
