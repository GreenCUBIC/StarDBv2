import { json, error } from "@sveltejs/kit";
import { executeScript } from "$lib/utils"
import type { RequestHandler } from "./$types";

export const GET: RequestHandler = async ({ url }) => {
  const geneName = url.searchParams.get("gene");
  const data = await executeScript("stardb2/estrous_cycle/query.py", "-n " + geneName);

  return json({ measurements: JSON.parse(data) });
};
