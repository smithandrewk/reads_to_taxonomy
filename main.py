# %%
import os
from tqdm import tqdm
from staphb_toolkit.lib import calldocker as container_engine
from staphb_toolkit.lib.autopath import path_replacer
import staphb_toolkit.lib.container_handler as container
source_dir = f'data/0_raw'
target_dir = f'data/1_trimmed'
if not os.path.isdir(target_dir):
    os.makedirs(target_dir)

# %%
for file in tqdm(os.listdir(source_dir)):
    id = file.split("_")[0]
    print(id)
    if os.path.exists(f'{target_dir}/{id}_1.trimd.fastq'):
        print(f'{id} already trimmed, continuing')
        continue
    print(f'trimming {id}')
    command = f'staphb-tk trimmomatic PE {source_dir}/{id}_1.fastq {source_dir}/{id}_2.fastq {target_dir}/{id}_1.paired.fastq {target_dir}/{id}_1.unpaired.fastq {target_dir}/{id}_2.paired.fastq {target_dir}/{id}_2.unpaired.fastq LEADING:20 TRAILING:20 MINLEN:50'
    os.system(command)

# %%
source_dir = f'data/1_trimmed'
target_dir = f'data/2_qc'
if not os.path.isdir(target_dir):
    os.makedirs(target_dir)
files = [file.replace(".fastq","") for file in os.listdir(source_dir) if file.endswith(".paired.fastq")]
files

# %%
for file in files:
    if os.path.exists(f'{target_dir}/{file}_fastqc.html'):
        print(f'{file} already qc, continue')
        continue
    command = f'staphb-tk fastqc {source_dir}/{file}.fastq -o {target_dir}'
    os.system(command)

# %%
command = f'staphb-tk multiqc data/2_qc -o data/3_mqc --force'
os.system(command)

# %%
import os
source_dir = f'data/1_trimmed'
target_dir = f'data/4_assembled'
if not os.path.isdir(target_dir):
    os.makedirs(target_dir)
files = [file.replace("_1.paired.fastq","") for file in os.listdir(source_dir) if file.endswith('1.paired.fastq')]

# %%
for file in files:
    print(file)
    if os.path.isdir(f'{target_dir}/{file}'):
        print(f'already assembled {file}')
        continue
    args = [f'-1',f'{source_dir}/{file}_1.paired.fastq',f'-2',f'{source_dir}/{file}_2.paired.fastq']
    arg_string,path_map = path_replacer(args,os.getcwd())
    print(arg_string,path_map)
    command = f'spades.py {arg_string} -o {target_dir}/{file}'
    program_object = container.Run(command=command, path=path_map, image='staphb/spades', tag='latest')
    program_object.run()
    os.system(f'cp {target_dir}/{file}/contigs.fasta {target_dir}/{file}/{file}_contigs.fasta')
command = f'staphb-tk quast data/4_assembled/*/contigs.fasta -o data/5_quast -t 1'
os.system(command)

# %%
# TODO double check
for id in os.listdir(f'data/4_assembled'):
    command = f'blastn -query data/4_assembled/{id}/contigs.fasta -db pathogen_database/ref_prok_rep_genomes -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle" -out data/4_assembled/{id}/results.tsv'
    os.system(command)

# %%
import pandas as pd
df = pd.read_csv(f'data/4_assembled/{id}/results.tsv',delimiter='\t',header=None,nrows=5)
df