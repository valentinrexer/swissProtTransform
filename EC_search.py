path = '/home/valentin-rexer/uni/UofM/datascience/datasets/uniprot_sprot.dat'

with open(path, 'r') as f:
    for line in f:
        if "EC=" in line:
            print(line)