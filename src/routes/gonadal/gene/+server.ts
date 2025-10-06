import { json, error } from "@sveltejs/kit";
import { estrousDbPool } from "$lib/db";
import type { RequestHandler } from "./$types";

const geneQuery = `
SELECT sub.sample_id, gene_name, ensembl_id, stage, rpkm
FROM (
    SELECT sample_id, gene.gene_name, measurement.ensembl_id, rpkm
    FROM gene JOIN measurement ON gene.ensembl_id = measurement.ensembl_id
    WHERE gene.gene_name = $1::text
) AS sub
JOIN sample ON sample.sample_id = sub.sample_id;
`;

export const GET: RequestHandler = async ({ url }) => {
  const geneName = url.searchParams.get("gene");
  const res = await estrousDbPool.query(geneQuery, [geneName]);

  return json({ measurements: res.rows });
};
