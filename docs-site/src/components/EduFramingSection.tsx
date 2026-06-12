import SectionHeader from './SectionHeader'

const capabilities = [
  { capability: 'Understands intent', evidence: 'QueryAgent extracts what the student needs from natural language instead of forcing a portal choice.' },
  { capability: 'Routes responsibly', evidence: 'RouterAgent maps the request to IT, registrar, financial aid, student affairs, housing, accessibility, or crisis support.' },
  { capability: 'Acts with context', evidence: 'ActionAgent creates tickets, retrieves knowledge articles, checks status, and preserves session continuity.' },
  { capability: 'Speaks and listens', evidence: 'Voice and text share the same pipeline, so accessibility and preference do not split the support experience.' },
  { capability: 'Earns operational trust', evidence: 'Health endpoints, session IDs, modality logs, kill switch, and graceful fallback give IT administrators confidence.' },
]

export default function EduFramingSection() {
  return (
    <section id="edu-framing" className="scroll-mt-24 reveal reveal-delay-3">
      <SectionHeader icon="🎓" title="EDU Framing" id="edu-framing-heading" />
      <div className="space-y-8">
        <article className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover">
          <h3 className="text-mercury-blue font-medium text-lg mb-4">The “47 Front Doors” Problem</h3>
          <p className="text-silver mb-4">
            Universities have built specialized systems for every office, but students experience them as fragmentation. The burden of routing falls on the person least equipped to route: a stressed student trying to get help.
          </p>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.18em] text-lead font-mono mb-2">Before</p>
              <pre className="text-xs text-silver">{`Student need
  ├─ IT portal
  ├─ LMS helpdesk
  ├─ Registrar form
  ├─ Financial aid queue
  ├─ Advising email
  ├─ Housing desk
  └─ Accessibility office`}</pre>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.18em] text-lead font-mono mb-2">After</p>
              <pre className="text-xs text-mercury-blue/80">{`Student need
  └─ 47 Doors
       ├─ Understands
       ├─ Routes
       ├─ Acts
       └─ Follows up`}</pre>
            </div>
          </div>
          <blockquote className="mt-5 border-l-4 border-mercury-blue/50 pl-4 py-3 bg-mercury-blue/5 rounded-r-xl text-silver text-sm">
            “We are not replacing campus teams. We are replacing confusion at the front door with a colleague who knows where to send the student and how to keep them moving.”
          </blockquote>
        </article>

        <article className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover">
          <h3 className="text-mercury-blue font-medium text-lg mb-4">Trusted Digital Colleague</h3>
          <div className="overflow-x-auto rounded-xl border border-lead/50">
            <table>
              <thead><tr><th>Capability</th><th>What to Show in the Demo</th></tr></thead>
              <tbody>
                {capabilities.map((row) => (
                  <tr key={row.capability}>
                    <td className="font-medium text-starlight">{row.capability}</td>
                    <td className="text-silver">{row.evidence}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>

        <article className="bg-midnight-slate border border-lead/50 rounded-2xl p-6 card-hover">
          <h3 className="text-mercury-blue font-medium text-lg mb-4">Applicable to Any University</h3>
          <p className="text-silver mb-4">
            The departments, knowledge base, ticket systems, and escalation policies can change from campus to campus; the pattern stays the same. Every institution has a front-door problem, a trust problem, and a continuity problem. 47 Doors is a composable pattern for replacing scattered entry points with a single conversational layer that meets students where they are — by text or by voice.
          </p>
          <ul className="feature-list">
            <li><span className="text-mercury-blue">●</span><span>Start with the highest-volume student questions, then expand routing as institutional confidence grows.</span></li>
            <li><span className="text-mercury-blue">●</span><span>Keep humans in the loop with tickets, escalation, and transparent session trails.</span></li>
            <li><span className="text-mercury-blue">●</span><span>Use voice as an accessibility and convenience layer, not a separate product silo.</span></li>
          </ul>
          <blockquote className="mt-5 border-l-4 border-mercury-blue/50 pl-4 py-3 bg-mercury-blue/5 rounded-r-xl text-silver text-sm">
            “The outcome is simple: fewer doors for students, better context for staff, and a support experience that feels like the university is listening.”
          </blockquote>
        </article>
      </div>
    </section>
  )
}
