import { json, error } from "@sveltejs/kit";
import { developmentDbPool } from "$lib/db";
import type { RequestHandler } from "./$types";
import util from "util";
import { exec as execNonPromise } from "child_process";
import { readFile } from "fs/promises";

const exec = util.promisify(execNonPromise);

export const GET: RequestHandler = async ({ url }) => {
  const gene = url.searchParams.get("gene");

  const gene_id_query = await developmentDbPool.query("SELECT ensembl_id FROM gene WHERE gene_name = $1;", [gene]);
  const ensembl_id = gene_id_query.rows[0].ensembl_id;

  const data = await readFile(`data/development/correlations/${gene}.json`, 'utf-8')


  return json({ correlations: JSON.parse(data) });
};
