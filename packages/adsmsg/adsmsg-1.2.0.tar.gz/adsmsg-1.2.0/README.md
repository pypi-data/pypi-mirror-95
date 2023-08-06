[![Build Status](https://travis-ci.org/adsabs/ADSPipelineMsg.svg)](https://travis-ci.org/adsabs/ADSPipelineMsg)
[![Coverage Status](https://coveralls.io/repos/adsabs/ADSPipelineMsg/badge.svg)](https://coveralls.io/r/adsabs/ADSPipelineMsg)


# adsmsg

## Short Summary

Message definitions based on [Google Protocol Buffers](https://developers.google.com/protocol-buffers/) to be used by ADS Pipelines.


## Development

To modify message definition, Protocol Buffers compiler should be installed:

```
sudo apt-get install autoconf automake libtool curl make g++ unzip
wget https://github.com/google/protobuf/releases/download/v3.3.0/protobuf-python-3.3.0.tar.gz
tar -zxvf protobuf-python-3.3.0.tar.gz
cd protobuf-3.3.0/
./configure
make
sudo make install
sudo ldconfig # refresh shared library cache.
```

and the protocol buffers should be compiled from the specs directory with:

```
protoc --python_out=../adsmsg/protobuf filename.proto
# protoc does not express imports in a relative form, which messes up with our package structure
# thus we force relative imports by changing the generated files with the next sed command:
# 	https://github.com/protocolbuffers/protobuf/issues/1491#issuecomment-369324250
sed -i 's/^import \([^ ]*\)_pb2 as \([^ ]*\)$/from . import \1_pb2 as \2/' ../adsmsg/protobuf/*_pb2.py
```

Alternatively, a docker container can be built:

```
docker build -t adsmsg .
docker run --rm -v `pwd`:/app --name adsmsg adsmsg make
```

Or better, just run:

```
./rebuild.sh
```

Every time the protocol buffers specifications are changed.


### Testing

Travis will run tests automatically. You can manually run them in your machine with:

```
py.test
```

### Releasing new version to pypi

When a new release is ready, it should be uploaded to pypi. First, try the test environment (instructions given for Python 3, but can also use Python 2):

```
python3 -m venv ./venv
source venv/bin/activate
pip install --upgrade setuptools wheel
rm -rf dist/
python3 setup.py sdist
python3 setup.py bdist_wheel --universal
pip install --upgrade twine
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Verify the [testing pypi repository](https://test.pypi.org/project/adsmsg/) and if everything looks good, you can proceed to upload to the [official repository](https://pypi.org/project/adsmsg/):

```
twine upload dist/*
```


## Maintainer(s)

Sergi
