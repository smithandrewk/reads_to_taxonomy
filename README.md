# Prerequisites
- staphb-tk
- blast
- docker
- python
- fasterq-dump (for testing)
# Usage
1. ```mkidr data```
2. ```mkidr data/0_raw```
3. ```cd data/0_raw```
4. ```fasterq-dump -Sp SRR26826511``` (for example, download a few)
5. ```cd ../../```
6. Download and place in subdirectory pathogen_database (ref_prok_rep_genomes) (reach out to andrew if you don't know how to download)(17 GB)
7. python3 main.py
# reads_to_taxonomy
