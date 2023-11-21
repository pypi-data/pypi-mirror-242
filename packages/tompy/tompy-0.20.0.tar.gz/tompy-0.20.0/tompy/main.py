from typing import Callable

from atopy.typer import typer
from numpy import float64, nan
from numpy.typing import NDArray
from pandas import DataFrame, Series

from tompy.dataframe import dataframe_describe
from tompy.io import csv_read
from tompy.matrix import (
    matrix_portfolio_sr,
    matrix_rolling_mean,
    matrix_shift,
    matrix_sr_minimize_rolling,
    matrix_sr_objective_kelly,
    matrix_sr_objective_kelly_entropy,
    matrix_zeros,
)
from tompy.series import series_price_dterms_metrics, series_sr_dterms_metrics
from tompy.vector import vector_sr_kelly_criterion

app = typer()


def csv_read_fillna(csv: str, fillna: bool) -> DataFrame:
    df = csv_read(csv)
    assert df is not None
    if fillna:
        df = df.fillna(0)
    print(dataframe_describe(df))
    return df


def pf_objective(
    obj: str,
) -> Callable[[NDArray[float64], NDArray[float64]], float64]:
    if obj == "kelly":
        return matrix_sr_objective_kelly
    if obj == "ekelly":
        return matrix_sr_objective_kelly_entropy
    return matrix_sr_objective_kelly_entropy


def pf_stat(
    sr: NDArray[float64], w: NDArray[float64], lag: int = 0
) -> tuple[DataFrame, NDArray[float64], NDArray[float64]]:
    wlag = matrix_shift(w, 1 + lag)
    pfsr = matrix_portfolio_sr(sr, wlag)
    pfst = series_sr_dterms_metrics(Series(pfsr))
    return pfst, pfsr, wlag


def pf_dump(
    df: DataFrame,
    w: NDArray[float64],
    pfst: DataFrame,
    pfsr: NDArray[float64],
    wlag: NDArray[float64],
    window1: int,
    window2: int,
    prefix: str = "",
) -> None:
    idx = df.index
    cols = df.columns
    dfw = DataFrame(w, index=idx, columns=cols, dtype=float64)
    print(
        window1,
        window2,
        "\n",
        pfst,
        "\n",
        dfw.tail().applymap(lambda x: f"{x:.4f}"),
    )
    if prefix:
        prefix = f"{prefix}_{window1}_{window2}"
        dfw.to_csv(f"{prefix}_w.csv")
        DataFrame(wlag, index=idx, columns=cols, dtype=float64).to_csv(
            f"{prefix}_wlag.csv"
        )
        DataFrame(
            pfsr.reshape(-1, 1), index=idx, columns=["sr"], dtype=float64
        ).to_csv(f"{prefix}_pfsr.csv")
        pfst.to_csv(f"{prefix}_pfst.csv")


@app.command()
def pr_stat(pr_csv: str, mode: int = 0) -> None:
    df = csv_read_fillna(pr_csv, False)
    for col in df:
        df2 = series_price_dterms_metrics(df[col], mode=mode)
        print(col, "\n", df2)


@app.command()
def sr_stat(sr_csv: str, fillna: bool = True, mode: int = 0) -> None:
    df = csv_read_fillna(sr_csv, fillna)
    for col in df:
        df2 = series_sr_dterms_metrics(df[col], mode=mode)
        print(col, "\n", df2)


@app.command()
def sr_kelly(sr_csv: str, fillna: bool = True) -> None:
    df = csv_read_fillna(sr_csv, fillna)
    sr = df.values.astype(float64)
    nc = sr.shape[1]
    for i in range(nc):
        k = vector_sr_kelly_criterion(sr[:, i])
        print(df.columns[i], k)


@app.command()
def sr_pf_eq(
    sr_csv: str,
    skip: int,
    fillna: bool = True,
    dump_prefix: str = "",
) -> None:
    df = csv_read_fillna(sr_csv, fillna)
    sr = df.values.astype(float64)
    nr, nc = sr.shape
    w2 = matrix_zeros(nr, nc) + (1 / nc)
    w2[:skip, :] = nan
    pfst, pfsr, wlag = pf_stat(sr, w2, lag=0)
    pf_dump(df, w2, pfst, pfsr, wlag, 0, 0, prefix=dump_prefix)


@app.command()
def sr_pf_sim(
    sr_csv: str,
    obj: str,
    max_lookback: int,
    max_moveavg: int,
    lag: int,
    fillna: bool = True,
    dump_prefix: str = "",
) -> None:
    df = csv_read_fillna(sr_csv, fillna)
    skip = max_lookback + max_moveavg - 1
    objective = pf_objective(obj)
    sr = df.values.astype(float64)
    for window1 in range(1, max_lookback + 1):
        w1 = matrix_sr_minimize_rolling(sr, window1, objective)
        for window2 in range(1, max_moveavg + 1):
            w2 = matrix_rolling_mean(w1, window2)
            w2[:skip, :] = nan
            pfst, pfsr, wlag = pf_stat(sr, w2, lag=lag)
            pf_dump(
                df, w2, pfst, pfsr, wlag, window1, window2, prefix=dump_prefix
            )


@app.command()
def sr_pf_one(
    sr_csv: str,
    obj: str,
    lookback: int,
    moveavg: int,
    skip: int,
    lag: int,
    fillna: bool = True,
    dump_prefix: str = "",
) -> None:
    df = csv_read_fillna(sr_csv, fillna)
    objective = pf_objective(obj)
    sr = df.values.astype(float64)
    window1 = lookback
    w1 = matrix_sr_minimize_rolling(sr, window1, objective)
    window2 = moveavg
    w2 = matrix_rolling_mean(w1, window2)
    if skip > 0:
        w2[:skip, :] = nan
    pfst, pfsr, wlag = pf_stat(sr, w2, lag=lag)
    pf_dump(df, w2, pfst, pfsr, wlag, window1, window2, prefix=dump_prefix)


if __name__ == "__main__":
    app()
