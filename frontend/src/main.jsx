import React, { useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './style.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [sourceUrl, setSourceUrl] = useState('')
  const [prompt, setPrompt] = useState('')
  const [status, setStatus] = useState('')
  const [busy, setBusy] = useState(false)
  const inputRef = useRef(null)

  async function createJob(withPrompt) {
    if (!sourceUrl.trim()) { setStatus('Add a video URL first.'); return }
    setBusy(true); setStatus('Creating discovery job…')
    try {
      const response = await fetch(`${API}/api/jobs`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({source_url: sourceUrl.trim(), prompt: withPrompt ? (prompt.trim() || null) : null}) })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Could not create job')
      setStatus(`Job ${data.id.slice(0, 8)} queued. Analysis worker will process it.`)
    } catch (error) { setStatus(error.message) } finally { setBusy(false) }
  }

  async function upload(event) {
    const file = event.target.files?.[0]
    if (!file) return
    setBusy(true); setStatus('Uploading and validating media…')
    const form = new FormData(); form.append('file', file)
    try {
      const response = await fetch(`${API}/api/media/upload`, {method: 'POST', body: form})
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Upload failed')
      setStatus(`${data.filename} validated: ${Math.round(data.metadata.duration_seconds)}s, ${data.metadata.width}×${data.metadata.height}`)
    } catch (error) { setStatus(error.message) } finally { setBusy(false); event.target.value = '' }
  }

  return <main className="shell">
    <header><div className="brand"><span className="mark">✦</span><span>CLIPFORGE</span></div><span className="status"><i/> Local workspace</span></header>
    <section className="hero"><p className="eyebrow">AI CLIPPING STUDIO</p><h1>Turn long videos into<br/><em>unmissable moments.</em></h1><p className="sub">Find complete, high-energy moments from videos and livestreams. Reframe, caption, and export clips ready for Shorts.</p></section>
    <section className="card"><label>VIDEO SOURCE</label><input value={sourceUrl} onChange={e => setSourceUrl(e.target.value)} placeholder="Paste a YouTube, Twitch, or direct video URL"/><div className="divider"><span>or</span></div><input ref={inputRef} type="file" accept="video/mp4,video/quicktime,video/webm,video/x-matroska" onChange={upload} hidden/><button className="upload" disabled={busy} onClick={() => inputRef.current?.click()}>＋ Upload a local video</button><label className="prompt-label">OPTIONAL PROMPT</label><textarea value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="Find the funniest complete stories where the streamer reacts loudly..."/><div className="actions"><button className="secondary" disabled={busy} onClick={() => createJob(false)}>Find Best Moments <span>→</span></button><button className="primary" disabled={busy} onClick={() => createJob(true)}>Find Moments Like This <span>→</span></button></div>{status && <p className="notice">{status}</p>}</section>
    <section className="features"><div><b>01</b><h3>Complete thoughts</h3><p>Clips begin with a hook and end after the payoff—not halfway through a sentence.</p></div><div><b>02</b><h3>Explainable scoring</h3><p>See why each moment ranked: hook, flow, value, emotion, and audience energy.</p></div><div><b>03</b><h3>Creator control</h3><p>Prompt the search, review the boundaries, and keep your best moments private.</p></div></section>
  </main>
}
createRoot(document.getElementById('root')).render(<App />)
