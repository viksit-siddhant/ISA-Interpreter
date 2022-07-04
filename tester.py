import subprocess
def gen():
    for i in range(1,12):
        read_file = open(f"test_cases/{i}.txt",'r')
        write_file = open(f"test_cases/{i}_input.txt",'w')
        check_file = open(f"test_cases/{i}_output.txt",'w')
        flag = True
        for line in read_file:
            if line[0] == '#':
                flag = False
                continue
            if flag:
                write_file.write(line)
            else:
                check_file.write(line)

def test():
    for i in range(1,12):