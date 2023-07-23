import pytest
import logging
from unittest.mock import patch

from liana_rpc.liana_rpc import LianaRPC, get_liana_instances


@pytest.mark.xfail(strict=True)
def test_multi_lianad():
    socket = get_liana_instances()
    i = 0
    while len(socket) < 2:
        i += 1
        socket.append(socket[0] + str(i))
    with patch('liana_rpc.liana_rpc.get_liana_instances', return_value=socket):
        LianaRPC()


@pytest.mark.xfail(strict=True)
def test_no_lianad():
    socket = []
    with patch('liana_rpc.liana_rpc.get_liana_instances', return_value=socket):
        LianaRPC()