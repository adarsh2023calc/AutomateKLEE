import os
import shutil


def copy_to_directory(c_files,source_directory_path):
    destination= '/home/adarsh2023/input'
    for file in c_files:
        src_path = os.path.join(source_directory_path,file)
        destination_file = os.path.join(destination,file)
        shutil.copy(src_path,destination_file)
    

def extract_files(directory):
    c_files=[]
    files = os.listdir(directory)
    for file in files:
        if file.endswith('.c'):
            c_files.append(file)
    return c_files
if __name__ =='__main__':
    directory='/home/adarsh2023/sv-benchmarks/c/combinations'
    c_files = extract_files(directory)
    copy_to_directory(c_files,directory)




