import argparse
import os
import sys
import subprocess
import re
import textwrap

try:
    from Bio import SeqIO
except:
    print("SeqIO module is not installed! Please install SeqIO and try again.")
    sys.exit()

try:
    import tqdm
except:
    print("tqdm module is not installed! Please install tqdm and try again.")
    sys.exit()

parser = argparse.ArgumentParser(prog='python gb2fasta.py',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent('''\

# gb2fasta

Author: Murat Buyukyoruk

        gb2fasta help:

This script is developed to convert genbank files to fasta.

SeqIO package from Bio is required to fetch sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.
        
Syntax:

        python gb2fasta.py -i demo.fasta 

gb2fasta dependencies:

Bio module and SeqIO available in this package      refer to https://biopython.org/wiki/Download

tqdm                                                refer to https://pypi.org/project/tqdm/
	
Input Paramaters (REQUIRED):
----------------------------
	-i/--input		Genbank		Specify a .gb file to convert into FASTA file 
	
Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.

	
      	'''))
parser.add_argument('-i', '--input', required=True, type=str, dest='filename', help='Specify a genbank file.\n')

results = parser.parse_args()
filename = results.filename

out = filename.split('.gb')[0] + '.fasta'

os.system('> ' + out)

proc = subprocess.Popen("grep -c 'ORIGIN' " + filename, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])

with tqdm.tqdm(range(length)) as pbar:
    pbar.set_description('Reading...')
    f = open(out, 'a')
    sys.stdout = f
    for record in SeqIO.parse(filename, "genbank"):
        pbar.update()
        print('>' + record.id + ' ' + record.description)
        print(re.sub("(.{60})", "\\1\n", str(record.seq), 0, re.DOTALL))
