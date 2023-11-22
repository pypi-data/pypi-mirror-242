import io
from abc import ABC
from typing import List

import boto3
from botocore.client import BaseClient
from deprecated.classic import deprecated
from drb.core import DrbNode, DrbFactory
from drb.drivers.http import DrbHttpNode
from drb.nodes.abstract_node import AbstractNode
from requests.auth import HTTPBasicAuth


class Auth:
    """
    This class give us all the requirement to connect to a swift service.

    Parameters:
        service_name: The name of a service, e.g. 's3' or 'ec2'.
            region_name: The name of the region associated with the client.
            A client is associated with a single region.

        api_version: The API version to use.  By default, this implementation
            use the latest API version. You only need to specify this parameter
            if you want to use a previous API version of the client.

        use_ssl: Whether to use SSL.  By default, SSL is used.
            Note that not all services support non-ssl connections.

        verify: Whether to verify SSL certificates. By default,
            SSL certificates are verified.  You can provide the following
            values:
            * False - do not validate SSL certificates.  SSL will still be
            used (unless use_ssl is False), but SSL certificates
            will not be verified.
            * path/to/cert/bundle.pem - A filename of the CA cert bundle to
            uses.

        endpoint_url: The complete URL to use for the constructed
            client. If this value is provided, then ``use_ssl`` is ignored.

        aws_access_key_id: The access key to use when creating
            the client.

        aws_secret_access_key: The secret key to use when creating
            the client.

        aws_session_token: The session token to use when creating
            the client.

        config: Advanced client configuration options. If region_name
            is specified in the client config, its value will take precedence
            over environment variables and configuration values, but not over
            a region_name value passed explicitly to the method.  If
            user_agent_extra is specified in the client config, it overrides
            the default user_agent_extra provided by the resource API.
      """

    def __init__(self,
                 **kwargs):
        self.service_name = "s3"
        self.region_name = kwargs.get("", None)
        self.api_version = kwargs.get("api_version", None)
        self.use_ssl = kwargs.get("use_ssl", True)
        self.verify = kwargs.get("verify", None)
        self.endpoint_url = kwargs.get("endpoint_url", None)
        self.aws_access_key_id = kwargs.get("aws_access_key_id", None)
        self.aws_secret_access_key = kwargs.get("aws_secret_access_key", None)
        self.aws_session_token = kwargs.get("aws_session_token", None)
        self.config = kwargs.get("config", None)

    def get_session(self):
        session = boto3.session.Session()

        return session.client(
            service_name=self.service_name,
            region_name=self.region_name,
            api_version=self.api_version,
            use_ssl=self.use_ssl,
            verify=self.verify,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
            config=self.config
        )


class Connection:
    """
    This class use the singleton pattern to provide too
    much connection to the s3 server.

    Parameters:
        auth: An Auth object to provide all the information required
              to establish the connection with the server.
    """

    conn = None

    def __new__(cls, auth: Auth) -> BaseClient:
        if cls.conn is None:
            cls.conn = boto3.resource(
                service_name=auth.service_name,
                region_name=auth.region_name,
                api_version=auth.api_version,
                use_ssl=auth.use_ssl,
                verify=auth.verify,
                endpoint_url=auth.endpoint_url,
                aws_access_key_id=auth.aws_access_key_id,
                aws_secret_access_key=auth.aws_secret_access_key,
                aws_session_token=auth.aws_session_token,
                config=auth.config
            )
        return cls.conn


class Requests:
    def __init__(self, auth: Auth):
        self.conn = Connection(auth)
        self.auth = auth

    def list_buckets(self):
        return self.conn.buckets.all()

    def list_objects(self, name):
        return self.conn.Bucket(name).objects.all()

    def get_temp_url(self, bucket, name):
        s3_api = self.auth.get_session()
        return s3_api.generate_presigned_url(
            'get_object', Params={
                'Bucket': bucket,
                'Key': name
            },
            ExpiresIn=3600
        )

    def get_obj(self, bucket, name):
        buff = io.BytesIO()
        obj = self.conn.Object(bucket, name)
        obj.download_fileobj(buff)
        return buff


def check_args(*args):
    return len(args) > 0 and isinstance(
        args[0],
        int
    ) and args[0] > 0


class DrbS3Node(AbstractNode, ABC):
    """
    Common DrbS3Node interface
    """

    def __init__(self, auth: Auth):
        super(DrbS3Node, self).__init__()
        self._auth = auth
        self._conn = None

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def close(self) -> None:
        """
        Close The s3 connection
        """
        if self._conn is not None:
            self._conn.close()

    def get_auth(self) -> Auth:
        """
        Return the Auth object created to access the service.
        """
        return self._auth

    def __eq__(self, other):
        return isinstance(other, DrbS3Node) and \
            self._auth == other._auth

    def __hash__(self):
        return hash(self._auth)


class DrbS3Object(DrbS3Node):
    def __init__(self, obj, parent: DrbS3Node):
        super().__init__(auth=parent.get_auth())
        self.req = Requests(parent.get_auth())
        self._obj = obj
        self.name = obj.key
        self.parent = parent
        self.add_impl(io.BytesIO, self._get_stream)
        self._init_attrs()

    def _init_attrs(self):
        for e in self._obj.get_available_subresources():
            name = e
            value = self._obj.key
            self.__imatmul__((name, value))

    @property
    @deprecated(version='1.2.0',
                reason='Usage of the bracket is recommended')
    def children(self) -> List[DrbNode]:
        return []

    @staticmethod
    def _get_stream(node: DrbNode, **kwargs):
        if not isinstance(node, DrbS3Object):
            raise TypeError(f'Invalid node type: {type(node)}')

        if kwargs.get('temp_url', False):
            tmp_url = node.req.get_temp_url(node.parent.name, node.name)
            return DrbHttpNode(tmp_url).get_impl(io.BytesIO)
        else:
            return node.req.get_obj(node.parent.name, node.name)


class DrbS3Bucket(DrbS3Node):

    def __init__(self, obj, parent: DrbS3Node):
        super().__init__(auth=parent.get_auth())
        self.req = Requests(parent.get_auth())
        self._bucket = obj
        self.name = obj.name
        self._children = None
        self.parent = parent
        self._init_attrs()

    def _init_attrs(self):
        for e in self._bucket.get_available_subresources():
            name = e
            value = self._bucket.name
            self.__imatmul__((name, value))

    @property
    @deprecated(version='1.2.0',
                reason='Usage of the bracket is recommended')
    def children(self) -> List[DrbNode]:
        self._conn = Connection(self._auth)
        if self._children is None:
            self._children = []
            objects = self.req.list_objects(self.name)
            for obj in objects:
                self._children.append(DrbS3Object(obj, self))

        return self._children


class DrbS3Service(DrbS3Node):
    def __init__(self, auth: Auth):
        super().__init__(auth=auth)
        self.req = Requests(auth)
        self._children = None
        self.name = self._auth.service_name

    @property
    @deprecated(version='1.2.0',
                reason='Usage of the bracket is recommended')
    def children(self) -> List[DrbNode]:
        self._conn = Connection(self._auth)
        if self._children is None:
            buckets = self.req.list_buckets()
            self._children = [
                DrbS3Bucket(bucket, self)
                for bucket in buckets
            ]
        return self._children


class S3NodeFactory(DrbFactory):

    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, DrbS3Node):
            return node
        if isinstance(node, DrbHttpNode):
            if isinstance(node.auth, HTTPBasicAuth):
                auth = Auth(service_name=node.path.original_path,
                            aws_access_key_id=node.auth.username,
                            aws_secret_access_key=node.auth.password)
            else:
                auth = Auth(service_name=node.path.original_path)
            return DrbS3Service(auth=auth)
        raise NotImplementedError("Call impl method")
