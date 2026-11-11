from typing import List, Sequence

def _check_window(window: int, n: int) -> None:
    if window < 1:
        raise ValueError("Окно должно быть >= 1")
    if window > n:
        raise ValueError("Окно не может быть больше длины ряда")

def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """SMA через бегущую сумму (эффективно, O(n))."""
    n = len(data)
    _check_window(window, n)
    
    running = sum(data[:window])
    result = [running / window]
    
    for i in range(window, n):
        running += data[i] - data[i - window]
        result.append(running / window)
        
    return result

def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированное MA (окно нечётное)."""
    if window % 2 == 0:
        raise ValueError("Для центрированного MA окно должно быть нечётным")
    return simple_moving_average(data, window)

def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """EMA = alpha * x[i] + (1 - alpha) * EMA[i-1]."""
    if not (0 < alpha <= 1):
        raise ValueError("alpha должна быть в диапазоне (0, 1]")
    if not data:
        return []
        
    ema = [data[0]]
    for i in range(1, len(data)):
        ema.append(alpha * data[i] + (1 - alpha) * ema[-1])
    return ema