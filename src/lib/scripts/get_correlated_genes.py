import argparse
import json
import os
import multiprocessing as mp

import scipy
import tqdm
import dotenv
import pandas as pd
import numpy

dotenv.load_dotenv()

from db_connection import get_db_connection

engine = get_db_connection("development")
genes_df = pd.read_sql(
    f"""SELECT * FROM gene;
""",
    con=engine,
)
male_data = json.load(open(os.getenv('GENE_EXPRESSION_SERIES_MALE')))
female_data = json.load(open(os.getenv('GENE_EXPRESSION_SERIES_FEMALE')))

genes_dict = { x['ensembl_id']: x['gene_name'] for i, x in genes_df.iterrows() }

def run(target_gene):
    
    other_genes = set(male_data.keys()).difference(target_gene)
    
    correlations = {
        'male': {},
        'female': {},
        'both': {}
    }
    
    gene_name_correlations = {
        'male': {},
        'female': {},
        'both': {}
    }
    
    target_gene_series_male = male_data[target_gene]
    target_gene_series_female = female_data[target_gene]
    for gene in other_genes:
        correlations['male'][gene] = scipy.stats.pearsonr(target_gene_series_male, male_data[gene]).statistic
        correlations['female'][gene] = scipy.stats.pearsonr(target_gene_series_female, female_data[gene]).statistic
        correlations['both'][gene] = numpy.mean([correlations['male'][gene], correlations['female'][gene]])
        
    correlations['male'] = sorted(correlations['male'].items(), key=lambda x: abs(x[1]), reverse=True)
    correlations['female'] = sorted(correlations['female'].items(), key=lambda x: abs(x[1]), reverse=True)
    correlations['both'] = sorted(correlations['both'].items(), key=lambda x: abs(x[1]), reverse=True)
    
    if args['top']:
        correlations['male'] = correlations['male'][:args['top']]
        correlations['female'] = correlations['female'][:args['top']]
        correlations['both'] = correlations['both'][:args['top']]
        
    correlations['male'] = [{'ensembl_id': x[0], 'gene_name': genes_dict[x[0]], 'correlation': x[1] } for x in correlations['male']]
    correlations['female'] = [{'ensembl_id': x[0], 'gene_name': genes_dict[x[0]], 'correlation': x[1] } for x in correlations['female']]
    correlations['both'] = [{'ensembl_id': x[0], 'gene_name': genes_dict[x[0]], 'correlation': x[1] } for x in correlations['both']]
        
    if args['output']:
        open(f"{args['output']}/{genes_dict[target_gene]}.json", 'w').write(json.dumps(correlations, indent=2))

def main(args):
    jobs = genes_dict.keys()
    
            
    with mp.Pool(15) as pool:
      r = list(tqdm.tqdm(pool.imap(run, jobs), total=len(jobs)))
    #print(json.dumps(correlations, indent=2))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ensembl_id', type=str, required=True, help='Ensembl ID of the gene for which correlations are to be retrieved.')
    parser.add_argument('-t', '--top', type=int, required=False, help='Number of most correlated genes to return.')
    parser.add_argument('-o', '--output', type=str, required=False, help='output file.')
    args = vars(parser.parse_args())
    

    main(args)