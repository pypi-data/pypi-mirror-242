from typing import Any

from bottleneck import (
    allnan,
    anynan,
    move_argmax,
    move_argmin,
    move_max,
    move_mean,
    move_median,
    move_min,
    move_rank,
    move_std,
    move_sum,
    move_var,
    nanmax,
    nanmean,
    nanmedian,
    nanmin,
    nanstd,
    nansum,
)
from numpy import (  # pylint: disable=redefined-builtin
    abs,
    all,
    any,
    asarray,
    concatenate,
    copy,
    dot,
    exp,
    full,
    isnan,
    log,
    logical_and,
    logical_not,
    max,
    maximum,
    min,
    nancumsum,
    nanpercentile,
    sqrt,
    zeros,
)
from numpy.lib.stride_tricks import sliding_window_view
from scipy.optimize import minimize
from scipy.stats import kurtosis, skew

# bottleneck
any_allnan = allnan
any_anynan = anynan
any_move_argmax = move_argmax
any_move_argmin = move_argmin
any_move_max = move_max
any_move_mean = move_mean
any_move_median = move_median
any_move_min = move_min
any_move_rank = move_rank
any_move_std = move_std
any_move_sum = move_sum
any_move_var = move_var
any_nanmax = nanmax
any_nanmean = nanmean
any_nanmedian = nanmedian
any_nanmin = nanmin
any_nanstd = nanstd
any_nansum = nansum

# numpy
any_abs = abs
any_all = all
any_any = any
any_asarray = asarray
any_concatenate = concatenate
any_copy = copy
any_dot = dot
any_exp = exp
any_full = full
any_isnan = isnan
any_log = log
any_logical_and = logical_and
any_logical_not = logical_not
any_max = max
any_maximum = maximum
any_min = min
any_nancumsum = nancumsum
any_nanpercentile = nanpercentile
any_sqrt = sqrt
any_zeros = zeros

# numpy.lib.stride_tricks
any_sliding_window_view = sliding_window_view

# scipy.optimize
any_minimize = minimize

# scipy.stats
any_kurtosis = kurtosis
any_skew = skew


def any_sr2lr(sr: Any) -> Any:
    return any_log(sr + 1)


def any_lr2sr(lr: Any) -> Any:
    return any_exp(lr) - 1
