import grpc
import os

from base64 import b64encode
from typing import Optional

from pyspark.sql.connect.client import ChannelBuilder

AUTHORIZATION_HEADER = 'authorization'


class _NebiusChannelBuilder(ChannelBuilder):
    def __init__(self, connect_endpoint: str, auth_header: str, root_certificates: Optional[bytes] = None):
        self._root_certificates = root_certificates
        super().__init__(url=f"sc://{connect_endpoint}")

        self.params = {
            ChannelBuilder.PARAM_USE_SSL: "true",
            AUTHORIZATION_HEADER: auth_header
        }

    def toChannel(self) -> grpc.Channel:
        destination = f"{self.host}:{self.port}"

        ssl_creds = grpc.ssl_channel_credentials(
            root_certificates=self._root_certificates,
        )
        return grpc.secure_channel(
            destination,
            credentials=ssl_creds,
            options=self._channel_options,
        )


def create_channel_builder(
        connect_endpoint: str,
        *,
        password: Optional[str] = None,
        root_certificates_file: Optional[str] = None,
) -> ChannelBuilder:
    """Creates a ChannelBuilder instance for establishing a gRPC channel to
    connect to Spark Connect session.

    Examples
    --------
    >>> from pyspark.sql.connect.session import SparkSession
    >>> from nebius.spark.connect import channel_builder
    >>> spark = SparkSession \
    ...     .builder \
    ...     .channelBuilder(create_channel_builder('spsession-example123.nebius.cloud:443', password='my-password')) \
    ...     .getOrCreate()

    Parameters
    ----------
    connect_endpoint : str
        The Spark Connect endpoint to connect to. Must be in the format `host:port`.
    password : str, optional
        The password for authentication.
    root_certificates_file : str, optional
        The path to the root certificates file. If None, certificates will be
        retrieved from a default location chosen by gRPC runtime.

    Raises
    ------
    ValueError
        If password is missing

    Returns
    -------
    ChannelBuilder
        An instance of ChannelBuilder configured with the provided parameters.
    """

    # Make sure the SPARK_CONNECT_MODE_ENABLED environment variable is set to 1
    # This is required for pyspark to detect that it is running in Spark Connect mode
    os.environ["SPARK_CONNECT_MODE_ENABLED"] = "1"

    if password is None:
        raise ValueError("Password is required for authentication.")

    root_certificates: Optional[bytes] = None
    if root_certificates_file:
        with open(root_certificates_file, 'rb') as f:
            root_certificates = f.read()

    username_password = f'spark:{password}'
    auth_header = f'Basic {b64encode(username_password.encode()).decode()}'

    return _NebiusChannelBuilder(connect_endpoint, auth_header, root_certificates)
