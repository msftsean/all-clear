# Curriculum readiness verifier

Run the repository-level curriculum gate from the repository root:

```bash
npm run curriculum:verify
```

The command checks participant-runbook HTML and lab Markdown links, canonical
governance references, required stage artifacts, schedule arithmetic and break
capacity, required GitHub workflow names, and completion gates. It exits
non-zero with file and line locations when a curriculum claim is stale,
missing, or only backed by an environment-variable toggle.
