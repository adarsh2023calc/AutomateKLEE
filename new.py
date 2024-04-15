
import os
# This is to add klee/klee.h module in each C File you encounter

def add_klee_include(file_path):
    # Read the content of the C file
    with open(file_path, 'r') as file:
        content = file.read()

    # Add the #include <klee/klee.h> at the beginning of the file
    modified_content = '#include <klee/klee.h>\n' + content

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)

# Specify the path to your C file
c_file_path = '/home/adarsh2023/input/'
for file in os.listdir(c_file_path):
    if file!='__pycache__' and file.endswith(".c"):
        add_klee_include(file)
