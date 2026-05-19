NUMERIC_FEATURES = [
    "sessions_count",
    "page_views_count",
    "time_on_site_sec",
    "requested_budget",
    "company_size",
]

CATEGORICAL_FEATURES = [
    "source",
    "industry",
]

BINARY_FEATURES = [
    "viewed_pricing",
    "downloaded_pdf",
]

FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES + BINARY_FEATURES
