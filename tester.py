import subprocess, shutil

ass = subprocess.Popen(["py","FloatAssembler.py"],stdin=open("input.txt","r"),stdout=subprocess.PIPE)
print("Running simulator...")
subprocess.run(["py","FloatSimulator.py"],stdin=ass.stdout)
subprocess.run(["py","FloatAssembler.py"],stdin=open("input.txt","r"),stdout=open("code.txt","w"))