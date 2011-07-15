#!/usr/bin/env python
#
# C++ code insertion plugin
#
# This plugin can be used to insert code into C++ generated code.
#
#
# Author: Thiago Cangussu de Castro Gomes <cangussu@gmail.com>
#
import sys
import os
import plugin_pb2

# Default contents:
includes_content  = "#include \"%s_include.h\""
global_content    = "#include \"%s_global.h\""
namespace_content = "#include \"%s_namespace.h\""
class_content     = "#include \"%s_class_%s.h\""

def insert_includes():
	pass

def insert_global():
	pass

def insert_class(filename, classname):
	content = class_content % ( filename, classname.replace(".", "_") )
	insert(filename, "class_scope:%s" % mtype.name, content)

def insert_namespace():
	pass

def insert_globals(filename):
	insert(filename, "includes",        includes_content  % filename)
	insert(filename, "global_scope",    global_content    % filename)
	insert(filename, "namespace_scope", namespace_content % filename)

def debug(message):
	sys.stderr.write(message + "\n")

# Create request and response objects
request = plugin_pb2.CodeGeneratorRequest()
response = plugin_pb2.CodeGeneratorResponse()

# Read request from standard input
request.ParseFromString(sys.stdin.read())

# Inserts a content at a given response insertion point
def insert(filename, insertion, content):
	response_file = response.file.add()
	response_file.name            = filename
	response_file.insertion_point = insertion
	response_file.content         = content

def add_nested_types(filename, message, prevname):
	for mtype in message.nested_type:
		newname = prevname + "." + mtype.name
		insert_class(filename, newname)
		add_nested_types(filename, mtype, newname)

# Generates code for each input file:
for index in range(len(request.proto_file)):
	# Get the output filename: test.proto -> test.pb.h
	filename = request.file_to_generate[index]
	filename = filename.split(".")[0] + ".pb.h"

	insert_globals(filename)

	for mtype in request.proto_file[index].message_type:
		insert(filename, "class_scope:%s" % mtype.name, class_content % (filename, mtype.name.replace(".", "_")))
		add_nested_types(filename, mtype, mtype.name)
	break

# Finally, send the inserted code to output stream
sys.stdout.write(response.SerializeToString())


