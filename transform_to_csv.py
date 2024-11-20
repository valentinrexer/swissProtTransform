import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

path = f'/home/valentin-rexer/uni/UofM/datascience/datasets/uniprot_sprot.fasta'
columns = ["Type", "Accession", "EntryName", "Description", "Organism", "TaxonomyID", "GeneName", "ProteinExistence", "SequenceVersion", "AASequence"]
df = pd.DataFrame(columns=columns)


def parse_uniprot_fasta_header(header):

    header_as_list = []

    # if the header starts with a > it is removed
    if header.startswith('>'):
        header = header[1:]

    # split the header into an identifier and description part
    header_parts = header.split(' ', 1)
    identifier = header_parts[0]
    description = header_parts[1]

    for part in identifier.split('|'):
        header_as_list.append(part)

    started_Description = False

    for part in description.split(' '):
        if not started_Description and not '=' in part:
            started_Description = True
            header_as_list.append(part)

        elif not '=' in part:
            header_as_list[len(header_as_list) - 1] += "_" + part

        else:
            header_as_list.append(part)

    return header_as_list


def create_df_entry(row_as_list, data_frame):
    list_to_zip = []
    list_to_zip.extend(row_as_list[0:4])

    list_to_zip += [None] * 5
    list_to_zip.append(row_as_list[9])

    for attr in row_as_list:
        if "OS=" in attr:
            list_to_zip[4] = attr.split('=')[1]

        if "OX=" in attr:
            list_to_zip[5] = attr.split('=')[1]

        if "GN=" in attr:
            list_to_zip[6] = attr.split('=')[1]

        if "PE=" in attr:
            list_to_zip[7] = attr.split('=')[1]

        if "SV=" in attr:
            list_to_zip[8] = attr.split('=')[1]

    row = dict(zip(columns, list_to_zip))
    data_frame = pd.concat([data_frame, pd.DataFrame([row])], ignore_index=True)
    print(data_frame)

current_seq = ''
current_entry = []


with open(path, 'r') as f:
    for line in f:
        if line.startswith('>') and current_seq == '':
            current_entry = parse_uniprot_fasta_header(line)

        elif line.startswith('>'):
            current_entry.append(current_seq)
            current_seq = ''





header_to_use = parse_uniprot_fasta_header(">sp|P53031|2ABA_CANTR Protein phosphatase PP2A regulatory subunit B OS=Candida tropicalis OX=5482 GN=CDC55 PE=3 SV=1")
header_to_use.append("AGCATCATGC")

create_df_entry(header_to_use, df)



