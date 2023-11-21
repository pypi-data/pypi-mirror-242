from typing import Any, Callable
from warnings import catch_warnings, simplefilter

from numpy import float64, inf, nan
from numpy.typing import NDArray

from tompy.any import (
    any_allnan,
    any_any,
    any_asarray,
    any_concatenate,
    any_copy,
    any_full,
    any_isnan,
    any_kurtosis,
    any_log,
    any_lr2sr,
    any_maximum,
    any_minimize,
    any_move_argmax,
    any_move_argmin,
    any_move_max,
    any_move_mean,
    any_move_median,
    any_move_min,
    any_move_rank,
    any_move_std,
    any_move_sum,
    any_move_var,
    any_nancumsum,
    any_nanmax,
    any_nanmean,
    any_nanmedian,
    any_nanmin,
    any_nanpercentile,
    any_nanstd,
    any_nansum,
    any_skew,
    any_sliding_window_view,
    any_sqrt,
    any_sr2lr,
    any_zeros,
)


def vector_validate(v: NDArray[float64]) -> int:
    assert v.ndim == 1
    return v.shape[0]


def vector_validate_rolling(v: NDArray[float64], window: int) -> int:
    assert window >= 0
    return vector_validate(v)


def vector_zeros(n: int) -> NDArray[float64]:
    return any_zeros(n, dtype=float64)


def vector_nans(n: int) -> NDArray[float64]:
    return any_full(n, nan, dtype=float64)


def vector_describe_meta() -> dict[str, str]:
    return {
        "COUNT": "Count",
        "MEAN": "Mean",
        "STD": "Standard Deviation",
        "SKEW": "Skewness",
        "KURT": "Kurtosis",
        "MIN": "Min",
        "25%": "25%",
        "50%": "50%",
        "75%": "75%",
        "MAX": "Max",
    }


def vector_describe(v: NDArray[float64]) -> NDArray[float64]:
    n = vector_validate(v)
    if n <= 0:
        return vector_nans(len(vector_describe_meta()))
    return any_asarray(
        [
            vector_nancnt(v),
            vector_nanmean(v),
            vector_nanstd(v),
            vector_nanskew(v),
            vector_nankurt(v),
            vector_nanpctl(v, 0),
            vector_nanpctl(v, 25),
            vector_nanpctl(v, 50),
            vector_nanpctl(v, 75),
            vector_nanpctl(v, 100),
        ],
        dtype=float64,
    )


def vector_shift(v: NDArray[float64], lag: int) -> NDArray[float64]:
    n = vector_validate(v)
    if n <= 0 or lag == 0:
        return v
    if lag > 0:
        if lag >= n:
            return vector_nans(n)
        return any_concatenate((vector_nans(lag), v[:-lag]))
    lag = -lag
    if lag >= n:
        return vector_nans(n)
    return any_concatenate((v[lag:], vector_nans(lag)))


def vector_nancnt(v: NDArray[float64]) -> float64:
    n = vector_validate(v)
    if n <= 0:
        return nan  # type: ignore
    return n - any_nansum(any_isnan(v))  # type: ignore


def vector_nanmean(v: NDArray[float64]) -> float64:
    n = vector_validate(v)
    if n <= 0:
        return nan  # type: ignore
    return any_nanmean(v)  # type: ignore


def vector_nanstd(v: NDArray[float64]) -> float64:
    n = vector_validate(v)
    if n <= 0:
        return nan  # type: ignore
    return any_nanstd(v, ddof=1)  # type: ignore


def vector_nanskew(v: NDArray[float64]) -> float64:
    n = vector_validate(v)
    if n <= 0:
        return nan  # type: ignore
    if any_allnan(v):
        return nan  # type: ignore
    return any_skew(v, axis=None, bias=False, nan_policy="omit")  # type: ignore


def vector_nankurt(v: NDArray[float64]) -> float64:
    n = vector_validate(v)
    if n <= 0:
        return nan  # type: ignore
    if any_allnan(v):
        return nan  # type: ignore
    return any_kurtosis(  # type: ignore
        v, axis=None, fisher=True, bias=False, nan_policy="omit"
    )


def vector_nanpctl(v: NDArray[float64], q: int) -> float64:
    n = vector_validate(v)
    if n <= 0:
        return nan  # type: ignore
    if q <= 0:
        return any_nanmin(v)  # type: ignore
    if q >= 100:
        return any_nanmax(v)  # type: ignore
    if q == 50:
        return any_nanmedian(v)  # type: ignore
    if any_allnan(v):
        return nan  # type: ignore
    return any_nanpercentile(v, q)


def vector_rolling_sum(v: NDArray[float64], window: int) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    return any_move_sum(v, window)  # type: ignore


def vector_rolling_mean(v: NDArray[float64], window: int) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    return any_move_mean(v, window)  # type: ignore


def vector_rolling_std(v: NDArray[float64], window: int) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    return any_move_std(v, window, ddof=1)  # type: ignore


def vector_rolling_var(v: NDArray[float64], window: int) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    return any_move_var(v, window, ddof=1)  # type: ignore


def vector_rolling_min(v: NDArray[float64], window: int) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    return any_move_min(v, window)  # type: ignore


def vector_rolling_max(v: NDArray[float64], window: int) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    return any_move_max(v, window)  # type: ignore


def vector_rolling_argmin(
    v: NDArray[float64], window: int
) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    return any_move_argmin(v, window)  # type: ignore


def vector_rolling_argmax(
    v: NDArray[float64], window: int
) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    return any_move_argmax(v, window)  # type: ignore


def vector_rolling_median(
    v: NDArray[float64], window: int
) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    return any_move_median(v, window)  # type: ignore


def vector_rolling_rank(v: NDArray[float64], window: int) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    return any_move_rank(v, window)  # type: ignore


def vector_rolling_apply(
    v: NDArray[float64],
    window: int,
    func: Callable[[NDArray[float64]], float64],
) -> NDArray[float64]:
    n = vector_validate_rolling(v, window)
    if window == 0 or window > n:
        return vector_nans(n)
    swv = any_sliding_window_view(v, window)
    ret = any_asarray([func(sw) for sw in swv], dtype=float64)
    assert ret.ndim == 1
    if window > 1:
        ret = any_concatenate((vector_nans(window - 1), ret))
    return ret


def vector_price2sr(price: NDArray[float64]) -> NDArray[float64]:
    n = vector_validate(price)
    if n <= 1:
        return vector_nans(n)
    sr = price[1:] / price[:-1] - 1
    return any_concatenate((vector_nans(1), sr))


def vector_price2lr(price: NDArray[float64]) -> NDArray[float64]:
    n = vector_validate(price)
    if n <= 1:
        return vector_nans(n)
    lr = any_log(price[1:] / price[:-1])
    return any_concatenate((vector_nans(1), lr))


def vector_price_metrics(
    price: NDArray[float64], ann_factor: float64, mode: int = 0
) -> NDArray[float64]:
    sr = vector_price2sr(price)
    lr = any_sr2lr(sr)
    return vector_lr_sr_metrics(lr, sr, ann_factor, mode=mode)


def vector_sr2lr(sr: NDArray[float64]) -> NDArray[float64]:
    n = vector_validate(sr)
    if n <= 0:
        return vector_nans(n)
    return any_sr2lr(sr)  # type: ignore


def vector_sr_objective_kelly(sr: NDArray[float64], x: float64) -> float64:
    srx = sr * x
    if any_any(srx <= -1):
        return inf  # type: ignore
    return -any_nansum(any_sr2lr(srx))  # type: ignore


def vector_sr_minimize(
    sr: NDArray[float64],
    func: Callable[[NDArray[float64], float64], float64],
    lb: None | float64 = None,
    ub: None | float64 = None,
    constraints: None | list[dict[str, Any]] = None,
) -> float64:
    with catch_warnings():
        simplefilter("ignore")

        n = vector_validate(sr)
        if n <= 0:
            return nan  # type: ignore

        eps = 1e-4
        if lb is None:
            max_sr = any_nanmax(sr)
            lb = -1 / max(max_sr, eps) + eps
        if ub is None:
            min_sr = any_nanmin(sr)
            ub = -1 / min(min_sr, -eps) - eps
        bounds = [(lb, ub)]

        x0 = vector_zeros(1)
        result = any_minimize(
            lambda x: func(sr, x[0]),
            x0,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )
        if result.success:
            return result.x[0]  # type: ignore
        return nan  # type: ignore


def vector_sr_kelly_criterion(sr: NDArray[float64]) -> float64:
    """
    Kelly Criterion with Empirical Distribution
    """
    return vector_sr_minimize(sr, vector_sr_objective_kelly)


def vector_sr_metrics(
    sr: NDArray[float64], ann_factor: float64, mode: int = 0
) -> NDArray[float64]:
    lr = any_sr2lr(sr)
    return vector_lr_sr_metrics(lr, sr, ann_factor, mode=mode)


def vector_sr_terms_metrics(
    sr: NDArray[float64], terms: list[int], ann_factor: float64, mode: int = 0
) -> NDArray[float64]:
    n = vector_validate(sr)
    lr = any_sr2lr(sr)
    nr = len(vector_lr_sr_metrics_meta(mode))

    def metrics(term: int) -> NDArray[float64]:
        if term > n:
            return vector_nans(nr)
        return vector_lr_sr_metrics(
            lr[-term:],
            sr[-term:],
            ann_factor,
            mode=mode,
        )

    return any_asarray([metrics(term) for term in terms], dtype=float64).T


def vector_lr2sr(lr: NDArray[float64]) -> NDArray[float64]:
    n = vector_validate(lr)
    if n <= 0:
        return vector_nans(n)
    return any_lr2sr(lr)  # type: ignore


def vector_lr2crdd(
    lr: NDArray[float64],
) -> tuple[NDArray[float64], NDArray[float64]]:
    n = vector_validate(lr)
    if n <= 0:
        return vector_nans(n), vector_nans(n)
    lr0_cr = any_nancumsum(lr)
    lr0_peak = any_maximum.accumulate(lr0_cr)
    lr0_dd = lr0_cr - lr0_peak
    return lr0_cr, lr0_dd


def vector_lr_metrics(
    lr: NDArray[float64], ann_factor: float64, mode: int = 0
) -> NDArray[float64]:
    sr = any_lr2sr(lr)
    return vector_lr_sr_metrics(lr, sr, ann_factor, mode=mode)


def vector_lr_sr_metrics_meta(mode: int) -> dict[str, str]:
    if mode == 0:
        return {
            "SR_CR": "[SR] Cumulative Return",
            "SR_AGR": "[SR] Annualized Growth Rate",
            "SR_DD": "[SR] Drawdown",
            "SR_ADD": "[SR] Average Drawdown",
            "SR_MDD": "[SR] Maximum Drawdown",
            "SR_KELLY": "[SR] Kelly Criterion",
            "LR_CR": "[LR] Cumulative Return",
            "LR_AGR": "[LR] Annualized Growth Rate",
            "LR_DD": "[LR] Drawdown",
            "LR_ADD": "[LR] Average Drawdown",
            "LR_MDD": "[LR] Maximum Drawdown",
            "LR_VOL": "[LR] Annualized Volatility",
            "LR_VOL-": "[LR] Annualized Volatility-",
            "LR_SHARPE": "[LR] Sharpe Ratio",
            "LR_SORTINO": "[LR] Sortino Ratio",
            "LR_WIN": "[LR] Winning Ratio",
            "LR_PLR": "[LR] Profit Loss Ratio",
        }
    assert False, "NotImplemented"


def __vector_lr_sr_metrics_mode_0(
    lr: NDArray[float64], sr: NDArray[float64], ann_factor: float64
) -> NDArray[float64]:
    lr0_cr, lr0_dd = vector_lr2crdd(lr)
    lr_cr = lr0_cr[-1]
    lr_agr = any_nanmean(lr) * ann_factor
    lr_dd = lr0_dd[-1]
    lr_add = any_nanmean(lr0_dd)
    lr_mdd = any_nanmin(lr0_dd)

    sr_cr = any_lr2sr(lr_cr)
    sr_agr = any_lr2sr(lr_agr)
    sr0_dd = any_lr2sr(lr0_dd)
    sr_dd = sr0_dd[-1]
    sr_add = any_nanmean(sr0_dd)
    sr_mdd = any_nanmin(sr0_dd)
    sr_kelly = vector_sr_kelly_criterion(sr)

    lr_vol = any_nanstd(lr, ddof=1) * any_sqrt(ann_factor)
    lr2 = any_copy(lr)
    lr2[lr2 > 0] = 0
    lr_vol2 = any_nanstd(lr2, ddof=1) * any_sqrt(ann_factor * 2)
    lr_sharpe = nan if lr_vol == 0 else lr_agr / lr_vol
    lr_sortino = nan if lr_vol2 == 0 else lr_agr / lr_vol2
    lrp = lr[lr > 0]
    lrp_count = vector_nancnt(lrp)
    lrp_mean = any_nanmean(lrp)
    lrl = lr[lr < 0]
    lrl_count = vector_nancnt(lrl)
    lrl_mean = any_nanmean(lrl)
    lr_count = lrp_count + lrl_count
    lr_win = nan if lr_count == 0 else lrp_count / lr_count
    lr_plr = nan if lrl_mean == 0 else lrp_mean / -lrl_mean

    return any_asarray(
        [
            sr_cr,
            sr_agr,
            sr_dd,
            sr_add,
            sr_mdd,
            sr_kelly,
            lr_cr,
            lr_agr,
            lr_dd,
            lr_add,
            lr_mdd,
            lr_vol,
            lr_vol2,
            lr_sharpe,
            lr_sortino,
            lr_win,
            lr_plr,
        ],
        dtype=float64,
    )


def vector_lr_sr_metrics(
    lr: NDArray[float64],
    sr: NDArray[float64],
    ann_factor: float64,
    mode: int = 0,
) -> NDArray[float64]:
    n_lr = vector_validate(lr)
    n_sr = vector_validate(sr)
    assert n_lr == n_sr
    if n_lr <= 0:
        return vector_nans(len(vector_lr_sr_metrics_meta(mode)))
    if mode == 0:
        return __vector_lr_sr_metrics_mode_0(lr, sr, ann_factor)
    assert False, "NotImplemented"
