const SOURCE_LABELS = {
  google_ads: 'Google Ads',
  social: 'Соцсети',
  organic: 'Органика',
  referral: 'Реферал',
  email: 'Email',
}

const INDUSTRY_LABELS = {
  fintech: 'Финтех',
  education: 'Образование',
  ecommerce: 'E-commerce',
}

export const SOURCES = Object.keys(SOURCE_LABELS)
export const INDUSTRIES = Object.keys(INDUSTRY_LABELS)

export const DEFAULT_LEAD = {
  sessions_count: 3,
  page_views_count: 8,
  time_on_site_sec: 300,
  requested_budget: 90000,
  company_size: 25,
  source: 'email',
  industry: 'fintech',
  viewed_pricing: 1,
  downloaded_pdf: 0,
}

function formatPercent(probability) {
  return `${Math.round(probability * 100)}%`
}

function getTier(probability) {
  if (probability >= 0.75) return 'hot'
  if (probability >= 0.55) return 'warm'
  if (probability >= 0.35) return 'cool'
  return 'cold'
}

const TIER_META = {
  hot: {
    label: 'Горячий лид',
    color: '#16a34a',
    summary: 'Высокая вероятность сделки — действуйте быстро.',
    actions: [
      'Позвоните в течение 1 часа и предложите созвон с ЛПР.',
      'Подготовьте персональное КП с учётом бюджета и размера компании.',
      'Зафиксируйте следующий шаг в CRM с датой и ответственным.',
    ],
  },
  warm: {
    label: 'Тёплый лид',
    color: '#ca8a04',
    summary: 'Есть потенциал — нужен активный follow-up.',
    actions: [
      'Свяжитесь сегодня: уточните задачу и сроки принятия решения.',
      'Отправьте кейс из похожей отрасли и короткое демо.',
      'Запланируйте повторный контакт через 2–3 дня, если нет ответа.',
    ],
  },
  cool: {
    label: 'Прохладный лид',
    color: '#ea580c',
    summary: 'Сигналы слабые — стоит прогреть, но не перегружать менеджера.',
    actions: [
      'Отправьте полезный контент: гайд, чек-лист или вебинар.',
      'Проверьте, смотрел ли лид pricing — если нет, пришлите тарифы.',
      'Не тратьте больше 15 минут на первый контакт без ответа.',
    ],
  },
  cold: {
    label: 'Холодный лид',
    color: '#64748b',
    summary: 'Низкая вероятность — оставьте в автоматической воронке.',
    actions: [
      'Добавьте в email-цепочку на 2–4 недели без ручных звонков.',
      'Пересмотрите источник и качество трафика по этому каналу.',
      'Вернитесь к лиду только при новой активности на сайте.',
    ],
  },
}

function getContextTips(lead, probability) {
  const tips = []

  if (!lead.viewed_pricing) {
    tips.push('Лид не смотрел pricing — отправьте страницу с тарифами и FAQ по оплате.')
  }

  if (!lead.downloaded_pdf) {
    tips.push('PDF не скачан — предложите материал с кейсами или ROI-калькулятор.')
  }

  if (lead.sessions_count <= 2 && lead.page_views_count <= 4) {
    tips.push('Мало визитов — возможно, лид ещё на этапе исследования, не давите продажей.')
  }

  if (lead.time_on_site_sec >= 400) {
    tips.push('Долгое время на сайте — хороший повод спросить, какие разделы были полезны.')
  }

  if (lead.requested_budget >= 100000) {
    tips.push('Крупный бюджет — подключите старшего менеджера или аккаунта.')
  }

  if (lead.company_size >= 30) {
    tips.push('Средняя/крупная компания — уточните процесс согласования и количество ЛПР.')
  }

  if (!lead.industry) {
    tips.push('Отрасль не указана — уточните нишу на первом контакте для персонализации.')
  }

  if (probability >= 0.55 && lead.source === 'referral') {
    tips.push('Реферальный канал + высокий скор — поблагодарите партнёра и ускорьте сделку.')
  }

  return tips
}

export function getManagerAdvice(lead, { probability, predicted_class, threshold }) {
  const tier = getTier(probability)
  const meta = TIER_META[tier]
  const contextTips = getContextTips(lead, probability)

  return {
    tier,
    label: meta.label,
    color: meta.color,
    probabilityLabel: formatPercent(probability),
    predictedLabel: predicted_class === 1 ? 'Сделка вероятна' : 'Сделка маловероятна',
    isAboveThreshold: probability >= threshold,
    thresholdLabel: formatPercent(threshold),
    summary: meta.summary,
    actions: meta.actions,
    contextTips,
    sourceLabel: SOURCE_LABELS[lead.source] ?? lead.source,
    industryLabel: lead.industry ? (INDUSTRY_LABELS[lead.industry] ?? lead.industry) : 'Не указана',
  }
}
