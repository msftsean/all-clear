import SectionHeader from './SectionHeader'

const TROUBLESHOOTING_ROWS = [
  { sev: 'red', issue: 'Mic permission denied', likely: 'Browser or OS blocked microphone access.', fix: 'Click the lock icon in the address bar, allow microphone, then refresh. On macOS/Windows also check system privacy settings.' },
  { sev: 'red', issue: 'WebSocket fails 4001', likely: 'Realtime token/session rejected or expired.', fix: 'Refresh the page to request a new ephemeral session. Verify Azure OpenAI Realtime deployment settings.' },
  { sev: 'red', issue: 'WebSocket closes 4002', likely: 'Voice session failed during negotiation or function-tool handoff.', fix: 'Check backend logs, confirm the Realtime deployment name, and fall back to text while investigating.' },
  { sev: 'red', issue: 'No audio output', likely: 'Muted tab, muted OS output, wrong output device, or autoplay policy.', fix: 'Unmute tab, raise system volume, switch output device, and click once in the page before speaking.' },
  { sev: 'yellow', issue: 'VAD not triggering', likely: 'Input level too low or browser noise suppression is over-aggressive.', fix: 'Move closer to mic, use a headset, disable aggressive noise suppression, or click to stop and retry.' },
  { sev: 'yellow', issue: '“Voice unavailable” banner', likely: 'Backend reports Realtime unavailable or voice kill switch is enabled.', fix: 'Use text chat. Verify /api/realtime/health and VOICE_ENABLED before trying voice again.' },
  { sev: 'red', issue: '503 on POST /session', likely: 'Voice feature disabled or Realtime service unavailable.', fix: 'Check VOICE_ENABLED=true, MOCK_MODE=false, Azure Realtime deployment, and Container App environment variables.' },
  { sev: 'yellow', issue: 'Mic button not shown', likely: 'Health check says voice is not available or browser lacks required APIs.', fix: 'Open Chrome/Edge, verify /api/realtime/health returns realtime_available=true, then refresh.' },
  { sev: 'yellow', issue: 'Transcript not appearing', likely: 'Partial transcript event delayed or WebRTC data channel not open.', fix: 'Wait for the final response, retry once, then use text chat if data channel remains unavailable.' },
  { sev: 'red', issue: 'Text chat broken after voice', likely: 'Shared session state or frontend state machine regressed.', fix: 'Stop the voice session, refresh, and test /api/chat directly. Treat as blocking for the demo.' },
  { sev: 'red', issue: 'WebRTC ICE failure', likely: 'Network blocks UDP/TURN path or corporate firewall interferes.', fix: 'Switch networks, use a hotspot, try Edge/Chrome, or continue with text fallback.' },
  { sev: 'red', issue: 'Codespaces API calls fail', likely: 'Port forwarding or VITE_API_BASE_URL points at inaccessible localhost.', fix: 'Forward ports 5173 and 8000. Leave VITE_API_BASE_URL empty so Vite proxies /api.' },
  { sev: 'red', issue: 'Container App not starting', likely: 'Missing env var, image pull failure, or startup command error.', fix: 'Inspect Container App revisions/log stream, verify image and env vars, then redeploy with azd deploy.' },
  { sev: 'red', issue: 'azd up failure', likely: 'Subscription, quota, region, or permissions issue.', fix: 'Run az account show, confirm subscription ME-MngEnvMCAP262307-segayle-1, then retry after fixing quota or RBAC.' },
  { sev: 'red', issue: 'Azure OpenAI quota exceeded', likely: 'Deployment rate limit or quota exhausted.', fix: 'Wait, reduce concurrent demos, switch deployment/region, or use text fallback if Realtime cannot serve turns.' },
  { sev: 'yellow', issue: 'Cold start delay', likely: 'Container App scaled to zero or Realtime warm-up latency.', fix: 'Warm up five minutes early with /api/health and one text query. Keep the app open before the customer call.' },
]

export default function TroubleshootingSection() {
  return (
    <section id="troubleshooting" className="scroll-mt-24 reveal reveal-delay-2">
      <SectionHeader icon="🧯" title="Troubleshooting" id="troubleshooting-heading" />
      <div className="grid md:grid-cols-3 gap-3 mb-6">
        <Legend color="red" label="Blocking" text="Stop and fix before demoing voice." />
        <Legend color="yellow" label="Degraded" text="Demo can continue with caution or text fallback." />
        <Legend color="green" label="Self-resolving" text="Usually clears after warm-up, refresh, or retry." />
      </div>
      <div className="overflow-x-auto rounded-xl border border-lead/50">
        <table>
          <thead><tr><th>Severity</th><th>Symptom</th><th>Likely Cause</th><th>Fast Fix</th></tr></thead>
          <tbody>
            {TROUBLESHOOTING_ROWS.map((row) => (
              <tr key={row.issue}>
                <td className={severityText(row.sev)}>{severityIcon(row.sev)}</td>
                <td className="font-medium">{row.issue}</td>
                <td className="text-silver">{row.likely}</td>
                <td className="text-silver">{row.fix}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

function Legend({ color, label, text }: { color: 'red' | 'yellow' | 'green', label: string, text: string }) {
  const classes = {
    red: 'border-red-500/40 bg-red-500/10 text-red-400',
    yellow: 'border-amber-500/40 bg-amber-500/10 text-amber-400',
    green: 'border-emerald-500/40 bg-emerald-500/10 text-emerald-400',
  }
  return (
    <div className={`rounded-2xl border p-4 ${classes[color]}`}>
      <div className="font-semibold text-sm">{severityIcon(color)} {label}</div>
      <p className="text-xs text-silver mt-1">{text}</p>
    </div>
  )
}

function severityIcon(severity: string) {
  if (severity === 'red') return '🔴'
  if (severity === 'yellow') return '🟡'
  return '🟢'
}

function severityText(severity: string) {
  if (severity === 'red') return 'text-red-400 font-bold'
  if (severity === 'yellow') return 'text-amber-400 font-bold'
  return 'text-emerald-400 font-bold'
}
