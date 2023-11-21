from typing import Any, Callable
from warnings import catch_warnings, simplefilter

from numpy import float64, inf, nan
from numpy.typing import NDArray

from tompy.any import (
    any_abs,
    any_allnan,
    any_any,
    any_anynan,
    any_asarray,
    any_concatenate,
    any_dot,
    any_full,
    any_isnan,
    any_kurtosis,
    any_log,
    any_logical_and,
    any_logical_not,
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
    any_sr2lr,
    any_zeros,
)
from tompy.vector import (
    vector_describe_meta,
    vector_lr_sr_metrics,
    vector_lr_sr_metrics_meta,
    vector_nans,
    vector_zeros,
)


def matrix_validate(m: NDArray[float64]) -> tuple[int, int]:
    assert m.ndim == 2
    return m.shape  # type: ignore


def matrix_validate_rolling(
    m: NDArray[float64], window: int
) -> tuple[int, int]:
    assert window >= 0
    return matrix_validate(m)


def matrix_zeros(nr: int, nc: int) -> NDArray[float64]:
    return any_zeros((nr, nc), dtype=float64)


def matrix_nans(nr: int, nc: int) -> NDArray[float64]:
    return any_full((nr, nc), nan, dtype=float64)


def matrix_describe_meta() -> dict[str, str]:
    return vector_describe_meta()


def matrix_describe(m: NDArray[float64]) -> NDArray[float64]:
    nr, nc = matrix_validate(m)
    if nr <= 0:
        return matrix_nans(len(matrix_describe_meta()), nc)
    return any_asarray(
        [
            matrix_nancnt(m),
            matrix_nanmean(m),
            matrix_nanstd(m),
            matrix_nanskew(m),
            matrix_nankurt(m),
            matrix_nanpctl(m, 0),
            matrix_nanpctl(m, 25),
            matrix_nanpctl(m, 50),
            matrix_nanpctl(m, 75),
            matrix_nanpctl(m, 100),
        ],
        dtype=float64,
    )


def matrix_shift(m: NDArray[float64], lag: int) -> NDArray[float64]:
    nr, nc = matrix_validate(m)
    if nr <= 0 or lag == 0:
        return m
    if lag > 0:
        if lag >= nr:
            return matrix_nans(nr, nc)
        return any_concatenate((matrix_nans(lag, nc), m[:-lag, :]))
    lag = -lag
    if lag >= nr:
        return matrix_nans(nr, nc)
    return any_concatenate((m[lag:, :], matrix_nans(lag, nc)))


def matrix_nancnt(m: NDArray[float64]) -> NDArray[float64]:
    nr, nc = matrix_validate(m)
    if nr <= 0:
        return matrix_nans(0, nc)
    return nr - any_nansum(any_isnan(m), axis=0)  # type: ignore


def matrix_nanmean(m: NDArray[float64]) -> NDArray[float64]:
    nr, nc = matrix_validate(m)
    if nr <= 0:
        return matrix_nans(0, nc)
    return any_nanmean(m, axis=0)  # type: ignore


def matrix_nanstd(m: NDArray[float64]) -> NDArray[float64]:
    nr, nc = matrix_validate(m)
    if nr <= 0:
        return matrix_nans(0, nc)
    return any_nanstd(m, axis=0, ddof=1)  # type: ignore


def matrix_nanskew(m: NDArray[float64]) -> NDArray[float64]:
    nr, nc = matrix_validate(m)
    if nr <= 0:
        return matrix_nans(0, nc)
    if any_allnan(m):
        return matrix_nans(1, nc)
    return any_skew(m, axis=0, bias=False, nan_policy="omit")  # type: ignore


def matrix_nankurt(m: NDArray[float64]) -> NDArray[float64]:
    nr, nc = matrix_validate(m)
    if nr <= 0:
        return matrix_nans(0, nc)
    if any_allnan(m):
        return matrix_nans(1, nc)
    return any_kurtosis(  # type: ignore
        m, axis=0, fisher=True, bias=False, nan_policy="omit"
    )


def matrix_nanpctl(m: NDArray[float64], q: int) -> NDArray[float64]:
    nr, nc = matrix_validate(m)
    if nr <= 0:
        return matrix_nans(0, nc)
    if q <= 0:
        return any_nanmin(m, axis=0)  # type: ignore
    if q >= 100:
        return any_nanmax(m, axis=0)  # type: ignore
    if q == 50:
        return any_nanmedian(m, axis=0)  # type: ignore
    if any_allnan(m):
        return matrix_nans(1, nc)
    return any_nanpercentile(m, q, axis=0)  # type: ignore


def matrix_rolling_sum(m: NDArray[float64], window: int) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if window == 0 or window > nr:
        return matrix_nans(nr, nc)
    return any_move_sum(m, window, axis=0)  # type: ignore


def matrix_rolling_mean(m: NDArray[float64], window: int) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if window == 0 or window > nr:
        return matrix_nans(nr, nc)
    return any_move_mean(m, window, axis=0)  # type: ignore


def matrix_rolling_std(m: NDArray[float64], window: int) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if window == 0 or window > nr:
        return matrix_nans(nr, nc)
    return any_move_std(m, window, axis=0, ddof=1)  # type: ignore


def matrix_rolling_var(m: NDArray[float64], window: int) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if window == 0 or window > nr:
        return matrix_nans(nr, nc)
    return any_move_var(m, window, axis=0, ddof=1)  # type: ignore


def matrix_rolling_min(m: NDArray[float64], window: int) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if window == 0 or window > nr:
        return matrix_nans(nr, nc)
    return any_move_min(m, window, axis=0)  # type: ignore


def matrix_rolling_max(m: NDArray[float64], window: int) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if window == 0 or window > nr:
        return matrix_nans(nr, nc)
    return any_move_max(m, window, axis=0)  # type: ignore


def matrix_rolling_argmin(
    m: NDArray[float64], window: int
) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if window == 0 or window > nr:
        return matrix_nans(nr, nc)
    return any_move_argmin(m, window, axis=0)  # type: ignore


def matrix_rolling_argmax(
    m: NDArray[float64], window: int
) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if window == 0 or window > nr:
        return matrix_nans(nr, nc)
    return any_move_argmax(m, window, axis=0)  # type: ignore


def matrix_rolling_median(
    m: NDArray[float64], window: int
) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if window == 0 or window > nr:
        return matrix_nans(nr, nc)
    return any_move_median(m, window, axis=0)  # type: ignore


def matrix_rolling_rank(m: NDArray[float64], window: int) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if window == 0 or window > nr:
        return matrix_nans(nr, nc)
    return any_move_rank(m, window, axis=0)  # type: ignore


def matrix_rolling_apply(
    m: NDArray[float64],
    window: int,
    func: Callable[[NDArray[float64]], NDArray[float64]],
    nfout: None | int = None,
) -> NDArray[float64]:
    nr, nc = matrix_validate_rolling(m, window)
    if nfout is None:
        nfout = nc
    if window == 0 or window > nr:
        return matrix_nans(nr, nfout)
    swv = any_sliding_window_view(m, (window, nc)).reshape((-1, window, nc))
    ret = any_asarray([func(sw) for sw in swv], dtype=float64)
    assert ret.ndim == 2 and ret.shape[1] == nfout
    if window > 1:
        ret = any_concatenate((matrix_nans(window - 1, nfout), ret))
    return ret


def matrix_price2sr(price: NDArray[float64]) -> NDArray[float64]:
    nr, nc = matrix_validate(price)
    if nr <= 1 or nc <= 0:
        return matrix_nans(nr, nc)
    sr = price[1:, :] / price[:-1, :] - 1
    return any_concatenate((matrix_nans(1, nc), sr))


def matrix_price2lr(price: NDArray[float64]) -> NDArray[float64]:
    nr, nc = matrix_validate(price)
    if nr <= 1 or nc <= 0:
        return matrix_nans(nr, nc)
    lr = any_log(price[1:, :] / price[:-1, :])
    return any_concatenate((matrix_nans(1, nc), lr))


def matrix_price_metrics(
    price: NDArray[float64], ann_factor: float64, mode: int = 0
) -> NDArray[float64]:
    sr = matrix_price2sr(price)
    lr = any_sr2lr(sr)
    return matrix_lr_sr_metrics(lr, sr, ann_factor, mode=mode)


def matrix_sr2lr(sr: NDArray[float64]) -> NDArray[float64]:
    nr, nc = matrix_validate(sr)
    if nr <= 0:
        return matrix_nans(nr, nc)
    return any_sr2lr(sr)  # type: ignore


def matrix_sr_objective_kelly(
    sr: NDArray[float64], x: NDArray[float64]
) -> float64:
    srx = any_dot(sr, x)
    if any_any(srx <= -1):
        return inf  # type: ignore
    return -any_nansum(any_sr2lr(srx))  # type: ignore


def matrix_sr_objective_kelly_entropy(
    sr: NDArray[float64], x: NDArray[float64]
) -> float64:
    p = x[any_logical_and(x > 0, x < 1)]
    entropy = -any_nansum(p * any_log(p))
    ret = matrix_sr_objective_kelly(sr, x) * (entropy + 1)
    return ret  # type: ignore


def matrix_sr_minimize(
    sr: NDArray[float64],
    func: Callable[[NDArray[float64], NDArray[float64]], float64],
    lbf: None | Callable[[int], float64] = None,
    ubf: None | Callable[[int], float64] = None,
    constraints: None | list[dict[str, Any]] = None,
) -> NDArray[float64]:
    with catch_warnings():
        simplefilter("ignore")

        nr, nc0 = matrix_validate(sr)
        if nr <= 0:
            return vector_nans(nc0)

        isvalid = any_logical_not(any_anynan(sr, axis=0))
        sr1 = sr[:, isvalid]
        nc1 = sr1.shape[1]
        if nc1 <= 0:
            return vector_nans(nc0)

        lb = 0 if lbf is None else lbf(nc1)
        ub = 1 if ubf is None else ubf(nc1)
        bounds = [(lb, ub)] * nc1

        if constraints is None:
            constraints = [
                {"type": "ineq", "fun": lambda x: 1 - any_nansum(x)},
            ]

        x0 = vector_zeros(nc1) + (1 / nc1)
        result = any_minimize(
            lambda x: func(sr1, x),
            x0,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )
        if result.success:
            ret = vector_zeros(nc0)
            ret[isvalid] = result.x
            return ret
        return vector_nans(nc0)


def matrix_sr_minimize_rolling(
    sr: NDArray[float64],
    window: int,
    func: Callable[[NDArray[float64], NDArray[float64]], float64],
    lbf: None | Callable[[int], float64] = None,
    ubf: None | Callable[[int], float64] = None,
    constraints: None | list[dict[str, Any]] = None,
) -> NDArray[float64]:
    return matrix_rolling_apply(
        sr,
        window,
        lambda x: matrix_sr_minimize(
            x, func, lbf=lbf, ubf=ubf, constraints=constraints
        ),
    )


def matrix_sr_minimize_rolling_ensemble(
    sr: NDArray[float64],
    windows: list[int],
    func: Callable[[NDArray[float64], NDArray[float64]], float64],
    lbf: None | Callable[[int], float64] = None,
    ubf: None | Callable[[int], float64] = None,
    constraints: None | list[dict[str, Any]] = None,
) -> NDArray[float64]:
    nr, nc = matrix_validate(sr)
    if nr <= 0:
        return matrix_nans(nr, nc)
    ws = matrix_zeros(nr, nc)
    for window in windows:
        wi = matrix_sr_minimize_rolling(
            sr, window, func, lbf=lbf, ubf=ubf, constraints=constraints
        )
        ws = ws + wi
    w = ws / len(windows)
    return w


def matrix_sr_metrics(
    sr: NDArray[float64], ann_factor: float64, mode: int = 0
) -> NDArray[float64]:
    lr = any_sr2lr(sr)
    return matrix_lr_sr_metrics(lr, sr, ann_factor, mode=mode)


def matrix_lr2sr(lr: NDArray[float64]) -> NDArray[float64]:
    nr, nc = matrix_validate(lr)
    if nr <= 0:
        return matrix_nans(nr, nc)
    return any_lr2sr(lr)  # type: ignore


def matrix_lr2crdd(
    lr: NDArray[float64],
) -> tuple[NDArray[float64], NDArray[float64]]:
    nr, nc = matrix_validate(lr)
    if nr <= 0:
        return matrix_nans(nr, nc), matrix_nans(nr, nc)
    lr0_cr = any_nancumsum(lr, axis=0)
    lr0_peak = any_maximum.accumulate(lr0_cr, axis=0)
    lr0_dd = lr0_cr - lr0_peak
    return lr0_cr, lr0_dd


def matrix_lr_metrics(
    lr: NDArray[float64], ann_factor: float64, mode: int = 0
) -> NDArray[float64]:
    sr = any_lr2sr(lr)
    return matrix_lr_sr_metrics(lr, sr, ann_factor, mode=mode)


def matrix_lr_sr_metrics_meta(mode: int) -> dict[str, str]:
    return vector_lr_sr_metrics_meta(mode)


def matrix_lr_sr_metrics(
    lr: NDArray[float64],
    sr: NDArray[float64],
    ann_factor: float64,
    mode: int = 0,
) -> NDArray[float64]:
    nr_lr, nc_lr = matrix_validate(lr)
    nr_sr, nc_sr = matrix_validate(sr)
    assert nr_lr == nr_sr and nc_lr == nc_sr
    if nr_lr <= 0:
        return matrix_nans(len(matrix_lr_sr_metrics_meta(mode)), nc_lr)
    return any_asarray(
        [
            vector_lr_sr_metrics(lr[:, i], sr[:, i], ann_factor, mode=mode)
            for i in range(nc_lr)
        ],
        dtype=float64,
    ).T


def matrix_portfolio_price(
    price: NDArray[float64], weight: NDArray[float64], fee_rate: float64
) -> NDArray[float64]:
    price_shape = matrix_validate(price)
    weight_shape = matrix_validate(weight)
    assert price_shape == weight_shape
    nr, nc = weight_shape
    nav = 1
    position_quantity = vector_zeros(nc)
    cash = 1
    navs = vector_zeros(nr)
    for i in range(nr):
        pi = price[i]
        wi = weight[i]
        nav = cash + any_nansum(position_quantity * pi)
        if not any_allnan(wi):
            target_position_dollar = nav * wi
            target_position_quantity = target_position_dollar / pi
            trading_position_quantity = (
                target_position_quantity - position_quantity
            )
            trading_position_dollar = trading_position_quantity * pi
            trading_fee = (
                any_nansum(any_abs(trading_position_dollar)) * fee_rate
            )
            nav = (
                cash
                - any_nansum(trading_position_dollar)
                + any_nansum(target_position_dollar)
                - trading_fee
            )
            position_dollar = nav * wi
            position_quantity = position_dollar / pi
            cash = nav - any_nansum(position_dollar)
        navs[i] = nav
    return navs


def matrix_portfolio_sr(
    sr: NDArray[float64], weight: NDArray[float64]
) -> NDArray[float64]:
    sr_shape = matrix_validate(sr)
    weight_shape = matrix_validate(weight)
    assert sr_shape == weight_shape
    ret = any_nansum((sr * weight), axis=1)
    ret[any_allnan(weight, axis=1)] = nan
    return ret  # type: ignore
