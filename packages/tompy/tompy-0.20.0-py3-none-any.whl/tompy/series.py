from numpy import float64
from pandas import DataFrame, Series

from tompy.any import any_asarray
from tompy.vector import (
    vector_describe,
    vector_describe_meta,
    vector_lr2crdd,
    vector_lr2sr,
    vector_lr_metrics,
    vector_lr_sr_metrics,
    vector_lr_sr_metrics_meta,
    vector_price2lr,
    vector_price2sr,
    vector_price_metrics,
    vector_rolling_max,
    vector_rolling_mean,
    vector_rolling_min,
    vector_rolling_std,
    vector_rolling_sum,
    vector_rolling_var,
    vector_shift,
    vector_sr2lr,
    vector_sr_metrics,
    vector_sr_terms_metrics,
)


def series_describe(s: Series) -> Series:
    return Series(
        data=vector_describe(s.values.astype(float64)),
        index=vector_describe_meta().keys(),
        dtype=float64,
    )


def series_shift(s: Series, lag: int) -> Series:
    if lag == 0:
        return s
    return Series(
        data=vector_shift(s.values.astype(float64), lag),
        index=s.index,
        dtype=float64,
    )


def series_rolling_sum(s: Series, window: int) -> Series:
    return Series(
        data=vector_rolling_sum(s.values.astype(float64), window),
        index=s.index,
        dtype=float64,
    )


def series_rolling_mean(s: Series, window: int) -> Series:
    return Series(
        data=vector_rolling_mean(s.values.astype(float64), window),
        index=s.index,
        dtype=float64,
    )


def series_rolling_std(s: Series, window: int) -> Series:
    return Series(
        data=vector_rolling_std(s.values.astype(float64), window),
        index=s.index,
        dtype=float64,
    )


def series_rolling_var(s: Series, window: int) -> Series:
    return Series(
        data=vector_rolling_var(s.values.astype(float64), window),
        index=s.index,
        dtype=float64,
    )


def series_rolling_min(s: Series, window: int) -> Series:
    return Series(
        data=vector_rolling_min(s.values.astype(float64), window),
        index=s.index,
        dtype=float64,
    )


def series_rolling_max(s: Series, window: int) -> Series:
    return Series(
        data=vector_rolling_max(s.values.astype(float64), window),
        index=s.index,
        dtype=float64,
    )


def series_rolling_corr(s1: Series, s2: Series, window: int) -> Series:
    return s1.rolling(window).corr(s2, ddof=1)


def series_rolling_ema(s: Series, window: int) -> Series:
    return s.ewm(span=window, adjust=False).mean()


def series_price2sr(price: Series) -> Series:
    return Series(
        data=vector_price2sr(price.values.astype(float64)),
        index=price.index,
        dtype=float64,
    )


def series_price2lr(price: Series) -> Series:
    return Series(
        data=vector_price2lr(price.values.astype(float64)),
        index=price.index,
        dtype=float64,
    )


def series_price_metrics(
    price: Series, ann_factor: float64, mode: int = 0
) -> Series:
    return Series(
        data=vector_price_metrics(
            price.values.astype(float64), ann_factor, mode=mode
        ),
        index=vector_lr_sr_metrics_meta(mode).keys(),
        dtype=float64,
    )


def series_price_dterms_metrics(price: Series, mode: int = 0) -> DataFrame:
    sr = series_price2sr(price)
    return series_sr_dterms_metrics(sr, mode=mode)


def series_sr2lr(sr: Series) -> Series:
    return Series(
        data=vector_sr2lr(sr.values.astype(float64)),
        index=sr.index,
        dtype=float64,
    )


def series_sr_metrics(
    sr: Series, ann_factor: float64, mode: int = 0
) -> Series:
    return Series(
        data=vector_sr_metrics(
            sr.values.astype(float64), ann_factor, mode=mode
        ),
        index=vector_lr_sr_metrics_meta(mode).keys(),
        dtype=float64,
    )


def series_sr_terms_metrics(
    sr: Series, terms: dict[str, int], ann_factor: float64, mode: int = 0
) -> DataFrame:
    return DataFrame(
        data=vector_sr_terms_metrics(
            sr.values.astype(float64),
            list(terms.values()),
            ann_factor,
            mode=mode,
        ),
        index=vector_lr_sr_metrics_meta(mode).keys(),
        columns=terms.keys(),
        dtype=float64,
    )


def series_sr_dterms_metrics(sr: Series, mode: int = 0) -> DataFrame:
    n = sr.shape[0]
    ann_factor = float64(252)
    D = 1
    W = 5
    M = 21
    Y = M * 12
    terms = {
        "1D": 1 * D,
        "1W": 1 * W,
        "2W": 2 * W,
        "1M": 1 * M,
        "3M": 3 * M,
        "6M": 6 * M,
        "1Y": 1 * Y,
        "3Y": 3 * Y,
        "5Y": 5 * Y,
        "10Y": 10 * Y,
        "ITD": n,
    }
    return series_sr_terms_metrics(sr, terms, ann_factor, mode=mode)


def series_lr2sr(lr: Series) -> Series:
    return Series(
        data=vector_lr2sr(lr.values.astype(float64)),
        index=lr.index,
        dtype=float64,
    )


def series_lr2crdd(lr: Series) -> DataFrame:
    lr0_cr, lr0_dd = vector_lr2crdd(lr.values.astype(float64))
    return DataFrame(
        data=any_asarray([lr0_cr, lr0_dd], dtype=float64).T,
        index=lr.index,
        columns=["LR_CR", "LR_DD"],
        dtype=float64,
    )


def series_lr_metrics(
    lr: Series, ann_factor: float64, mode: int = 0
) -> Series:
    return Series(
        data=vector_lr_metrics(
            lr.values.astype(float64), ann_factor, mode=mode
        ),
        index=vector_lr_sr_metrics_meta(mode).keys(),
        dtype=float64,
    )


def series_lr_sr_metrics(
    lr: Series, sr: Series, ann_factor: float64, mode: int = 0
) -> Series:
    return Series(
        data=vector_lr_sr_metrics(
            lr.values.astype(float64),
            sr.values.astype(float64),
            ann_factor,
            mode=mode,
        ),
        index=vector_lr_sr_metrics_meta(mode).keys(),
        dtype=float64,
    )
