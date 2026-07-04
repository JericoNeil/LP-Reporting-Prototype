import { useCallback, useRef, useState } from 'react'
import './App.css'

const WEBHOOK_PATH = '/webhook/lp-report-upload'

function App() {
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('idle') // idle | uploading | success | error
  const [result, setResult] = useState(null)
  const [errorMessage, setErrorMessage] = useState('')
  const [dragActive, setDragActive] = useState(false)
  const inputRef = useRef(null)

  const pickFile = useCallback((f) => {
    if (!f) return
    if (f.type !== 'application/pdf') {
      setStatus('error')
      setErrorMessage('Please choose a PDF file.')
      return
    }
    setFile(f)
    setStatus('idle')
    setErrorMessage('')
    setResult(null)
  }, [])

  const onDrop = useCallback(
    (e) => {
      e.preventDefault()
      setDragActive(false)
      pickFile(e.dataTransfer.files?.[0])
    },
    [pickFile]
  )

  const onSubmit = useCallback(async () => {
    if (!file) return
    setStatus('uploading')
    setErrorMessage('')
    try {
      const formData = new FormData()
      formData.append('data', file, file.name)

      const res = await fetch(WEBHOOK_PATH, {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) {
        throw new Error(`Workflow returned ${res.status}`)
      }

      const data = await res.json()
      setResult(data)
      setStatus('success')
    } catch (err) {
      console.error(err)
      setStatus('error')
      setErrorMessage(
        'Could not reach the workflow. Make sure n8n is running (docker compose up -d) and the workflow is active.'
      )
    }
  }, [file])

  const reset = useCallback(() => {
    setFile(null)
    setResult(null)
    setStatus('idle')
    setErrorMessage('')
    if (inputRef.current) inputRef.current.value = ''
  }, [])

  return (
    <div className="page">
      <header className="header">
        <div className="brand-mark">LP Reporting Assistant</div>
        <div className="brand-sub">Two-step AI workflow &mdash; draft, then review</div>
      </header>

      <main className="card">
        {status !== 'success' && (
          <>
            <h1 className="title">Upload a quarterly report</h1>
            <p className="subtitle">
              Drop in a portfolio company&rsquo;s quarterly report (PDF) to generate a draft LP
              update paragraph, reviewed for factual accuracy and tone before it reaches the
              template document.
            </p>

            <label
              className={`dropzone ${dragActive ? 'dropzone--active' : ''} ${file ? 'dropzone--has-file' : ''}`}
              onDragOver={(e) => {
                e.preventDefault()
                setDragActive(true)
              }}
              onDragLeave={() => setDragActive(false)}
              onDrop={onDrop}
            >
              <input
                ref={inputRef}
                type="file"
                accept="application/pdf"
                onChange={(e) => pickFile(e.target.files?.[0])}
                hidden
              />
              {file ? (
                <span className="dropzone-text">
                  <strong>{file.name}</strong>
                  <span className="dropzone-hint">Click to choose a different file</span>
                </span>
              ) : (
                <span className="dropzone-text">
                  <strong>Click to select a PDF</strong>
                  <span className="dropzone-hint">or drag and drop it here</span>
                </span>
              )}
            </label>

            {status === 'error' && <p className="error-text">{errorMessage}</p>}

            <button
              className="primary-button"
              disabled={!file || status === 'uploading'}
              onClick={onSubmit}
            >
              {status === 'uploading' ? 'Drafting and reviewing…' : 'Generate LP Update'}
            </button>

            {status === 'uploading' && (
              <p className="progress-note">
                Extracting text &rarr; Claude draft &amp; anomaly check &rarr; Claude review &rarr;
                writing to Google Doc&hellip;
              </p>
            )}
          </>
        )}

        {status === 'success' && result && (
          <div className="result">
            <div className="result-meta">
              <span className="result-label">Portfolio Company</span>
              <h2 className="result-company">{result.companyName}</h2>
              <span className="result-quarter">{result.quarterLabel}</span>
            </div>

            <div className="result-paragraph">
              <span className="result-label">Draft LP Update Paragraph</span>
              <p>{result.finalParagraph}</p>
            </div>

            <div className="result-actions">
              {result.googleDocUrl && (
                <a
                  className="primary-button primary-button--link"
                  href={result.googleDocUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  Open in Google Docs
                </a>
              )}
              <button className="secondary-button" onClick={reset}>
                Process another report
              </button>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        Draft only &mdash; requires human review before any update is sent to Limited Partners.
      </footer>
    </div>
  )
}

export default App
