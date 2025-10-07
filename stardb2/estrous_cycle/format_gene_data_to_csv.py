import sys
import os
import argparse
import json

import pandas as pd

from stardb2.db import get_db_connection

engine = get_db_connection('estrous_cycle')

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--id', type=str, required=False, nargs='+', help="Ensembl ID of the gene.")
parser.add_argument('-n', '--name', type=str, required=False, nargs='+', help="Name of the gene.")
args = vars(parser.parse_args())

if args['id']:
    gene_id_to_name = json.load(open(os.getenv('ENSEMBL_ID_TO_GENE_NAME_MAP')))
    genes = [gene_id_to_name[i] for i in args['id']]
else: 
    genes = args['name']
    
gene_array = f"ARRAY[{','.join([f"'{g}'" for g in genes])}]"

query = f"""
SELECT gene_name, ensembl_id, stage, rpkm
FROM (
    SELECT sample_id, gene.gene_name, measurement.ensembl_id, rpkm
    FROM gene JOIN measurement ON gene.ensembl_id = measurement.ensembl_id
    WHERE gene.gene_name = ANY({gene_array})
) AS sub
JOIN sample ON sample.sample_id = sub.sample_id;
"""

df = pd.read_sql(query, con=engine)

group = df.groupby(['gene_name', 'stage'])

mean = group['rpkm'].mean()
std = group['rpkm'].sem(ddof=0)
df = pd.concat([mean, std], axis=1)
df.columns = ['mean_rpkm', 'stderr_rpkm']
df['gene_name'] = [x[0] for x in group.indices.keys()]
df['stage'] = [x[1] for x in group.indices.keys()]

print(df[['gene_name', 'stage', 'mean_rpkm', 'stderr_rpkm']].to_csv(index=False))