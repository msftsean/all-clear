import type { ContentBlock } from '../content/types'
import Checklist from './Checklist'
import CalloutCard from './CalloutCard'

interface ContentBlocksProps {
  blocks: ContentBlock[]
}

export default function ContentBlocks({ blocks }: ContentBlocksProps) {
  return (
    <div className="space-y-5">
      {blocks.map((block, i) => (
        <div key={i} data-reveal>
          <BlockRenderer block={block} />
        </div>
      ))}
    </div>
  )
}

function BlockRenderer({ block }: { block: ContentBlock }) {
  switch (block.kind) {
    case 'heading':
      return block.level === 2 ? (
        <h2 className="text-xl font-semibold text-ink mt-4 mb-1">{block.text}</h2>
      ) : (
        <h3 className="text-base font-semibold text-ink mt-2">{block.text}</h3>
      )

    case 'paragraph':
      return <p className="text-ink/75 leading-relaxed">{block.text}</p>

    case 'checklist':
      return <Checklist title={block.title} items={block.items} />

    case 'callout':
      return (
        <CalloutCard tone={block.tone} title={block.title}>
          {block.text}
        </CalloutCard>
      )

    case 'troubleshoot':
      return (
        <div className="card bg-amber/10 rounded-xl">
          <p className="font-semibold text-amber/80">
            <span className="text-ink/50 font-normal text-sm">Symptom: </span>
            {block.symptom}
          </p>
          {block.cause && (
            <p className="mt-2 text-ink/65 text-sm">
              <span className="font-semibold text-ink/80">Cause: </span>
              {block.cause}
            </p>
          )}
          <p className="mt-2 text-ink/80 text-sm">
            <span className="font-semibold text-sage">Fix: </span>
            {block.fix}
          </p>
        </div>
      )

    case 'lane':
      return (
        <div className="card bg-cofounder-soft border-cofounder/20">
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
            <span className="h-2.5 w-2.5 rounded-full bg-cofounder" aria-hidden="true" />
            <h3 className="font-semibold text-ink">{block.name}</h3>
            <span className="text-sm font-medium text-cofounder">{block.outcome}</span>
          </div>
          <p className="mt-2 text-ink/75 leading-relaxed text-sm">{block.detail}</p>
        </div>
      )

    case 'schedule':
      return <ScheduleTable rows={block.rows} />

    case 'link':
      return (
        <p>
          <a
            href={block.href}
            className="inline-flex items-center gap-1 text-cofounder font-medium underline underline-offset-2 hover:text-cofounder-dark focus:outline-none focus-visible:ring-2 focus-visible:ring-cofounder focus-visible:ring-offset-2 rounded transition-colors"
            target={block.href.startsWith('http') ? '_blank' : undefined}
            rel={block.href.startsWith('http') ? 'noopener noreferrer' : undefined}
          >
            {block.label} →
          </a>
        </p>
      )

    default:
      return null
  }
}

type ScheduleRow = { start: string; end: string; block: string; lead: string; min: number }

/** Run-of-show schedule: a table on >=sm, stacked cards on mobile (no h-scroll). */
function ScheduleTable({ rows }: { rows: ScheduleRow[] }) {
  const total = rows.reduce((sum, r) => sum + r.min, 0)
  return (
    <div>
      {/* Desktop / tablet: real table */}
      <div className="hidden sm:block card p-0 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <caption className="sr-only">Run of show schedule</caption>
          <thead>
            <tr className="bg-cofounder-soft">
              <th scope="col" className="px-4 py-2.5 text-xs font-semibold uppercase tracking-wide text-ink/70 whitespace-nowrap">
                Time
              </th>
              <th scope="col" className="px-4 py-2.5 text-xs font-semibold uppercase tracking-wide text-ink/70">
                Block
              </th>
              <th scope="col" className="px-4 py-2.5 text-xs font-semibold uppercase tracking-wide text-ink/70 whitespace-nowrap">
                Lead
              </th>
              <th scope="col" className="px-4 py-2.5 text-xs font-semibold uppercase tracking-wide text-ink/70 text-right">
                Min
              </th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i} className="border-t border-border hover:bg-cofounder-soft/40 transition-colors">
                <td className="px-4 py-3 font-medium text-cofounder whitespace-nowrap tabular-nums">
                  {r.start}–{r.end}
                </td>
                <td className="px-4 py-3 text-ink font-medium">{r.block}</td>
                <td className="px-4 py-3 text-ink/65 whitespace-nowrap">{r.lead}</td>
                <td className="px-4 py-3 text-right text-ink/55 tabular-nums">{r.min}</td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr className="border-t border-border bg-paper">
              <td className="px-4 py-2.5 text-xs font-semibold uppercase tracking-wide text-ink/60" colSpan={3}>
                Total
              </td>
              <td className="px-4 py-2.5 text-right font-semibold text-ink tabular-nums">{total}</td>
            </tr>
          </tfoot>
        </table>
      </div>

      {/* Mobile: stacked cards */}
      <ul className="sm:hidden space-y-2" role="list">
        {rows.map((r, i) => (
          <li key={i} className="card flex items-center justify-between gap-3 py-3">
            <div className="min-w-0">
              <p className="text-sm font-medium text-cofounder tabular-nums">
                {r.start}–{r.end}
              </p>
              <p className="text-ink font-medium">{r.block}</p>
              <p className="text-ink/60 text-sm">{r.lead}</p>
            </div>
            <span className="flex-shrink-0 inline-flex items-center justify-center min-w-[2.75rem] px-2.5 py-1 rounded-pill bg-cofounder-soft text-cofounder text-sm font-semibold tabular-nums">
              {r.min}m
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}
