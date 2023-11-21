from numpy import float64


def scalar_kelly_criterion(p: float64, a: float64, b: float64) -> float64:
    """
    Kelly Criterion with Bernoulli Distribution
    p is the probability that the investment increases in value.
    a is the fraction that is lost in a negative outcome.
    b is the fraction that is gained in a positive outcome.
    """
    assert 0 <= p <= 1 and a > 0 and b > 0
    q = 1 - p
    f = p / a - q / b
    return f
