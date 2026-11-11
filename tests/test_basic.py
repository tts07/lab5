import pytest

# Исправленные пути: указываем питону, что модули лежат во вложенной папке
from num_series.num_series.stats import mean, median, spread, summarize
from num_series.num_series.moving_average import (
    simple_moving_average,
    exponential_moving_average,
)
from num_series.num_series.generator import random_series, sine_series, trend_series


def test_mean():
    assert mean([1, 2, 3]) == 2.0

def test_median_odd():
    assert median([3, 1, 2]) == 2.0

def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5

def test_spread():
    assert spread([1, 5, 3]) == 4.0

def test_summarize_keys():
    s = summarize([1, 2, 3, 4, 5])
    assert s["count"] == 5
    assert s["mean"] == 3.0
    assert s["median"] == 3.0
    assert s["spread"] == 4.0

def test_sma():
    assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]

def test_sma_window_too_big():
    with pytest.raises(ValueError):
        simple_moving_average([1, 2, 3], 5)

def test_ema():
    r = exponential_moving_average([1, 2, 3], 0.5)
    assert r[0] == 1
    assert r[1] == 1.5
    assert r[2] == 2.25

def test_random_series_length():
    assert len(random_series(10, seed=42)) == 10

def test_validate_negative():
    with pytest.raises(ValueError):
        random_series(-5, seed=42)

def test_sine_series_length():
    assert len(sine_series(15, seed=1)) == 15

def test_trend_series_length():
    assert len(trend_series(8, seed=1)) == 8