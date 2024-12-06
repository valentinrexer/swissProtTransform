from Bio import SwissProt
import pandas as pd
import sqlite3
import re


def create_db_from_df(df, db_path, table_name='sw_table'):
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, index=False)


def extract_ec_number(description):
    description = description.replace('n', '')

    # Regex pattern to match EC number format
    ec_pattern = r'EC=([0-9]+|-).([0-9]+|-).([0-9]+|-).([0-9]+|-)'

    # Search for EC number in the text
    match = re.search(ec_pattern, description, re.IGNORECASE)

    if match:
        return match.group(0)

    return None

path = '/home/user/datascience/uniprot_sprot.dat'
out_db_path = '/home/user/datascience/swissprot.dat.db'

rows = []
columns = ["ID","AC_Number","Description", "EC_Number", "Sequence"]

with open(path) as f:
    for record in SwissProt.parse(f):
        ec_number = ''

        if "EC=" in record.description:
            ec_number = extract_ec_number(record.description)

            if ec_number is not None:
                ec_number = ec_number.split('=')[1]

            else:
                continue

        else:
            continue


        entry = [record.entry_name,
                 record.accessions[0],
                 record.description,
                 ec_number,
                 record.sequence]


        rows.append(dict(zip(columns, entry)))


with open(out_db_path, 'w') as f:
    f.write('')

print(len(rows))


swiss_prot_df = pd.DataFrame(rows)
create_db_from_df(swiss_prot_df, out_db_path)



