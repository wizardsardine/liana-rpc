## Requirements for tests

To run the tests you should have a running bitcoind and a runnind lianad, if lianad running, it will be automaticaly 
detected.

You need to install `embit`, `tox` and `pytest` installed prior to run tests:
```shell
pip install embit tox pytest
```
tox will allow you to run the test on different python versions

## Run tests with pytest
You can also run the test on pytest on your actual python version:
```shell
pytest -v -s tests/
```

if you want to show outputs of expected failing tests:
```shell
pytest -v -s --runxfail tests/
```

## Run only mocked test
Note that if there is no running `lianad` instance, pytest will skip `live_rpc_test.py` and run only `mock_rpc_test.py`.

## Build package

`build` is needed to build the package, you can install it with:
```shell
pip install build
```

Then for build the package just run:
```shell
python3 -m build
```

packages will be in `dist/` folder