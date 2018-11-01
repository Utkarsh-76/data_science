in_file = 'C:\Users\Jubin\Desktop\\tt.pdf'
print(in_file)
out_file = in_file[:-3] + "docx"

import subprocess, sys

p = subprocess.Popen(["powershell.exe", '-ExecutionPolicy','Unrestricted', "C:\\Users\\Jubin\\Desktop\\pdf_to_word.ps1", in_file, out_file], stdout=sys.stdout)

p.communicate()