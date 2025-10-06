import { json, error } from "@sveltejs/kit";
import { developmentDbPool } from "$lib/db";
import type { RequestHandler } from "./$types";
import util from "util";
import { exec as execNonPromise } from "child_process";

const exec = util.promisify(execNonPromise);

export const GET: RequestHandler = async ({ url }) => {
  const genes = url.searchParams.get("gene").split(',').join(' ');

  const data = (await exec(`env/bin/python3 src/lib/scripts/download_development_data.py ${genes}`)).stdout

return new Response(data, {
    status: 200,
    headers: {
      "Content-type": "text/csv",
      "Content-Disposition": `attachment; filename=stardb_development_data.csv`,
    },
  });
};

