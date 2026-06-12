import { test, expect } from '@playwright/test'
import { readFileSync, existsSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import { sections } from '../../src/content'

// Content-drift safety net (contracts/content-map.md "Test obligation").
// Asserts the section/source contract holds without a backend or a browser.

const here = dirname(fileURLToPath(import.meta.url))
// coach-site/tests/e2e -> repo root is three levels up.
const repoRoot = resolve(here, '..', '..', '..')

const EXPECTED_IDS = ['prepare', 'timeline', 'framing', 'help', 'troubleshooting', 'assess']

test.describe('content map contract', () => {
  test('there are exactly six sections with the expected ids, once each', () => {
    expect(sections).toHaveLength(EXPECTED_IDS.length)
    const ids = sections.map((s) => s.id).sort()
    expect(ids).toEqual([...EXPECTED_IDS].sort())
  })

  for (const id of EXPECTED_IDS) {
    test(`section "${id}" has non-empty blocks and a resolvable source`, () => {
      const section = sections.find((s) => s.id === id)
      expect(section, `section ${id} must exist`).toBeTruthy()
      if (!section) return

      // Every section must render content.
      expect(section.blocks.length).toBeGreaterThan(0)

      // Source may name one or more repo files (joined with " + ").
      const files = section.source.split('+').map((f) => f.trim())
      expect(files.length).toBeGreaterThan(0)
      for (const file of files) {
        const abs = resolve(repoRoot, file)
        expect(existsSync(abs), `source file not found: ${file}`).toBe(true)
        // Non-empty source file.
        expect(readFileSync(abs, 'utf8').length).toBeGreaterThan(0)
      }
    })
  }

  test('every block satisfies its non-empty validation rules', () => {
    for (const section of sections) {
      for (const block of section.blocks) {
        if (block.kind === 'checklist') {
          expect(block.items.length, `${section.id} checklist`).toBeGreaterThan(0)
          for (const item of block.items) expect(item.trim().length).toBeGreaterThan(0)
        }
        if (block.kind === 'troubleshoot') {
          expect(block.symptom.trim().length, `${section.id} symptom`).toBeGreaterThan(0)
          expect(block.fix.trim().length, `${section.id} fix`).toBeGreaterThan(0)
        }
      }
    }
  })
})
