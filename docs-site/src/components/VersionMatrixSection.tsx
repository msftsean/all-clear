import type { ReactNode } from 'react'
import SectionHeader from './SectionHeader'

function TableWrap({ children }: { children: ReactNode }) {
  return <div className="overflow-x-auto rounded-xl border border-lead/50 mb-6">{children}</div>
}

export default function VersionMatrixSection() {
  return (
    <section id="version-matrix" className="scroll-mt-24 reveal reveal-delay-1">
      <SectionHeader icon="🧰" title="Version Matrix & Compatibility" id="version-matrix-heading" />
      <h3 className="text-mercury-blue font-medium text-lg mb-4 mt-8">Runtime & Framework Versions</h3>
      <TableWrap>
        <table>
          <thead><tr><th>Component</th><th>Required</th><th>Recommended</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td>🐍 Python</td><td><code>3.11+</code></td><td><code>3.12</code></td><td className="text-emerald-400 font-medium">✅ Supported</td></tr>
            <tr><td>🟩 Node.js</td><td><code>18+</code></td><td><code>20 LTS</code></td><td className="text-emerald-400 font-medium">✅ Supported</td></tr>
            <tr><td>⚡ FastAPI</td><td><code>0.109+</code></td><td><code>0.115+</code></td><td className="text-emerald-400 font-medium">✅ Supported</td></tr>
            <tr><td>⚛️ React</td><td><code>18.x</code></td><td><code>18.3+</code></td><td className="text-emerald-400 font-medium">✅ Supported</td></tr>
            <tr><td>⚡ Vite</td><td><code>5.x</code></td><td><code>5.2+</code></td><td className="text-emerald-400 font-medium">✅ Supported</td></tr>
          </tbody>
        </table>
      </TableWrap>

      <h3 className="text-mercury-blue font-medium text-lg mb-4 mt-8">Azure OpenAI Model Versions</h3>
      <TableWrap>
        <table>
          <thead><tr><th>Model</th><th>Version</th><th>Use Case</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td>🧠 GPT-4.1</td><td><code>2025-04-01-preview</code></td><td>Text chat pipeline</td><td className="text-emerald-400">✅ Active</td></tr>
            <tr><td>🎤 GPT Realtime</td><td><code>2025-04-01-preview</code></td><td>Voice / WebRTC (GA nested format, default voice: marin)</td><td className="text-emerald-400">✅ Active</td></tr>
            <tr><td>🔊 GPT-4o Audio Preview</td><td><code>2024-10-01</code></td><td>Audio fallback</td><td className="text-amber-400">🟡 Optional</td></tr>
          </tbody>
        </table>
      </TableWrap>

      <h3 className="text-mercury-blue font-medium text-lg mb-4 mt-8">Browser Compatibility</h3>
      <TableWrap>
        <table>
          <thead><tr><th>Browser</th><th>Min Version</th><th>WebRTC</th><th>Audio API</th><th>Recommended</th></tr></thead>
          <tbody>
            <tr><td>🟡 Chrome</td><td><code>90+</code></td><td className="text-emerald-400">✅ Full</td><td className="text-emerald-400">✅ Full</td><td>⭐ Best</td></tr>
            <tr><td>🔵 Edge</td><td><code>90+</code></td><td className="text-emerald-400">✅ Full</td><td className="text-emerald-400">✅ Full</td><td>⭐ Best</td></tr>
            <tr><td>🟠 Firefox</td><td><code>85+</code></td><td className="text-emerald-400">✅ Full</td><td className="text-emerald-400">✅ Full</td><td className="text-emerald-400">✅ Good</td></tr>
            <tr><td>🔘 Safari</td><td><code>15+</code></td><td className="text-amber-400">⚠️ Partial</td><td className="text-amber-400">⚠️ Partial</td><td className="text-amber-400">🟡 Caution</td></tr>
            <tr><td>🔴 IE / Legacy</td><td>Any</td><td className="text-red-400">❌ None</td><td className="text-red-400">❌ None</td><td className="text-red-400">❌ Unsupported</td></tr>
          </tbody>
        </table>
      </TableWrap>
      <blockquote className="border-l-4 border-mercury-blue/50 pl-4 py-3 bg-mercury-blue/5 rounded-r-xl text-silver text-sm mb-6">
        <strong className="text-starlight">Safari note:</strong> WebRTC and Web Audio API support varies. Test before customer demos on macOS/iOS.
      </blockquote>

      <h3 className="text-mercury-blue font-medium text-lg mb-4 mt-8">Operating System Support</h3>
      <TableWrap>
        <table>
          <thead><tr><th>Platform</th><th>Support Level</th><th>Notes</th></tr></thead>
          <tbody>
            <tr><td>🪟 Windows 10/11</td><td className="text-emerald-400">✅ Full</td><td>Recommended for demos</td></tr>
            <tr><td>🍎 macOS 12+</td><td className="text-emerald-400">✅ Full</td><td>Check Safari mic permissions</td></tr>
            <tr><td>🐧 Linux (Ubuntu 22+)</td><td className="text-emerald-400">✅ Full</td><td>Chrome/Firefox only</td></tr>
            <tr><td>☁️ GitHub Codespaces</td><td className="text-emerald-400">✅ Full</td><td>Leave <code>VITE_API_BASE_URL</code> empty</td></tr>
            <tr><td>🐳 Docker Desktop</td><td className="text-emerald-400">✅ Full</td><td><code>docker-compose up</code> — one command</td></tr>
          </tbody>
        </table>
      </TableWrap>
    </section>
  )
}
