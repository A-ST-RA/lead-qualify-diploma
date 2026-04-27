import marimo

__generated_with = "0.23.3"
app = marimo.App()


@app.cell
def _():
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier

    from sklearn.pipeline import Pipeline

    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder

    from sklearn.model_selection import train_test_split

    from sklearn.compose import ColumnTransformer

    from sklearn.metrics import (
      accuracy_score,
      confusion_matrix,
      precision_score,
      recall_score,
      f1_score,
      roc_auc_score,
    )

    import pandas as pd

    return (
        ColumnTransformer,
        DecisionTreeClassifier,
        HistGradientBoostingClassifier,
        OneHotEncoder,
        Pipeline,
        RandomForestClassifier,
        SimpleImputer,
        accuracy_score,
        confusion_matrix,
        f1_score,
        pd,
        precision_score,
        recall_score,
        roc_auc_score,
        train_test_split,
    )


@app.cell
def _(pd):
    df = pd.read_csv('leads_big.csv')

    print(df.columns)
    return (df,)


@app.cell
def _():
    numerical_features = ['sessions_count', 'page_views_count', 'time_on_site_sec', 'requested_budget', 'company_size']

    binary_features = ['viewed_pricing', 'downloaded_pdf']

    categorical_features = ['source', 'industry']
    return binary_features, categorical_features, numerical_features


@app.cell
def _(OneHotEncoder, Pipeline, SimpleImputer):
    numerical_pipline = Pipeline([
      ('imputer', SimpleImputer(strategy="median")),
    ])

    binary_pipline = Pipeline([
      ('imputer', SimpleImputer(strategy="constant", fill_value=0)),
    ])

    categorical_pipline = Pipeline([
      ('imputer', SimpleImputer(strategy="constant")),
      ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return binary_pipline, categorical_pipline, numerical_pipline


@app.cell
def _(binary_features, categorical_features, df, numerical_features):
    X = df[numerical_features + binary_features + categorical_features]
    y = df['deal_won']
    return X, y


@app.cell
def _(
    DecisionTreeClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
):
    models = {
      "DecisionTree": DecisionTreeClassifier(random_state=42),
      "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
      "HistGradientBoosting": HistGradientBoostingClassifier(max_iter=100,
        learning_rate=0.05,
        max_leaf_nodes=5,
        min_samples_leaf=2,
        random_state=42,
      ),
    }
    return (models,)


@app.cell
def _(X, train_test_split, y):
    X_train, X_test, y_train, y_test = train_test_split(
      X,
      y,
      test_size=0.25,
      random_state=42,
      stratify=y
    )
    return X_test, X_train, y_test, y_train


@app.cell
def _(
    ColumnTransformer,
    binary_features,
    binary_pipline,
    categorical_features,
    categorical_pipline,
    numerical_features,
    numerical_pipline,
):
    preprocessor = ColumnTransformer([
      ("numeric", numerical_pipline, numerical_features),
      ("categorical", categorical_pipline, categorical_features),
      ("binary", binary_pipline, binary_features),
    ])
    return (preprocessor,)


@app.cell
def _(Pipeline, preprocessor):
    def makeModlePipline(model):
      model_pipline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', model)
      ])
  
      return model_pipline

    return (makeModlePipline,)


@app.cell
def _(
    X_test,
    X_train,
    accuracy_score,
    confusion_matrix,
    f1_score,
    makeModlePipline,
    models,
    precision_score,
    recall_score,
    roc_auc_score,
    y_test,
    y_train,
):
    for name, model in models.items():
      curr_model = makeModlePipline(model)
  
      curr_model.fit(X_train, y_train)
  
      preds = curr_model.predict(X_test)
      probs = curr_model.predict_proba(X_test)[:, 1]
  
      print(f"\n=== {name} ===")
      print("Accuracy:", accuracy_score(y_test, preds))
      print("Precision:", precision_score(y_test, preds))
      print("Recall:", recall_score(y_test, preds))
      print("F1:", f1_score(y_test, preds))
      print("ROC-AUC:", roc_auc_score(y_test, probs))
      print("Confusion matrix:")
      print(confusion_matrix(y_test, preds))
    return


if __name__ == "__main__":
    app.run()
