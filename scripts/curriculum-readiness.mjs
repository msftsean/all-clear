#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_ROOT = path.resolve(SCRIPT_DIR, "..");

const REQUIRED_ARTIFACTS = [
  ["S0", "labs/00-setup/README.md"],
  ["S0", "labs/00-setup/SPEC.md"],
  ["S0", "labs/00-setup/verify_environment.py"],
  ["S1", "labs/01-understanding-agents/README.md"],
  ["S1", "labs/01-understanding-agents/SPEC.md"],
  ["S2", "labs/04-build-rag-pipeline/README.md"],
  ["S2", "labs/04-build-rag-pipeline/SPEC.md"],
  ["S2", "labs/04-build-rag-pipeline/verify_index.py"],
  ["S3", "labs/02-azure-mcp-setup/README.md"],
  ["S3", "labs/02-azure-mcp-setup/SPEC.md"],
  ["S3", "labs/07-mcp-server/README.md"],
  ["S3", "labs/07-mcp-server/SPEC.md"],
  ["S4", "labs/08-apim-gateway/README.md"],
  ["S4", "labs/08-apim-gateway/SPEC.md"],
  ["S5", "labs/06-deploy-with-azd/README.md"],
  ["S5", "labs/06-deploy-with-azd/SPEC.md"],
  ["S5", "labs/09-github-in-the-lab/README.md"],
  ["S5", "labs/09-github-in-the-lab/test_starter_red_to_green.py"],
];

const REQUIRED_WORKFLOWS = ["smoke-test.yml", "allclear-backend-ci.yml"];
const RETIRED_GOVERNANCE_REFS = [
  "shared/constitution.md",
  "shared\\constitution.md",
];

function displayPath(root, file) {
  return path.relative(root, file).split(path.sep).join("/");
}

function lineNumber(text, index) {
  return text.slice(0, index).split("\n").length;
}

function readText(file) {
  return fs.readFileSync(file, "utf8");
}

function walk(root, predicate) {
  const found = [];
  function visit(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      if ([".git", "node_modules", "__pycache__"].includes(entry.name)) continue;
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) visit(absolute);
      else if (predicate(absolute)) found.push(absolute);
    }
  }
  visit(root);
  return found;
}

function sourceFiles(root) {
  const files = [];
  const labs = path.join(root, "labs");
  if (fs.existsSync(labs)) files.push(...walk(labs, (file) => file.endsWith(".md")));
  const runbook = path.join(root, "participant-runbook", "index.html");
  if (fs.existsSync(runbook)) files.push(runbook);
  return files;
}

function curriculumFiles(root) {
  const files = sourceFiles(root);
  const labs = path.join(root, "labs");
  if (fs.existsSync(labs)) {
    files.push(...walk(labs, (file) => /\.(?:py|js)$/.test(file)));
  }
  return files;
}

function isExternal(destination) {
  return /^(?:[a-z][a-z\d+.-]*:|\/\/)/i.test(destination)
    || destination.startsWith("#");
}

function localDestinations(file, text) {
  const results = [];
  const pattern = file.endsWith(".html")
    ? /(?:href|src)\s*=\s*["']([^"']+)["']/gi
    : /!?\[[^\]]*\]\((?:<([^>]+)>|([^) \t]+))(?:\s+["'][^"']*["'])?\)/g;
  for (const match of text.matchAll(pattern)) {
    const destination = file.endsWith(".html") ? match[1] : (match[1] || match[2]);
    if (!destination || isExternal(destination)) continue;
    results.push({ destination, index: match.index ?? 0 });
  }
  return results;
}

function checkLocalLinks(root, errors) {
  for (const file of sourceFiles(root)) {
    const text = readText(file);
    for (const { destination, index } of localDestinations(file, text)) {
      const [rawPath] = destination.split("#", 1);
      if (!rawPath) continue;
      const target = rawPath.startsWith("/")
        ? path.resolve(root, "participant-runbook", rawPath.slice(1))
        : path.resolve(path.dirname(file), rawPath);
      if (!target.startsWith(`${root}${path.sep}`) && target !== root) {
        errors.push(`${displayPath(root, file)}:${lineNumber(text, index)} local link escapes the repository: ${destination}`);
      } else if (!fs.existsSync(target)) {
        errors.push(`${displayPath(root, file)}:${lineNumber(text, index)} broken local link: ${destination}`);
      }
    }
  }
}

function checkGovernanceReferences(root, errors) {
  const canonical = path.join(root, ".specify", "memory", "constitution.md");
  if (!fs.existsSync(canonical)) {
    errors.push("required governance file is missing: .specify/memory/constitution.md");
  }
  for (const file of sourceFiles(root)) {
    const text = readText(file);
    for (const retired of RETIRED_GOVERNANCE_REFS) {
      let start = 0;
      while (true) {
        const index = text.indexOf(retired, start);
        if (index < 0) break;
        errors.push(`${displayPath(root, file)}:${lineNumber(text, index)} references deleted governance file ${retired}; use .specify/memory/constitution.md`);
        start = index + retired.length;
      }
    }
  }
}

function checkArtifacts(root, errors) {
  for (const [stage, relative] of REQUIRED_ARTIFACTS) {
    if (!fs.existsSync(path.join(root, relative))) {
      errors.push(`${stage} is missing required artifact: ${relative}`);
    }
  }
}

function parseMinutes(value) {
  const match = value.match(/(\d+)\s*min/i);
  return match ? Number(match[1]) : null;
}

function clockMinutes(hour, minute, meridiem) {
  let normalized = Number(hour) % 12;
  if (meridiem.toLowerCase() === "pm") normalized += 12;
  return normalized * 60 + Number(minute);
}

function checkSchedule(root, errors) {
  const file = path.join(root, "participant-runbook", "index.html");
  if (!fs.existsSync(file)) return;
  const text = readText(file);
  const agenda = text.match(/<section id="agenda">([\s\S]*?)<\/section>/i)?.[1];
  if (!agenda) {
    errors.push("participant-runbook/index.html is missing the agenda section");
    return;
  }
  const total = Number(
    agenda.match(/totalling\s*<strong>(\d+)\s*minutes/i)?.[1]
    || agenda.match(/<span[^>]*class="pill"[^>]*>(\d+)\s*minutes/i)?.[1]
    || NaN,
  );
  const clock = agenda.match(/(\d{1,2}):(\d{2})\s*AM[^0-9]+(\d{1,2}):(\d{2})\s*PM/i);
  const clockCells = [...agenda.matchAll(/<td>(\d{1,2}):(\d{2})\s*(?:&ndash;|[-–])\s*(\d{1,2}):(\d{2})<\/td>/gi)];
  const durations = [...agenda.matchAll(/<td>(?:<strong>[^<]+<\/strong>)?\s*(\d+)\s*min(?:ute)?s?<\/td>/gi)].map((match) => Number(match[1]));
  if (!Number.isFinite(total) || (!clock && clockCells.length === 0) || durations.length === 0) {
    errors.push("participant-runbook/index.html agenda must declare total minutes, clock bounds, and stage durations");
    return;
  }
  const firstClock = clockCells[0]?.slice(1) || clock?.slice(1);
  const lastClock = clockCells.at(-1)?.slice(3) || clock?.slice(3);
  const elapsed = firstClock && lastClock
    ? (clockMinutes(lastClock[0], lastClock[1], Number(lastClock[0]) < 8 ? "PM" : "AM")
      - clockMinutes(firstClock[0], firstClock[1], Number(firstClock[0]) < 8 ? "PM" : "AM"))
    : NaN;
  const stageTotal = durations.reduce((sum, value) => sum + value, 0);
  const hasBreak = /\b(?:break|lunch|buffer|slack)\b/i.test(agenda);
  if (stageTotal !== total) {
    errors.push(`agenda stage durations total ${stageTotal} minutes but declaration says ${total}`);
  }
  if (total > elapsed) {
    errors.push(`agenda declares ${total} minutes in a ${elapsed}-minute window`);
  } else if (total === elapsed && !hasBreak) {
    errors.push(`agenda fills the entire ${elapsed}-minute window with stages and declares no break or buffer`);
  }
}

function checkWorkflows(root, errors) {
  const workflowDirectory = path.join(root, ".github", "workflows");
  for (const workflow of REQUIRED_WORKFLOWS) {
    if (!fs.existsSync(path.join(workflowDirectory, workflow))) {
      errors.push(`required workflow is stale or missing: .github/workflows/${workflow}`);
    }
  }
  for (const file of sourceFiles(root)) {
    const text = readText(file);
    for (const match of text.matchAll(/(?:\.github\/workflows\/)?([A-Za-z0-9._-]*(?:workflow|smoke|ci|deploy)[A-Za-z0-9._-]*\.yml)\b/gi)) {
      const workflow = match[1];
      if (!fs.existsSync(path.join(workflowDirectory, workflow))) {
        errors.push(`${displayPath(root, file)}:${lineNumber(text, match.index ?? 0)} references stale workflow ${workflow}`);
      }
    }
  }
}

function checkCompletionGates(root, errors) {
  const files = curriculumFiles(root);
  for (const file of files) {
    const text = readText(file);
    const matches = [...text.matchAll(/\b[A-Z][A-Z0-9_]*(?:COMPLETE|COMPLETED|DONE|PASS|GATE)[A-Z0-9_]*\b/g)];
    if (!matches.length) continue;
    for (const match of matches) {
      const variable = match[0];
      const readsVariable = new RegExp(
        `(?:os\\.getenv|os\\.environ\\.get|os\\.environ\\[|getenv|process\\.env\\.)\\s*\\(?\\s*["']?${variable}\\b`,
      ).test(text);
      const stripsVariable = new RegExp(`\\.pop\\s*\\(\\s*["']${variable}["']`).test(text);
      if (readsVariable && !stripsVariable) {
        errors.push(`${displayPath(root, file)}:${lineNumber(text, match.index ?? 0)} participant completion gate relies on environment variable ${variable}; require observable exercise evidence instead`);
        break;
      }
    }
  }
}

export function verifyCurriculum(root = DEFAULT_ROOT) {
  const errors = [];
  checkLocalLinks(root, errors);
  checkGovernanceReferences(root, errors);
  checkArtifacts(root, errors);
  checkSchedule(root, errors);
  checkWorkflows(root, errors);
  checkCompletionGates(root, errors);
  return errors;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const root = path.resolve(process.argv[2] || DEFAULT_ROOT);
  const errors = verifyCurriculum(root);
  if (errors.length) {
    console.error(`Curriculum readiness FAILED with ${errors.length} issue(s):`);
    for (const error of errors) console.error(`- ${error}`);
    process.exitCode = 1;
  } else {
    console.log("Curriculum readiness PASSED: links, governance, artifacts, schedule, workflows, and completion gates are valid.");
  }
}
