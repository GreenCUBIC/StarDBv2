import json
import sys
import math
import warnings

warnings.filterwarnings("ignore")

import pandas as pd

from db_connection import get_db_connection

engine = get_db_connection("development")
male_df = pd.read_sql(
    f"""SELECT ensembl_id, sex, age, AVG(rpkm) FROM gene_expression WHERE sex = 'male' GROUP BY ensembl_id, sex, age ORDER BY ensembl_id, age;
""",
    con=engine,
)
female_df = pd.read_sql(
    f"""SELECT ensembl_id, sex, age, AVG(rpkm) FROM gene_expression WHERE sex = 'female' GROUP BY ensembl_id, sex, age ORDER BY ensembl_id, age;
""",
    con=engine,
)

male_data = {}
for gene, g in male_df.groupby(["ensembl_id"]):
    male_data[gene[0]] = list(g['avg'])
    
female_data = {}
for gene, g in female_df.groupby(["ensembl_id"]):
    female_data[gene[0]] = list(g['avg'])
 
open('../../../data/development/male_data.json', "w").write(json.dumps(male_data, indent=4))
open('../../../data/development/female_data.json', "w").write(json.dumps(female_data, indent=4))