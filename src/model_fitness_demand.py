# model_fitness_demand.py
# Predecir fitness density (gyms por 10k habitantes)

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error


def main():
    # 1) Cargar datos
    df = pd.read_csv("dataset_municipios_albacete_places_enriquecido_v5.csv")

    # 2) Definir variables
    features = ["poblacion_2025", "renta_media_proxy", "gyms_google_new"]
    target = "fitness_x10k_new"

    # 3) Dataset de modelado (incluye municipio + limpia NaNs)
    df_model = df[["municipio"] + features + [target]].dropna().copy()

    X = df_model[features]
    y = df_model[target]

    # 4) Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 5) Entrenar modelo
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # 6) Evaluar en test
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    # Predicción para todos los municipios (solo filas válidas sin NaN)
    df_model["predicted_fitness_density"] = model.predict(X)
    df_model["market_gap"] = df_model["predicted_fitness_density"] - df_model[target]

    # 7) Feature importance
    feature_importance = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)

    # 8) Cross-validation
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_r2 = cross_val_score(model, X, y, cv=cv, scoring="r2")
    cv_mae = -cross_val_score(model, X, y, cv=cv, scoring="neg_mean_absolute_error")

    # 9) Prints finales
    print("Test metrics")
    print("R2:", r2)
    print("MAE:", mae)

    print("\nFeature importance")
    print(feature_importance)

    print("\nCross-validation (5-fold)")
    print("R2  mean:", cv_r2.mean(), "std:", cv_r2.std())
    print("MAE mean:", cv_mae.mean(), "std:", cv_mae.std())

    # ============================
    # Ranking de oportunidades (market_gap alto = faltan gimnasios)
    # ============================
    opportunities = df_model.sort_values("market_gap", ascending=False)

    # Filtrar municipios con mercado viable
    opportunities_filtered = opportunities[opportunities["poblacion_2025"] > 2000]


    print("\nTop REAL market opportunities (poblacion > 2000):")

    print(
    opportunities_filtered[
        [
            "municipio",
            "poblacion_2025",
            "renta_media_proxy",
            "gyms_google_new",
            "fitness_x10k_new",
            "predicted_fitness_density",
            "market_gap"
        ]
    ].head(15)
    )

    print("\nTop market opportunities:")
    print(
        opportunities[
            [
                "municipio",
                "poblacion_2025",
                "renta_media_proxy",
                "gyms_google_new",
                "fitness_x10k_new",
                "predicted_fitness_density",
                "market_gap"
            ]
        ].head(15)
    )

    # ============================
    # Graficos del modelo
    # ============================
    os.makedirs("reports/figures", exist_ok=True)

    # 1) Predicción vs Realidad
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred)

    # línea ideal (predicho = real)
    plt.plot(
        [y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        "--"
    )

    plt.xlabel("Real (fitness_x10k_new)")
    plt.ylabel("Predicho")
    plt.title("Predicción vs Realidad")
    plt.tight_layout()
    plt.savefig("reports/figures/pred_vs_real.png", dpi=200)
    plt.show()

    # 2) Feature Importance
    fi_sorted = feature_importance.sort_values("importance", ascending=True)

    plt.figure(figsize=(7, 4))
    plt.barh(fi_sorted["feature"], fi_sorted["importance"])
    plt.xlabel("Importance")
    plt.title("Feature Importance (Random Forest)")
    plt.tight_layout()
    plt.savefig("reports/figures/feature_importance.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main()

# Test set
# R² = 0.58
# MAE = 3.06
# Cross-validation
# R² medio = 0.49
# MAE medio ≈ 3.49
# std R² = 0.37

# La población y la oferta de gimnasios existente explican aproximadamente la mitad de la variación en la densidad de gimnasios entre los municipios,
#  lo que sugiere que otros factores como la población del área de influencia, la demografía o la estructura urbana también juegan un papel.

