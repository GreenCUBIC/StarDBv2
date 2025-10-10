import { json, error } from "@sveltejs/kit";
import { developmentDbPool } from "$lib/db";
import type { RequestHandler } from "./$types";
import util from "util";
import { exec as execNonPromise } from "child_process";
import { executeScript } from "$lib/utils"

const exec = util.promisify(execNonPromise);

export const GET: RequestHandler = async ({ url }) => {

  const data = await executeScript("stardb2/development/download_gene_data.py", url.searchParams.get("gene"))

  return json({ measurements: JSON.parse(data) });
};
