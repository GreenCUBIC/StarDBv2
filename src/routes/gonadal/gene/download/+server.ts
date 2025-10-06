import { json, error } from "@sveltejs/kit";
import { estrousDbPool } from "$lib/db";
import * as math from "mathjs";
import type { RequestHandler } from "./$types";

const geneQuery = `
SELECT sub.sample_id, gene_name, ensembl_id, stage, rpkm
FROM (
    SELECT sample_id, gene.gene_name, measurement.ensembl_id, rpkm
    FROM gene JOIN measurement ON gene.ensembl_id = measurement.ensembl_id
    WHERE gene.gene_name = ANY($1::text[])
) AS sub
JOIN sample ON sample.sample_id = sub.sample_id;
`;

export const GET: RequestHandler = async ({ url }) => {
  const genes = url.searchParams.get("query").split(",");
  const res = await estrousDbPool.query(geneQuery, [genes]);

  const groupedGenes = Object.groupBy(res.rows, (x) => x.gene_name);

  const data = Object.entries(groupedGenes)
    .map((gene) => {
      const stageGroups = Object.groupBy(gene[1], (x) => x.stage);
      return Object.entries(stageGroups).map((stageGroup) => {
        const mean = math.mean(stageGroup[1].map((x) => x.rpkm));
        const std =
          math.std(stageGroup[1].map((x) => x.rpkm)) /
          math.sqrt(stageGroup[1].length);
        return {
          gene_name: gene[0],
          stage: stageGroup[0],
          mean,
          std,
        };
      });
    })
    .flat(Infinity);

  const text =
    "gene_name,stage,mean_rpkm,std_rpkm\n" +
    data.map((x) => `${x.gene_name},${x.stage},${x.mean},${x.std}`).join("\n");

  return new Response(text, {
    status: 200,
    headers: {
      "Content-type": "text/csv",
      "Content-Disposition": `attachment; filename=trapseq_data.csv`,
    },
  });
};
