import CollapsibleNotes from '../components/CollapsibleNotes'
import CalloutCard from '../components/CalloutCard'
import DiagramSVG from '../components/DiagramSVG'

export default function VoicePhone() {
  return (
    <div role="tabpanel" id="voice-phone-panel" aria-labelledby="voice-phone-tab">
      <div className="max-w-5xl mx-auto">
        <p className="mono-label text-ink/70 mb-3">Multi-channel intake</p>
        <h2 className="text-4xl font-semibold tracking-tight text-dark-text mb-4">Different transports, one signal contract</h2>
        <p className="text-xl text-ink/70 mb-10">Text, browser voice, and phone calls converge before classification. None receives extra authority.</p>

        <DiagramSVG
          title="Voice and phone converge on the All Clear pipeline"
          description="Browser voice uses WebRTC and phone uses a telephony bridge; both produce signals for the same pipeline."
          viewBox="0 0 900 300"
        >
          <rect x="40" y="55" width="170" height="60" rx="5" fill="#F7F8FA" stroke="#1B1B1F" strokeWidth="2" />
          <text x="125" y="91" textAnchor="middle" fontSize="14" fill="#1B1B1F">Browser voice</text>
          <rect x="40" y="185" width="170" height="60" rx="5" fill="#F7F8FA" stroke="#1B1B1F" strokeWidth="2" />
          <text x="125" y="221" textAnchor="middle" fontSize="14" fill="#1B1B1F">Phone call</text>
          <path d="M 215 85 L 370 145" stroke="#0F6CBD" strokeWidth="3" />
          <path d="M 215 215 L 370 155" stroke="#0F6CBD" strokeWidth="3" />
          <rect x="370" y="110" width="180" height="80" rx="5" fill="#0F6CBD" stroke="#1B1B1F" strokeWidth="2" />
          <text x="460" y="145" textAnchor="middle" fontSize="16" fill="white" fontWeight="bold">Signal</text>
          <text x="460" y="168" textAnchor="middle" fontSize="12" fill="white">transcript + channel</text>
          <path d="M 555 150 L 685 150" stroke="#1B1B1F" strokeWidth="3" />
          <rect x="690" y="110" width="170" height="80" rx="5" fill="#F7F8FA" stroke="#1B1B1F" strokeWidth="2" />
          <text x="775" y="145" textAnchor="middle" fontSize="14" fill="#1B1B1F" fontWeight="bold">Same pipeline</text>
          <text x="775" y="168" textAnchor="middle" fontSize="11" fill="#666">same controls</text>
        </DiagramSVG>

        <div className="grid md:grid-cols-2 gap-6 my-10">
          <article className="card">
            <h3 className="font-semibold text-xl mb-3">Browser voice</h3>
            <p>WebRTC uses a short-lived session credential. Spoken and visible responses share context with text, while raw audio is not persisted.</p>
          </article>
          <article className="card">
            <h3 className="font-semibold text-xl mb-3">Phone</h3>
            <p>Telephony audio reaches the backend bridge, produces a transcript, and enters the same classification, routing, and action path.</p>
          </article>
        </div>

        <CalloutCard variant="accent" title="Safety overrides intent">
          A crisis or life-safety phrase must escalate regardless of the predicted intent. When a channel is unavailable, the interface degrades honestly instead of presenting a broken control.
        </CalloutCard>

        <CollapsibleNotes>
          <p>Transport-specific plumbing may differ, but the output must still be a signal with channel metadata. This keeps audit, safety, dedup, and attribution consistent.</p>
        </CollapsibleNotes>
      </div>
    </div>
  )
}
