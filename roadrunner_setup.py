import os
import sys
import glob
import subprocess

# Install gRPC Tools
subprocess.run([sys.executable, '-m', 'pip', 'install', 'grpcio'])
subprocess.run([sys.executable, '-m', 'pip', 'install', 'grpcio-tools'])
# Install psutil
subprocess.run([sys.executable, '-m', 'pip', 'install', 'psutil'])

current_directory = os.path.dirname(os.path.realpath(__file__))
current_directory = current_directory.replace(os.sep, '/')
proto_directory = r"C:\Program Files\RoadRunner R2023b\bin\win64\Proto"
proto_directory = os.path.realpath(proto_directory).replace(os.sep, '/')
directory = proto_directory + "/mathworks/"
output_directory = current_directory

if not os.path.isdir(output_directory) :
    os.mkdir(output_directory)

file_paths = ""

def add_entries(directory) :
    global file_paths
    for entry in os.scandir(directory) : 
        file = os.path.relpath(entry.path, start = proto_directory)
        file = file.replace(os.sep, '/')
        if file.endswith(".proto"):
            file_paths += " " + "\"" + file + "\""

add_entries(directory + "roadrunner/")
add_entries(directory + "scenario/common/")
add_entries(directory + "scenario/scene/hd/")
add_entries(directory + "scenario/simulation/")

args = "\"" + sys.executable.replace(os.sep, '/') + "\" -m grpc_tools.protoc --proto_path=\"" + proto_directory + "\" --python_out=\"" + output_directory + "\" --grpc_python_out=\"" + output_directory + "\""
args = args + file_paths
subprocess.run(args)

library_init_file = output_directory + "/__init__.py"

if os.path.exists(library_init_file) :
    os.remove(library_init_file)

python_files = glob.glob(output_directory + "/**/*.py", recursive=True)
    
f = open(library_init_file, "a")
f.write("""import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
""")

for file in python_files : 
    file = os.path.relpath(file, start = output_directory)
    file = os.path.splitext(file)[0]
    file = file.replace(os.sep, '.')
    f.write("from {} import *".format(file) + "\n")
