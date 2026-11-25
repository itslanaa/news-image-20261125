import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const out = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const dir = path.dirname(fileURLToPath(import.meta.url));
fs.mkdirSync(out, { recursive: true });
fs.copyFileSync(path.join(dir, "entry.png"), path.join(out, "entry.png"));
