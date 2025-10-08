import { Client, Pool } from "pg";
import { DB_USER, DB_HOST, DB_PASSWORD, DB_PORT } from "$env/dynamic/private";

const developmentDbPool = new Pool({
  user: DB_USER,
  password: DB_PASSWORD,
  host: DB_HOST,
  port: DB_PORT,
  database: "development",
  max: 2,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
  maxLifetimeSeconds: 60,
});

const estrousDbPool = new Pool({
  user: DB_USER,
  password: DB_PASSWORD,
  host: DB_HOST,
  port: DB_PORT,
  database: "estrous_cycle",
  max: 2,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
  maxLifetimeSeconds: 60,
});

export { developmentDbPool, estrousDbPool };
