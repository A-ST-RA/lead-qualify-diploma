# Lead Qualify ML Service

Сервис обучает модель на размеченных лидах и отдаёт вероятность `deal_won=1` через REST API.

## Установка

```bash
cd ml-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Обучение

```bash
python -m lead_qualify.train --data study_tasks/leads_big.csv --output artifacts/model.joblib
```

Создаются:

- `artifacts/model.joblib` — sklearn Pipeline (препроцессинг + RandomForest)
- `artifacts/metrics.json` — метрики hold-out и метаданные обучения

## Запуск API

```bash
uvicorn lead_qualify.api.main:app --reload --port 8000
```

Документация: http://localhost:8000/docs

### Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/health` | Статус сервиса и загрузки модели |
| GET | `/model/info` | Признаки и метрики обучения |
| POST | `/predict` | Вероятность конверсии лида |

### Пример запроса

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sessions_count": 3,
    "page_views_count": 8,
    "time_on_site_sec": 300,
    "requested_budget": 90000,
    "company_size": 25,
    "source": "telegram_ads",
    "industry": null,
    "viewed_pricing": 1,
    "downloaded_pdf": 0
  }'
```

Ответ:

```json
{
  "probability": 0.73,
  "predicted_class": 1,
  "threshold": 0.5
}
```

## Признаки лида

| Поле | Тип | Описание |
|------|-----|----------|
| `sessions_count` | int | Число сессий |
| `page_views_count` | int | Просмотры страниц |
| `time_on_site_sec` | int | Время на сайте (сек) |
| `requested_budget` | float | Запрошенный бюджет |
| `company_size` | int | Размер компании |
| `source` | str | Канал привлечения |
| `industry` | str \| null | Отрасль |
| `viewed_pricing` | 0 \| 1 | Смотрел pricing |
| `downloaded_pdf` | 0 \| 1 | Скачал PDF |

Целевая переменная при обучении: `deal_won` (1 = сделка выиграна).

## Структура

```
ml-service/
├── lead_qualify/     # Пакет: обучение и API
├── artifacts/        # Модель и метрики (не в git)
├── study_tasks/      # Учебные скрипты и CSV
└── requirements.txt
```
