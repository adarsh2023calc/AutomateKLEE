
import os

def replace_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            # Check if the line contains only the specified pattern
            group = line.split('=')
            group1 = line.split('(')

            if group[-1].strip() =='__VERIFIER_nondet_int();' or group[-1].strip()=='__VERIFIER_nondet_bool();':
                declaration = (group[0].split())
                if len(declaration) > 1:
                    variable_type = declaration[0]
                    variable_name = declaration[1]
                    file.write(f'{variable_type} {variable_name};\nklee_make_symbolic(&{variable_name}, sizeof({variable_type}), "{variable_name}");\n')
                else:
                    if group[-1].strip()=='__VERIFIER_nondet_bool();':
                        file.write(f'\nklee_make_symbolic(&{declaration[0]}, sizeof(_Bool), "{declaration[0]}");\n')
                    else:
                        file.write(f'\nklee_make_symbolic(&{declaration[0]}, sizeof(int), "{declaration[0]}");\n')

            elif group[-1].strip() =='__VERIFIER_nondet_uint();':
                declaration = (group[0].split())
                string1  =""
                for element in declaration[:2]:
                    string1+= element+" "
                    
                file.write(f'{string1} {declaration[-1]};\n klee_make_symbolic(&{declaration[-1]}, sizeof({string1}), "{declaration[-1]}");\n')
            elif group1[0].strip()=="__VERIFIER_assert":
                line = line.strip()
                print(line)
                declaration ="klee"+line[10:]
                file.write(declaration)

            else:   
                # Keep the original line'''
                file.write(line)


# Replace lines in all C files in the current directory
for filename in os.listdir('/home/adarsh2023/input'):
    if filename.endswith('.c'):
        replace_lines(filename)