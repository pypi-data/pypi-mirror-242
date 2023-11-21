from numpy import float64
from pandas import DataFrame, Series

from tompy.any import any_abs
from tompy.matrix import (
    matrix_describe,
    matrix_describe_meta,
    matrix_lr2crdd,
    matrix_lr2sr,
    matrix_lr_metrics,
    matrix_lr_sr_metrics,
    matrix_lr_sr_metrics_meta,
    matrix_portfolio_price,
    matrix_price2lr,
    matrix_price2sr,
    matrix_price_metrics,
    matrix_rolling_max,
    matrix_rolling_mean,
    matrix_rolling_min,
    matrix_rolling_std,
    matrix_rolling_sum,
    matrix_rolling_var,
    matrix_shift,
    matrix_sr2lr,
    matrix_sr_metrics,
)
from tompy.series import series_rolling_corr, series_shift


def dataframe_drop_weekends(df: DataFrame) -> DataFrame:
    return df[df.index.dayofweek < 5]


def dataframe_describe(df: DataFrame) -> DataFrame:
    return DataFrame(
        data=matrix_describe(df.values.astype(float64)),
        index=matrix_describe_meta().keys(),
        columns=df.columns,
        dtype=float64,
    )


def dataframe_shift(df: DataFrame, lag: int) -> DataFrame:
    if lag == 0:
        return df
    return DataFrame(
        data=matrix_shift(df.values.astype(float64), lag),
        index=df.index,
        columns=df.columns,
        dtype=float64,
    )


def dataframe_rolling_sum(df: DataFrame, window: int) -> DataFrame:
    return DataFrame(
        data=matrix_rolling_sum(df.values.astype(float64), window),
        index=df.index,
        columns=df.columns,
        dtype=float64,
    )


def dataframe_rolling_mean(df: DataFrame, window: int) -> DataFrame:
    return DataFrame(
        data=matrix_rolling_mean(df.values.astype(float64), window),
        index=df.index,
        columns=df.columns,
        dtype=float64,
    )


def dataframe_rolling_std(df: DataFrame, window: int) -> DataFrame:
    return DataFrame(
        data=matrix_rolling_std(df.values.astype(float64), window),
        index=df.index,
        columns=df.columns,
        dtype=float64,
    )


def dataframe_rolling_var(df: DataFrame, window: int) -> DataFrame:
    return DataFrame(
        data=matrix_rolling_var(df.values.astype(float64), window),
        index=df.index,
        columns=df.columns,
        dtype=float64,
    )


def dataframe_rolling_min(df: DataFrame, window: int) -> DataFrame:
    return DataFrame(
        data=matrix_rolling_min(df.values.astype(float64), window),
        index=df.index,
        columns=df.columns,
        dtype=float64,
    )


def dataframe_rolling_max(df: DataFrame, window: int) -> DataFrame:
    return DataFrame(
        data=matrix_rolling_max(df.values.astype(float64), window),
        index=df.index,
        columns=df.columns,
        dtype=float64,
    )


def dataframe_rolling_corr(
    df: DataFrame, window: int, cidx: int = 0
) -> DataFrame:
    s = df[df.columns[cidx]]
    df2 = DataFrame(index=df.index, columns=df.columns, dtype=float64)
    for col in df:
        df2[col] = series_rolling_corr(s, df[col], window)
    return df2


def dataframe_rolling_ema(df: DataFrame, window: int) -> DataFrame:
    return df.ewm(span=window, adjust=False).mean()


def dataframe_price2sr(price: DataFrame) -> DataFrame:
    return DataFrame(
        data=matrix_price2sr(price.values.astype(float64)),
        index=price.index,
        columns=price.columns,
        dtype=float64,
    )


def dataframe_price2lr(price: DataFrame) -> DataFrame:
    return DataFrame(
        data=matrix_price2lr(price.values.astype(float64)),
        index=price.index,
        columns=price.columns,
        dtype=float64,
    )


def dataframe_price_metrics(
    price: DataFrame, ann_factor: float64, mode: int = 0
) -> DataFrame:
    return DataFrame(
        data=matrix_price_metrics(
            price.values.astype(float64), ann_factor, mode=mode
        ),
        index=matrix_lr_sr_metrics_meta(mode).keys(),
        columns=price.columns,
        dtype=float64,
    )


def dataframe_sr2lr(sr: DataFrame) -> DataFrame:
    return DataFrame(
        data=matrix_sr2lr(sr.values.astype(float64)),
        index=sr.index,
        columns=sr.columns,
        dtype=float64,
    )


def dataframe_sr_metrics(
    sr: DataFrame, ann_factor: float64, mode: int = 0
) -> DataFrame:
    return DataFrame(
        data=matrix_sr_metrics(
            sr.values.astype(float64), ann_factor, mode=mode
        ),
        index=matrix_lr_sr_metrics_meta(mode).keys(),
        columns=sr.columns,
        dtype=float64,
    )


def dataframe_lr2sr(lr: DataFrame) -> DataFrame:
    return DataFrame(
        data=matrix_lr2sr(lr.values.astype(float64)),
        index=lr.index,
        columns=lr.columns,
        dtype=float64,
    )


def dataframe_lr2crdd(lr: DataFrame) -> dict[str, DataFrame]:
    lr0_cr, lr0_dd = matrix_lr2crdd(lr.values.astype(float64))
    return {
        "LR_CR": DataFrame(
            data=lr0_cr, index=lr.index, columns=lr.columns, dtype=float64
        ),
        "LR_DD": DataFrame(
            data=lr0_dd, index=lr.index, columns=lr.columns, dtype=float64
        ),
    }


def dataframe_lr_metrics(
    lr: DataFrame, ann_factor: float64, mode: int = 0
) -> DataFrame:
    return DataFrame(
        data=matrix_lr_metrics(
            lr.values.astype(float64), ann_factor, mode=mode
        ),
        index=matrix_lr_sr_metrics_meta(mode).keys(),
        columns=lr.columns,
        dtype=float64,
    )


def dataframe_lr_sr_metrics(
    lr: DataFrame, sr: DataFrame, ann_factor: float64, mode: int = 0
) -> DataFrame:
    return DataFrame(
        data=matrix_lr_sr_metrics(
            lr.values.astype(float64),
            sr.values.astype(float64),
            ann_factor,
            mode=mode,
        ),
        index=matrix_lr_sr_metrics_meta(mode).keys(),
        columns=lr.columns,
        dtype=float64,
    )


def dataframe_portfolio_price(
    price: DataFrame, weights: DataFrame, fee_rate: float64
) -> Series:
    price = price[weights.columns]
    price = price.loc[weights.index]
    return Series(
        data=matrix_portfolio_price(
            price.values.astype(float64),
            weights.values.astype(float64),
            fee_rate,
        ),
        index=price.index,
        dtype=float64,
    )


def dataframe_ohlc_true_range(
    ohlc: DataFrame, col_h: str, col_l: str, col_c: str
) -> Series:
    h = ohlc[col_h]
    l = ohlc[col_l]
    c = ohlc[col_c]
    c1 = series_shift(c, 1)
    hl = h - l
    hc = any_abs(h - c1)
    lc = any_abs(l - c1)
    tr = DataFrame({"hl": hl, "hc": hc, "lc": lc}).max(axis=1, skipna=False)
    return tr


def dataframe_ohlc_range(ohlc: DataFrame, col_h: str, col_l: str) -> Series:
    h = ohlc[col_h]
    l = ohlc[col_l]
    hl = h - l
    return hl
