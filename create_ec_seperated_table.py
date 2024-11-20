import pandas
import pandas as pd
import sqlite3

def create_db_from_df(df, db_path, table_name='sep_ec_table'):
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, index=False)

path_to_big_db = '/home/valentin-rexer/uni/UofM/datascience/datasets/swissprot.dat.db'
path_to_out_db = '/home/valentin-rexer/uni/UofM/datascience/datasets/ec_sep_swissprot.dat.db'
out_columns=['EC1', 'EC2', 'EC3', 'EC4', 'Sequence']

big_db_df = pd.read_sql_query(f'SELECT EC_Number, Sequence FROM sw_table', sqlite3.connect(path_to_big_db))
out_db_df = pandas.DataFrame(columns=out_columns)
out_rows = []

for row in big_db_df.itertuples():
    current_ec = row[1].replace('EC_Number=', '').replace('-','0')
    current_seq = row[2].replace('Sequence=', '')
    new_db_entry = []

    for level in current_ec.split('.'):
        new_db_entry.append(int(level))

    new_db_entry.append(current_seq)
    out_rows.append(dict(zip(out_columns, new_db_entry)))

out_df = pd.DataFrame(out_rows)
create_db_from_df(out_df, path_to_out_db)
