f"""Computes the average translation for each gene in both genders and generates
JSON files with the series in the following form:
{
    "<gene>": [RPKM_P1, RPKM_P4, RPKM_P7, RPKM_P14, RPKM_P35, RPKM_ADULT],
    ...
}

This data is latter used to produce the correlation coefficients.
"""

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

MALE_TRANSLATION_SERIES_FILE = os.getenv("GENE_TRANSLATION_SERIES_MALE")
FEMALE_TRANSLATION_SERIES_FILE = os.getenv("GENE_TRANSLATION_SERIES_MALE")

engine = get_db_connection("development")

# Retrieve the translation data
male_df = pd.read_sql(
    f"""SELECT ensembl_id, sex, age, AVG(rpkm)
        FROM gene_expression
        WHERE sex = 'male'
        GROUP BY ensembl_id, sex, age
        ORDER BY ensembl_id, age;
""",
    con=engine,
)
female_df = pd.read_sql(
    f"""SELECT ensembl_id, sex, age, AVG(rpkm)
        FROM gene_expression
        WHERE sex = 'female'
        GROUP BY ensembl_id, sex, age
        ORDER BY ensembl_id, age;
""",
    con=engine,
)

# Format them in a nice dictionary of gene_name -> list of average rpkm values (in order of period, i.e. P1, P4, P7, ...).
male_data = {}
for gene, g in male_df.groupby(["ensembl_id"]):
    male_data[gene[0]] = list(g['avg'])
    
female_data = {}
for gene, g in female_df.groupby(["ensembl_id"]):
    female_data[gene[0]] = list(g['avg'])
 
# Save those results
open(MALE_TRANSLATION_SERIES_FILE, "w").write(json.dumps(male_data, indent=4))
open(FEMALE_TRANSLATION_SERIES_FILE, "w").write(json.dumps(female_data, indent=4))