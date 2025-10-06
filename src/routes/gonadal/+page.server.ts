import { estrousDbPool } from "$lib/db";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({}) => {
  const res = await estrousDbPool.query("SELECT gene_name FROM gene;");
  const availableGenes = res.rows.map((x) => x.gene_name);
  return {
    availableGenes,
  };
};
