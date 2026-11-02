import { appendFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const file = resolve(dirname(fileURLToPath(import.meta.url)), "../../../qa/automation/results/fe-notes.jsonl");

export function note(id: string, text: string) {
  mkdirSync(dirname(file), { recursive: true });
  appendFileSync(file, JSON.stringify({ id, text }) + "\n");
}
