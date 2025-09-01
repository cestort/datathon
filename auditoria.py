# auditoria.py
import numpy as np
import pandas as pd
from typing import Iterable, Optional

def audit_pair(
    train: pd.DataFrame,
    test: pd.DataFrame,
    name: str,
    check_nans: bool = True,
    allow_nans_cols: Optional[Iterable[str]] = None,
    check_order: bool = False,
) -> bool:
    """
    Verifica integridad entre dos DataFrames (TRAIN/TEST).

    - Comprueba que tienen las mismas columnas (y opcionalmente el mismo orden).
    - Si check_nans=True, asegura que no hay NaN fuera de allow_nans_cols.
    - Imprime un resumen 'OK' si todo pasa. Lanza AssertionError si algo falla.
    - Devuelve True si todo está correcto.

    Params
    ------
    train, test : pd.DataFrame
    name        : nombre legible del conjunto (p. ej. 'Escenario 3')
    check_nans  : si False, no se validan NaN (útil en datos crudos)
    allow_nans_cols : columnas donde se permiten NaN (p. ej. ['x8'])
    check_order : si True, exige el mismo ORDEN de columnas además del mismo conjunto

    """
    # 1) mismas columnas
    cols_train, cols_test = list(train.columns), list(test.columns)
    assert set(cols_train) == set(cols_test), f"[{name}] columnas no alineadas"

    if check_order:
        assert cols_train == cols_test, f"[{name}] mismo conjunto, PERO distinto ORDEN de columnas"

    if not check_nans:
        print(f"[OK] {name}: {train.shape} / {test.shape} (solo columnas; NaN permitidos)")
        return True

    # 2) chequeo NaN (permitiendo algunos campos)
    allow = set(allow_nans_cols or [])
    tr = train.drop(columns=[c for c in allow if c in train.columns], errors='ignore')
    ts = test.drop(columns=[c for c in allow if c in test.columns], errors='ignore')

    nan_tr = int(np.isnan(tr.values).sum())
    nan_ts = int(np.isnan(ts.values).sum())

    assert nan_tr == 0, f"[{name}] NaN en TRAIN fuera de {sorted(allow)}"
    assert nan_ts == 0, f"[{name}] NaN en TEST fuera de {sorted(allow)}"

    print(f"[OK] {name}: {train.shape} / {test.shape} (columnas alineadas; NaN solo en {sorted(allow)})")
    return True


def missing_report(df: pd.DataFrame, title: str, top: int = 20) -> None:
    """Imprime un ranking de columnas con NaN (para diagnóstico)."""
    miss = df.isna().sum()
    miss = miss[miss > 0].sort_values(ascending=False)
    print(f"\n[{title}] columnas con NaN:")
    if miss.empty:
        print("  (sin NaN)")
    else:
        print(miss.head(top))
