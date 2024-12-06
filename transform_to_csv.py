import pandas as pd
import sqlite3

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def parse_uniprot_fasta_header(header):
    header_as_list = []

    if header.startswith('>'):
        header = header[1:]

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

def create_df_entry(row_as_list):  # Remove data_frame parameter
    list_to_zip = []
    list_to_zip.extend(row_as_list[0:4])

    list_to_zip += [None] * 5
    list_to_zip.append(row_as_list[len(row_as_list) - 1])

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
            list_to_zip[8] = attr.split('=')[1].strip()

    return dict(zip(columns, list_to_zip))  # Return the dictionary instead of modifying DataFrame

def create_db_from_df(df, db_path, table_name='my_table'):
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, index=False)

fasta_path = '/user/datascience/uniprot_sprot.fasta'
columns = ["Type", "Accession", "EntryName", "Description", "Organism", "TaxonomyID", "GeneName", "ProteinExistence", "SequenceVersion", "AASequence"]
out_db_path = '/home/user/datascience/swissprot.db'

rows = []  # Store rows in a list instead of constantly concatenating DataFrames
current_seq = None
current_entry = []
c = 0

with open(fasta_path, 'r') as f:
    for line in f:

        if line.startswith('>'):
            if current_seq is not None:  # If we have a sequence
                current_entry.append(current_seq)
                rows.append(create_df_entry(current_entry))  # Add the row dictionary
            current_seq = ''
            current_entry = parse_uniprot_fasta_header(line)
        else:
            current_seq += line.strip()

    if current_seq is not None:
        current_entry.append(current_seq)
        rows.append(create_df_entry(current_entry))

with open(out_db_path, 'w') as f:
    f.write('')

final_df = pd.DataFrame(rows)  # Create DataFrame once at the end
create_db_from_df(final_df, out_db_path)

