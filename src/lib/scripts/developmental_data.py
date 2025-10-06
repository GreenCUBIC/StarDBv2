import json
import sys
import math
import warnings

warnings.filterwarnings("ignore")

import pandas as pd

from db_connection import get_db_connection

engine = get_db_connection("development")
df = pd.read_sql(
    f"""SELECT SUB.ensembl_id, sex, age, rpkm
FROM (
    SELECT ensembl_id
    FROM gene
    WHERE gene.gene_name = '{sys.argv[1]}'
) AS sub
 JOIN gene_expression
 ON sub.ensembl_id = gene_expression.ensembl_id;
""",
    con=engine,
)

data = {"male": [], "female": []}
for _, group in df.groupby("sex"):
    sex = group.iloc[0]["sex"]
    for _, subgroup in group.groupby("age"):
        age = subgroup.iloc[0]["age"]
        mean_rpkm = subgroup.rpkm.mean()
        std_rpkm = subgroup.rpkm.std() / math.sqrt(len(subgroup))
        data[sex].append({"age": int(age), "mean_rpkm": float(mean_rpkm), "std_rpkm": float(std_rpkm)})

    data[sex] = sorted(data[sex], key=lambda x: int(x["age"]))


print(json.dumps(data))
