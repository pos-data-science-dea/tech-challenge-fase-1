"""Funcoes auxiliares para modelagem preditiva."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score


def avaliar_modelo(nome, modelo, X_train, X_test, y_train, y_test, kfold=5):
    """Treina o modelo, avalia no teste e retorna métricas com cross-validation."""
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    cv_scores = cross_val_score(
        modelo, X_train, y_train,
        cv=kfold,
        scoring="neg_root_mean_squared_error",
    )
    rmse_cv = -cv_scores.mean()

    resultado = {
        "Modelo": nome,
        "RMSE (teste)": round(rmse, 4),
        "MAE (teste)": round(mae, 4),
        "R² (teste)": round(r2, 4),
        "RMSE CV (treino)": round(rmse_cv, 4),
    }
    return modelo, y_pred, resultado


def classificar_nps(score):
    """Classifica o score de NPS em Detrator, Neutro ou Promotor conforme a regra de mercado."""
    if score <= 6.0:
        return "Detrator"
    elif score <= 8.0:
        return "Neutro"
    else:
        return "Promotor"


__all__ = ["avaliar_modelo", "classificar_nps"]
