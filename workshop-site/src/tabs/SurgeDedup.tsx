import CollapsibleNotes from '../components/CollapsibleNotes'
import CalloutCard from '../components/CalloutCard'

export default function SurgeDedup() {
  return (
    <div role="tabpanel" id="surge-panel" aria-labelledby="surge-tab">
      <div className="max-w-5xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Hero scenario</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">A surge should grow magnitude, not queue noise</h2>
        <p className="text-xl text-ink/70 mb-10">All Clear compares each classified signal with open incidents in the same intent category.</p>

        <div className="grid md:grid-cols-2 gap-6 mb-10">
          <article className="card border-2 border-brand">
            <p className="mono-label text-ink/60">Similarity at or above threshold</p>
            <h3 className="font-semibold text-2xl my-3">ATTACH_TO_INCIDENT</h3>
            <ul className="space-y-2">
              <li>Signal becomes a report on the existing incident.</li>
              <li>Magnitude increments atomically.</li>
              <li>Reporter receives a short acknowledgment.</li>
              <li>No knowledge search keeps surge latency flat.</li>
            </ul>
          </article>
          <article className="card">
            <p className="mono-label text-ink/60">Similarity below threshold</p>
            <h3 className="font-semibold text-2xl my-3">OPEN_INCIDENT</h3>
            <ul className="space-y-2">
              <li>A new AC identifier is created.</li>
              <li>Severity, queue, and SLA are persisted.</li>
              <li>ActionAgent can search approved knowledge.</li>
              <li>The response includes grounded citations.</li>
            </ul>
          </article>
        </div>

        <div className="card">
          <h3 className="font-semibold text-xl mb-4">Surge replay: what good looks like</h3>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div><div className="stat-number">40</div><div className="stat-label">signals preserved</div></div>
            <div><div className="stat-number">1</div><div className="stat-label">incident operated</div></div>
            <div><div className="stat-number">40</div><div className="stat-label">magnitude shown</div></div>
          </div>
        </div>

        <CalloutCard title="Default comparison rule">
          Dedup uses embedding similarity against open incidents in the same intent category. The configured default threshold is 0.83 cosine similarity.
        </CalloutCard>

        <CollapsibleNotes>
          <p>The important tradeoff is precision versus fragmentation. A threshold that is too low combines unrelated events; one that is too high creates duplicate incidents and hides the true surge.</p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
