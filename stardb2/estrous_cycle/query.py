import sys
import os
import argparse
import json

import pandas as pd

from stardb2.db import get_db_connection

engine = get_db_connection('estrous_cycle')

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--id', type=str, required=False, help="Ensembl ID of the gene.")
parser.add_argument('-n', '--name', type=str, required=False, help="Name of the gene.")
args = vars(parser.parse_args())

if args['id']:
    gene_id_to_name = json.load(open(os.getenv('ENSEMBL_ID_TO_GENE_NAME_MAP_ESTROUS')))
    gene = gene_id_to_name[args['id']]
    gene_id = args['id']
else: 
    gene_name_to_id = json.load(open(os.getenv('GENE_NAME_TO_ENSEMBL_ID_MAP_ESTROUS')))
    gene = args['name']
    gene_id = gene_name_to_id[gene]
    
query = f"""
SELECT sub.sample_id, gene_name, ensembl_id, stage, rpkm
FROM (
    SELECT sample_id, gene.gene_name, measurement.ensembl_id, rpkm
    FROM gene JOIN measurement ON gene.ensembl_id = measurement.ensembl_id
    WHERE gene.gene_name = '{gene}'
) AS sub
JOIN sample ON sample.sample_id = sub.sample_id;
"""

df = pd.read_sql(query, con=engine)

groups = df.groupby(['gene_name', 'stage'])
mean = groups['rpkm'].mean()
stderr = groups['rpkm'].sem(ddof=0)
size = groups['rpkm'].size()


merged = pd.concat([mean, stderr, size], axis=1)
merged.columns = ["mean", "error", "n"]

merged['gene_name'] = len(merged) * [gene]
merged['ensembl_id'] = len(merged) * [gene_id]
merged['stage'] = list(groups['stage'].max())

print(json.dumps(merged.to_dict(orient="records")))