To regenerate python proto, download new proto files from https://github.com/Netflix/conductor/tree/master/grpc/src/main/proto
Rename the directory grpc to conductor grpc. Rename any imports in the proto files referencing grpc to be conductor_grpc.
Then run `python -m grpc_tools.protoc -I=proto --python_out=src --grpc_python_out=src proto/*/*.proto`

to build and upload:

```shell
pip install --upgrade build twine
python -m build
twine upload dist/*
```

or

```shell
pipx install build
pipx install twine
pyproject-build
twine upload dist/*
```
