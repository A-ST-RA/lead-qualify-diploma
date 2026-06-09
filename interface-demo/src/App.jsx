import { useEffect, useState } from 'react'
import { checkHealth, predictLead } from './api'
import { DEFAULT_LEAD, getManagerAdvice, INDUSTRIES, SOURCES } from './advice'

function Field({ label, children, hint }) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      {children}
      {hint && <span className="field-hint">{hint}</span>}
    </label>
  )
}

function Toggle({ checked, onChange, label }) {
  return (
    <button
      type="button"
      className={`toggle ${checked ? 'toggle-on' : ''}`}
      onClick={() => onChange(checked ? 0 : 1)}
      aria-pressed={Boolean(checked)}
    >
      <span className="toggle-track">
        <span className="toggle-thumb" />
      </span>
      <span>{label}</span>
    </button>
  )
}

export default function App() {
  const [lead, setLead] = useState(DEFAULT_LEAD)
  const [result, setResult] = useState(null)
  const [advice, setAdvice] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [apiStatus, setApiStatus] = useState(null)

  useEffect(() => {
    checkHealth().then(setApiStatus).catch(() => {
      setApiStatus({ status: 'error', model_loaded: false })
    })
  }, [])

  function updateField(name, value) {
    setLead((prev) => ({ ...prev, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    setAdvice(null)

    try {
      const payload = {
        ...lead,
        sessions_count: Number(lead.sessions_count),
        page_views_count: Number(lead.page_views_count),
        time_on_site_sec: Number(lead.time_on_site_sec),
        requested_budget: Number(lead.requested_budget),
        company_size: Number(lead.company_size),
        viewed_pricing: Number(lead.viewed_pricing),
        downloaded_pdf: Number(lead.downloaded_pdf),
        industry: lead.industry || null,
      }

      const prediction = await predictLead(payload)
      setResult(prediction)
      setAdvice(getManagerAdvice(payload, prediction))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <header className="header">
        <div>
          <p className="eyebrow">Lead Qualify</p>
          <h1>Оценка лида</h1>
          <p className="subtitle">Заполните данные и получите вероятность сделки с рекомендациями для менеджера.</p>
        </div>
        <div className={`status ${apiStatus?.model_loaded ? 'status-ok' : 'status-warn'}`}>
          {apiStatus === null && 'Проверка API…'}
          {apiStatus && !apiStatus.model_loaded && 'Модель не загружена'}
          {apiStatus?.model_loaded && 'Модель готова'}
        </div>
      </header>

      <main className="layout">
        <form className="card form" onSubmit={handleSubmit}>
          <h2>Данные лида</h2>

          <div className="grid">
            <Field label="Сессии">
              <input
                type="number"
                min="0"
                value={lead.sessions_count}
                onChange={(e) => updateField('sessions_count', e.target.value)}
                required
              />
            </Field>

            <Field label="Просмотры страниц">
              <input
                type="number"
                min="0"
                value={lead.page_views_count}
                onChange={(e) => updateField('page_views_count', e.target.value)}
                required
              />
            </Field>

            <Field label="Время на сайте, сек">
              <input
                type="number"
                min="0"
                value={lead.time_on_site_sec}
                onChange={(e) => updateField('time_on_site_sec', e.target.value)}
                required
              />
            </Field>

            <Field label="Бюджет, ₽">
              <input
                type="number"
                min="0"
                step="1000"
                value={lead.requested_budget}
                onChange={(e) => updateField('requested_budget', e.target.value)}
                required
              />
            </Field>

            <Field label="Размер компании">
              <input
                type="number"
                min="0"
                value={lead.company_size}
                onChange={(e) => updateField('company_size', e.target.value)}
                required
              />
            </Field>

            <Field label="Источник">
              <select value={lead.source} onChange={(e) => updateField('source', e.target.value)}>
                {SOURCES.map((source) => (
                  <option key={source} value={source}>{source}</option>
                ))}
              </select>
            </Field>

            <Field label="Отрасль">
              <select
                value={lead.industry}
                onChange={(e) => updateField('industry', e.target.value)}
              >
                <option value="">Не указана</option>
                {INDUSTRIES.map((industry) => (
                  <option key={industry} value={industry}>{industry}</option>
                ))}
              </select>
            </Field>
          </div>

          <div className="toggles">
            <Toggle
              checked={lead.viewed_pricing}
              onChange={(value) => updateField('viewed_pricing', value)}
              label="Смотрел pricing"
            />
            <Toggle
              checked={lead.downloaded_pdf}
              onChange={(value) => updateField('downloaded_pdf', value)}
              label="Скачал PDF"
            />
          </div>

          <button type="submit" className="submit" disabled={loading || !apiStatus?.model_loaded}>
            {loading ? 'Считаем…' : 'Оценить лид'}
          </button>

          {error && <p className="error">{error}</p>}
        </form>

        <section className="card result">
          <h2>Результат</h2>

          {!result && !loading && (
            <p className="placeholder">Заполните форму и нажмите «Оценить лид».</p>
          )}

          {loading && <p className="placeholder">Отправляем запрос к модели…</p>}

          {advice && (
            <>
              <div
                className="score"
                style={{ '--accent': advice.color, '--p': result.probability }}
              >
                <div className="score-ring">
                  <span className="score-value">{advice.probabilityLabel}</span>
                  <span className="score-caption">вероятность сделки</span>
                </div>
                <div className="score-meta">
                  <span className="badge" style={{ background: advice.color }}>{advice.label}</span>
                  <p className="prediction">{advice.predictedLabel}</p>
                  <p className="threshold">
                    Порог модели: {advice.thresholdLabel}
                    {' · '}
                    {advice.isAboveThreshold ? 'выше порога' : 'ниже порога'}
                  </p>
                </div>
              </div>

              <div className="advice-block">
                <h3>Что делать менеджеру</h3>
                <p className="advice-summary">{advice.summary}</p>
                <ul>
                  {advice.actions.map((action) => (
                    <li key={action}>{action}</li>
                  ))}
                </ul>
              </div>

              {advice.contextTips.length > 0 && (
                <div className="advice-block tips">
                  <h3>Дополнительно по этому лиду</h3>
                  <ul>
                    {advice.contextTips.map((tip) => (
                      <li key={tip}>{tip}</li>
                    ))}
                  </ul>
                </div>
              )}

              <dl className="meta">
                <div>
                  <dt>Источник</dt>
                  <dd>{advice.sourceLabel}</dd>
                </div>
                <div>
                  <dt>Отрасль</dt>
                  <dd>{advice.industryLabel}</dd>
                </div>
              </dl>
            </>
          )}
        </section>
      </main>
    </div>
  )
}
