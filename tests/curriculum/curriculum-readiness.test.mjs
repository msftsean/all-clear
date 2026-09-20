import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { verifyCurriculum } from "../../scripts/curriculum-readiness.mjs";

function fixture(files) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "all-clear-readiness-"));
  for (const [relative, content] of Object.entries(files)) {
    const file = path.join(root, relative);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, content);
  }
  return root;
}

const artifacts = {
  "labs/00-setup/README.md": "",
  "labs/00-setup/SPEC.md": "",
  "labs/00-setup/verify_environment.py": "",
  "labs/01-understanding-agents/README.md": "",
  "labs/01-understanding-agents/SPEC.md": "",
  "labs/04-build-rag-pipeline/README.md": "",
  "labs/04-build-rag-pipeline/SPEC.md": "",
  "labs/04-build-rag-pipeline/verify_index.py": "",
  "labs/02-azure-mcp-setup/README.md": "",
  "labs/02-azure-mcp-setup/SPEC.md": "",
  "labs/07-mcp-server/README.md": "",
  "labs/07-mcp-server/SPEC.md": "",
  "labs/08-apim-gateway/README.md": "",
  "labs/08-apim-gateway/SPEC.md": "",
  "labs/06-deploy-with-azd/README.md": "",
  "labs/06-deploy-with-azd/SPEC.md": "",
  "labs/09-github-in-the-lab/README.md": "",
  "labs/09-github-in-the-lab/test_starter_red_to_green.py": "",
  ".specify/memory/constitution.md": "# Constitution",
  ".github/workflows/smoke-test.yml": "",
  ".github/workflows/allclear-backend-ci.yml": "",
};

test("passes a complete curriculum fixture", () => {
  const root = fixture({
    ...artifacts,
    "participant-runbook/index.html": `
      <section id="agenda">
        <p>Six stages totalling <strong>360 minutes</strong> in a 10:00 AM - 5:00 PM window.</p>
        <p>Break: 60 minutes.</p>
        <td>60 min</td><td>60 min</td><td>60 min</td><td>60 min</td><td>60 min</td><td>60 min</td>
      </section>
      <a href="../labs/00-setup/README.md">lab</a>
    `,
  });
  assert.deepEqual(verifyCurriculum(root), []);
});

test("reports broken links, missing artifacts, stale workflows, and env gates", () => {
  const root = fixture({
    ...artifacts,
    "participant-runbook/index.html": `
      <section id="agenda">
        <p>Six stages totalling <strong>390 minutes</strong> in a 11:00 AM - 5:30 PM window.</p>
        <td>45 min</td><td>90 min</td><td>60 min</td><td>75 min</td><td>60 min</td><td>60 min</td>
      </section>
      <a href="../labs/missing/README.md">missing</a>
    `,
    "labs/09-github-in-the-lab/README.md": "Run old-workflow.yml with completion flag.",
    "labs/09-github-in-the-lab/test_starter_red_to_green.py": "os.getenv('ALL_CLEAR_LAB09_COMPLETE')",
  });
  fs.rmSync(path.join(root, "labs/08-apim-gateway/SPEC.md"));
  const errors = verifyCurriculum(root).join("\n");
  assert.match(errors, /broken local link/);
  assert.match(errors, /missing required artifact/);
  assert.match(errors, /stale workflow old-workflow\.yml/);
  assert.match(errors, /fills the entire/);
  assert.match(errors, /environment variable ALL_CLEAR_LAB09_COMPLETE/);
});

test("reports deleted governance references", () => {
  const root = fixture({
    ...artifacts,
    "participant-runbook/index.html": `
      <section id="agenda">
        <p>Six stages totalling <strong>360 minutes</strong> in a 10:00 AM - 5:00 PM window. Break 60 minutes.</p>
        <td>60 min</td><td>60 min</td><td>60 min</td><td>60 min</td><td>60 min</td><td>60 min</td>
      </section>
    `,
    "labs/03-spec-driven-development/README.md": "Use shared/constitution.md.",
  });
  assert.match(verifyCurriculum(root).join("\n"), /deleted governance file shared\/constitution\.md/);
});
