import util from "util";
import { exec as execNonPromise } from "child_process";

const exec = util.promisify(execNonPromise);

export const executeScript = async (scriptPath, args) => {
    const results = await exec(`PYTHONPATH=. env/bin/python3 ${scriptPath} ${args}`);
    return results.stdout
}