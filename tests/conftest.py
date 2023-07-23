import pytest
import subprocess
import os
from liana_rpc.liana_rpc import get_liana_instances

RED_COLOR = '\033[31m'
RESET_COLOR = '\033[0m'


def skip_live_rpc_test(items, msg):
    for item in items:
        if item.parent.name == "live_rpc_test.py":
            skip_marker = pytest.mark.skip(
                reason=RED_COLOR + msg + RESET_COLOR)
            item.add_marker(skip_marker)


def pytest_collection_modifyitems(config, items):

    if not get_liana_instances():
        skip_live_rpc_test(items, "SKIP - lianad not running")
        