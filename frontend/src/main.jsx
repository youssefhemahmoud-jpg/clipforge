import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import './style.css'

function App() {
  const [sourceUrl, setSourceUrl] = useState('')
  const [prompt, setPrompt] = useState('')
  const [submitted, setSubmitted] = useState(false)

  return <main className="shell">
    <header><div className="brand"><span className="mark">✦</span><span>CLIPFORGE</span></div><span className="status"><i/> Local workspace</span></header>
    <section className="hero"><p className="eyebrow">AI CLIPPING STUDIO</p><h1>Turn long videos into<br/><em>unmissable moments.</em></h1><p className="sub">Find complete, high-energy moments from videos and livestreams. Reframe, caption, and export clips ready for Shorts.</p></section>
    <section className="card"><label>VIDEO SOURCE</label><input value={sourceUrl} onChange={e => setSourceUrl(e.target.value)} placeholder="Paste a YouTube, Twitch, or direct video URL"/><div className="divider"><span>or</span></div><button className="upload">＋ Upload a local video</button><label className="prompt-label">OPTIONAL PROMPT</label><textarea value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="Find the funniest complete stories where the streamer reacts loudly..."/><div className="actions"><button className="secondary" onClick={() => setSubmitted(false)}>Find Best Moments <span>→</span></button><button className="primary" onClick={() => setSubmitted(true)}>Find Moments Like This <span>→</span></button></div>{submitted && <p className="notice">Discovery job queued locally. The analysis worker will appear in the next build.</p>}</section>
    <section className="features"><div><b>01</b><h3>Complete thoughts</h3><p>Clips begin with a hook and end after the payoff—not halfway through a sentence.</p></div><div><b>02</b><h3>Explainable scoring</h3><p>See why each moment ranked: hook, flow, value, emotion, and audience energy.</p></div><div><b>03</b><h3>Creator control</h3><p>Prompt the search, review the boundaries, and keep your best moments private.</p></div></section>
  </main>
}
createRoot(document.getElementById('root')).render(<App />)
