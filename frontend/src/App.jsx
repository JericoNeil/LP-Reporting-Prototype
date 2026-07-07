import { useCallback, useRef, useState } from 'react'
import './App.css'

const WEBHOOK_PATH = '/webhook/lp-report-upload'

const SAMPLE_REPORTS = [
  { label: 'NexoraCloud', file: 'NexoraCloud_Q2_2026_Report.pdf' },
  { label: 'Solvex Diagnostics', file: 'Solvex_Diagnostics_Q2_2026_Report.pdf' },
  { label: 'Kestrel Data Systems', file: 'Kestrel_Data_Systems_Q2_2026_Report.pdf' },
]

function App() {
  const [files, setFiles] = useState([]) // File[]
  const [status, setStatus] = useState('idle') // idle | uploading | success | error
  const [progress, setProgress] = useState({ current: 0, total: 0, label: '' })
  const [companies, setCompanies] = useState([]) // { companyName, quarterLabel, finalParagraph }
  const [docUrl, setDocUrl] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [dragActive, setDragActive] = useState(false)
  const inputRef = useRef(null)

  const addFiles = useCallback((incoming) => {
    const pdfs = Array.from(incoming || []).filter((f) => f.type === 'application/pdf')
    if (pdfs.length === 0) {
      setStatus('error')
      setErrorMessage('Please choose PDF files.')
      return
    }
    setFiles((prev) => {
      // de-dupe by name
      const names = new Set(prev.map((f) => f.name))
      return [...prev, ...pdfs.filter((f) => !names.has(f.name))]
    })
    setStatus('idle')
    setErrorMessage('')
  }, [])

  const onDrop = useCallback(
    (e) => {
      e.preventDefault()
      setDragActive(false)
      addFiles(e.dataTransfer.files)
    },
    [addFiles]
  )

  const removeFile = useCallback((name) => {
    setFiles((prev) => prev.filter((f) => f.name !== name))
  }, [])

  const loadAllSamples = useCallback(async () => {
    setStatus('uploading')
    setErrorMessage('')
    try {
      const loaded = await Promise.all(
        SAMPLE_REPORTS.map(async (sample) => {
          const res = await fetch(`/samples/${sample.file}`)
          if (!res.ok) throw new Error(`Could not load ${sample.label}.`)
          const blob = await res.blob()
          return new File([blob], sample.file, { type: 'application/pdf' })
        })
      )
      setFiles(loaded)
      setStatus('idle')
    } catch (err) {
      console.error(err)
      setStatus('error')
      setErrorMessage(err.message)
    }
  }, [])

  const onSubmit = useCallback(async () => {
    if (files.length === 0) return
    setStatus('uploading')
    setErrorMessage('')
    setCompanies([])
    setDocUrl('')

    const collected = []
    try {
      // Process sequentially: each report is drafted, reviewed, and written into the
      // same quarterly Google Doc before the next one starts. Awaiting each request
      // in turn also avoids a Drive indexing race (the doc exists and is indexed by
      // the time the next company looks for it).
      for (let i = 0; i < files.length; i++) {
        const f = files[i]
        setProgress({ current: i + 1, total: files.length, label: f.name })

        const formData = new FormData()
        formData.append('data', f, f.name)

        const res = await fetch(WEBHOOK_PATH, { method: 'POST', body: formData })
        if (!res.ok) {
          let detail = `status ${res.status}`
          try {
            const errBody = await res.json()
            if (errBody?.message) detail = errBody.message
          } catch {
            // response wasn't JSON; keep the status code
          }
          throw new Error(`Failed on ${f.name} (${detail}). Check the n8n Executions tab.`)
        }

        const data = await res.json()
        collected.push(data)
        setCompanies([...collected])
        if (data.googleDocUrl) setDocUrl(data.googleDocUrl)
      }

      setStatus('success')
    } catch (err) {
      console.error(err)
      setStatus('error')
      if (err instanceof TypeError) {
        setErrorMessage(
          'Could not reach the workflow. Make sure n8n is running (docker compose up -d) and the workflow is active.'
        )
      } else {
        setErrorMessage(err.message)
      }
    }
  }, [files])

  const reset = useCallback(() => {
    setFiles([])
    setCompanies([])
    setDocUrl('')
    setStatus('idle')
    setErrorMessage('')
    setProgress({ current: 0, total: 0, label: '' })
    if (inputRef.current) inputRef.current.value = ''
  }, [])

  return (
    <div className="page">
      <header className="header">
        <img src="/keensight-logo.png" alt="Keensight Capital" className="brand-logo" />
        <div className="brand-mark">LP Reporting Assistant</div>
        <div className="brand-sub">Two-step AI workflow &mdash; draft, then review</div>
      </header>

      <main className="card">
        {status !== 'success' && (
          <>
            <h1 className="title">Generate a quarterly LP report</h1>
            <p className="subtitle">
              Add each portfolio company&rsquo;s quarterly report (PDF). Every report is drafted and
              reviewed by Claude, then compiled into a single branded quarterly document &mdash; a
              Keensight cover and introduction, followed by one page per company.
            </p>

            <label
              className={`dropzone ${dragActive ? 'dropzone--active' : ''} ${files.length ? 'dropzone--has-file' : ''}`}
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
                multiple
                onChange={(e) => addFiles(e.target.files)}
                hidden
              />
              <span className="dropzone-text">
                <strong>Click to add PDF reports</strong>
                <span className="dropzone-hint">or drag and drop them here</span>
              </span>
            </label>

            {files.length > 0 && (
              <ul className="file-list">
                {files.map((f, i) => (
                  <li key={f.name} className="file-item">
                    <span className="file-index">{i + 1}</span>
                    <span className="file-name">{f.name}</span>
                    {status !== 'uploading' && (
                      <button
                        type="button"
                        className="file-remove"
                        onClick={() => removeFile(f.name)}
                        aria-label={`Remove ${f.name}`}
                      >
                        &times;
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            )}

            <div className="sample-picker">
              <span className="sample-picker-label">For the demo:</span>
              <div className="sample-picker-buttons">
                <button
                  type="button"
                  className="sample-chip"
                  disabled={status === 'uploading'}
                  onClick={loadAllSamples}
                >
                  Load all 3 sample reports
                </button>
              </div>
            </div>

            {status === 'error' && <p className="error-text">{errorMessage}</p>}

            <button
              className="primary-button"
              disabled={files.length === 0 || status === 'uploading'}
              onClick={onSubmit}
            >
              {status === 'uploading'
                ? `Processing ${progress.current} of ${progress.total}…`
                : `Generate quarterly report${files.length ? ` (${files.length})` : ''}`}
            </button>

            {status === 'uploading' && (
              <p className="progress-note">
                {progress.label} &mdash; extracting &rarr; Claude draft &amp; anomaly check &rarr;
                Claude review &rarr; writing into the quarterly document&hellip;
              </p>
            )}
          </>
        )}

        {status === 'success' && (
          <div className="result">
            <div className="result-meta">
              <span className="result-label">Quarterly Report Generated</span>
              <h2 className="result-company">
                {companies[0]?.quarterLabel || 'Current Quarter'}
              </h2>
              <span className="result-quarter">
                {companies.length} portfolio {companies.length === 1 ? 'company' : 'companies'} compiled
              </span>
            </div>

            <div className="result-paragraph">
              <span className="result-label">Companies included</span>
              {companies.map((c) => (
                <div key={c.companyName} className="company-block">
                  <strong className="company-name">{c.companyName}</strong>
                  <p className="company-para">{c.finalParagraph}</p>
                </div>
              ))}
            </div>

            <div className="result-actions">
              {docUrl && (
                <a
                  className="primary-button primary-button--link"
                  href={docUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  Open quarterly report in Google Docs
                </a>
              )}
              <button className="secondary-button" onClick={reset}>
                Start a new quarter
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
