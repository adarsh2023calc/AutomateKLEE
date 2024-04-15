

import os
import subprocess
import csv
import signal
import time
import keyboard

def search_csv(search_string):
    file_path = 'strategies1.csv'
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if search_string in row:
                return True
    return False

def convert_to_bitcode(c_file):
    # Use clang to compile C file to LLVM bitcode
    llvm_bitcode_file = f"{c_file[:-2]}.bc"
    print(llvm_bitcode_file)
    subprocess.run(['clang', '-I', '/home/adarsh2023/research/klee/include'  ,'-emit-llvm','-c', c_file])
    return llvm_bitcode_file

def timeout_handler():
    time.sleep(2)  
    #subprocess.run(['^C'])
    keyboard.press_and_release('ctrl+c')


def Read_to_csv(llvm_bitcode_file,strategy):
    print("END")
    time.sleep(1)
    file_path = '/home/adarsh2023/input/klee-last/info'
    with open(file_path, 'r') as file:
        last_lines = file.readlines()[-4:]
    # Extract numerical values and column names
        data = {}
        print(last_lines)
        file_name =(llvm_bitcode_file[:-2] +"c").split('/')[-1]
        fieldnames = ['File Name', 'Strategy', 'Total Instructions', 'Completed Paths', 'Partially Completed Paths', 'Generated Tests']
        data = {}
        data['File Name'] = file_name
        data['Strategy'] = strategy
        i =0
        for line in last_lines:
            parts = line.strip().split('=')
            column_name_extract = fieldnames[i+2]
            numerical_value = parts[-1].strip()
            data[column_name_extract] = numerical_value
            i+=1
        csv_file_path = 'strategies1.csv'
        with open(csv_file_path, 'a+', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)
    

def execute_with_klee(llvm_bitcode_file):
    # Use KLEE to execute LLVM bitcode
    
    strategies=['dfs','bfs','random-state','random-path','nurs:qc','nurs:md2u','nurs:icnt','nurs:rp','nurs:cpicnt','nurs:covnew']
    for strategy in strategies:
            flag =0
            signal.signal(signal.SIGALRM, timeout_handler)
            timeout_seconds = 40
            signal.alarm(timeout_seconds)

            try:
                flag = 1
           
                #subprocess.Popen(["klee",f"-search={strategy}", llvm_bitcode_file])
                subprocess.run(["klee",f"-search={strategy}", llvm_bitcode_file])
                
        # Save to CSV  file
            except:
                Read_to_csv(llvm_bitcode_file,strategy)
            finally:
                signal.alarm(0)
                if flag ==0:
                    Read_to_csv(llvm_bitcode_file,strategy)

            
        
def main(directory_path):
    # Get all C files in the specified directory
    c_files =[]
    for file in os.listdir(directory_path):

        if file.endswith(".c") and not search_csv(file):
            c_files.append(file)
    c_files.sort()
        
    # Convert each C file to LLVM bitcode and execute with KLEE
    for c_file in c_files:
        llvm_bitcode_file = convert_to_bitcode(os.path.join(directory_path, c_file))
        execute_with_klee(llvm_bitcode_file)

if __name__ == "__main__":
    directory_path = "/home/adarsh2023/input" # Replace path with the actual path to your directory
    main(directory_path)
