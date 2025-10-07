import { json, error } from "@sveltejs/kit";
import { estrousDbPool } from "$lib/db";
import * as math from "mathjs";
import type { RequestHandler } from "./$types";
import { executeScript } from "$lib/utils"

export const GET: RequestHandler = async ({ url }) => {
  const genes = url.searchParams.get("query").split(",");

  const csv = await executeScript("stardb2/estrous_cycle/format_gene_data_to_csv.py", '-n ' + genes.join(" "))

  return new Response(csv, {
    status: 200,
    headers: {
      "Content-type": "text/csv",
      "Content-Disposition": `attachment; filename=trapseq_data.csv`,
    },
  });
};
