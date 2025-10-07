import json
import os
import sys
import math
import warnings

warnings.filterwarnings("ignore")

import pandas as pd
import dotenv

from stardb2.db import get_db_connection

dotenv.load_dotenv()

genes = sys.argv[1:]
ensembl_id_to_gene = json.load(open(os.getenv('GENE_NAME_TO_ENSEMBL_ID_MAP')))
genes_string = ','.join([f"'{ensembl_id_to_gene[x]}'" for x in genes])

engine = get_db_connection("development")

df = pd.read_sql(
    f"""    SELECT gene_expression.ensembl_id, gene_name, sex, age, rpkm
            FROM gene_expression
            JOIN gene ON gene_expression.ensembl_id = gene.ensembl_id
            WHERE gene_expression.ensembl_id = ANY(ARRAY[{genes_string}])
            ORDER BY gene_expression.ensembl_id, sex, age
""",
    con=engine,
)

df['age'] = df['age'].apply(lambda x: x if x != 100 else 'adult')

print(df[['ensembl_id', 'gene_name', 'sex', 'age', 'rpkm']].to_csv(index=False))