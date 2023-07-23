import json
import logging
import os
import socket

TIMEOUT = 20

"""
These classes have been taken from the test framework of Liana:
https://github.com/wizardsardine/liana/blob/master/tests/test_framework/utils.py
"""


class RpcError(ValueError):
    def __init__(self, method: str, params: dict, error: str):
        super(ValueError, self).__init__(
            "RPC call failed: method: {}, params: {}, error: {}".format(
                method, params, error
            )
        )

        self.method = method
        self.params = params
        self.error = error


class UnixSocket(object):
    """A wrapper for socket.socket that is specialized to unix sockets.

    Some OS implementations impose restrictions on the Unix sockets.

     - On linux OSs the socket path must be shorter than the in-kernel buffer
       size (somewhere around 100 bytes), thus long paths may end up failing
       the `socket.connect` call.

    This is a small wrapper that tries to work around these limitations.

    """

    def __init__(self, path: str):
        self.path = path
        self.sock = None
        self.connect()

    def connect(self) -> None:
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.connect(self.path)
            self.sock.settimeout(TIMEOUT)
        except OSError as e:
            self.close()

            if e.args[0] == "AF_UNIX path too long" and os.uname()[0] == "Linux":
                # If this is a Linux system we may be able to work around this
                # issue by opening our directory and using `/proc/self/fd/` to
                # get a short alias for the socket file.
                #
                # This was heavily inspired by the Open vSwitch code see here:
                # https://github.com/openvswitch/ovs/blob/master/python/ovs/socket_util.py

                dirname = os.path.dirname(self.path)
                basename = os.path.basename(self.path)

                # Open an fd to our home directory, that we can then find
                # through `/proc/self/fd` and access the contents.
                dirfd = os.open(dirname, os.O_DIRECTORY | os.O_RDONLY)
                short_path = "/proc/self/fd/%d/%s" % (dirfd, basename)
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.sock.connect(short_path)
            else:
                # There is no good way to recover from this.
                raise

    def close(self) -> None:
        if self.sock is not None:
            self.sock.close()
        self.sock = None

    def sendall(self, b: bytes) -> None:
        if self.sock is None:
            raise socket.error("not connected")

        self.sock.sendall(b)

    def recv(self, length: int) -> bytes:
        if self.sock is None:
            raise socket.error("not connected")

        return self.sock.recv(length)

    def __del__(self) -> None:
        self.close()


class UnixDomainSocketRpc(object):
    def __init__(self, socket_path, logger=None):
        self.socket_path = socket_path
        if not logger:
            self.logger = logging.getLogger()
        else:
            self.logger = logger
        self.next_id = 0
        self.sock = UnixSocket(self.socket_path)
        
    def __del__(self):
        self.close()

    def _readobj(self):
        """Read a JSON object"""
        buff = b""
        while True:
            n_to_read = max(2048, len(buff))
            chunk = self.sock.recv(n_to_read)
            buff += chunk
            if len(chunk) != n_to_read:
                try:
                    return json.loads(buff)
                except json.JSONDecodeError:
                    # There is more to read, continue
                    # FIXME: this is a workaround for large reads taken from lianad.
                    # We should use the '\n' marker instead since lianad uses that.
                    continue

    def __getattr__(self, name):
        """Intercept any call that is not explicitly defined and call @call.

        We might still want to define the actual methods in the subclasses for
        documentation purposes.
        """

        def wrapper(*args, **kwargs):
            if len(args) != 0 and len(kwargs) != 0:
                raise RpcError(
                    name, {}, "Cannot mix positional and non-positional arguments"
                )
            return self.call(name, params=args or kwargs)

        return wrapper

    def call(self, method, params={}):
        self.logger.debug(f"Calling {method} with params {params}")

        msg = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 0,
                "method": method,
                "params": params,
            }
        )
        self.sock.sendall(msg.encode() + b"\n")
        this_id = self.next_id
        resp = self._readobj()

        self.logger.debug(f"Received response for {method} call: {resp}")
        if "id" in resp and resp["id"] != this_id:
            raise ValueError(
                "Malformed response, id is not {}: {}.".format(this_id, resp)
            )

        if not isinstance(resp, dict):
            raise ValueError(
                f"Malformed response, response is not a dictionary: {resp}"
            )
        elif "error" in resp:
            
            out = {
                'error': resp['error'],
            }
            return out
            
        elif "result" not in resp:
            raise ValueError('Malformed response, "result" missing.')
        return resp["result"]
    
    def close(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None
        