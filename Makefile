export PYTHONPATH=google/protobuf/compiler/
all:
	protoc --proto_path=/usr/include/ --python_out=. /usr/include/google/protobuf/compiler/plugin.proto
	protoc --proto_path=. --plugin=protoc-gen-cppinsertion --cpp_out=. --cppinsertion_out=. teste.proto
