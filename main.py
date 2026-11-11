import argparse
import sys
import os

# Принудительно добавляем путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Прямые импорты (в обход сломанного __init__.py)
from num_series.num_series.generator import random_series, sine_series, trend_series
from num_series.num_series.stats import summarize
from num_series.num_series.moving_average import (
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
)
from num_series.num_series.io_json import save_series_json, load_series_json
from num_series.num_series.file_io import load_series_txt, load_series_csv


def build_series(kind, n, seed):
    if kind == "random":
        return random_series(n, low=-50, high=50, seed=seed)
    if kind == "sine":
        return sine_series(n, amplitude=10, frequency=2, noise=1.5, seed=seed)
    if kind == "trend":
        return trend_series(n, start=0.0, step=1.0, noise=0.5, seed=seed)
    raise ValueError(f"Неизвестный тип: {kind}")

def print_series(title, values):
    print(f"\n{title} (n={len(values)}):")
    for i in range(0, len(values), 5):
        print("  " + " ".join(f"{v:>8.3f}" for v in values[i:i+5]))

def main():
    parser = argparse.ArgumentParser(description="Обработка числовых рядов")
    parser.add_argument("--kind", choices=["random", "sine", "trend"], default="sine")
    parser.add_argument("-n", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--window", type=int, default=3)
    parser.add_argument("--alpha", type=float, default=0.3)
    parser.add_argument("--save", metavar="PATH", help="Сохранить в JSON")
    parser.add_argument("--load", metavar="PATH", help="Загрузить из файла")
    
    args = parser.parse_args()

    # Получение данных
    try:
        if args.load:
            if args.load.endswith(".json"):
                data = load_series_json(args.load)
            elif args.load.endswith(".txt"):
                data = load_series_txt(args.load)
            else:
                data = load_series_csv(args.load)
            source = f"Файл: {args.load}"
        else:
            data = build_series(args.kind, args.n, args.seed)
            source = f"Генерация ({args.kind}, n={args.n}, seed={args.seed})"
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

    # Сохранение (если просили)
    if args.save:
        try:
            save_series_json(data, args.save, meta={"source": source})
            print(f"Сохранено в {args.save} ({len(data)} точек)")
        except ValueError as e:
            print(f"Ошибка сохранения: {e}", file=sys.stderr)
            return 1

    # Анализ
    try:
        stats = summarize(data)
        sma = simple_moving_average(data, args.window)
        ema = exponential_moving_average(data, args.alpha)
        cma = centered_moving_average(data, args.window) if args.window % 2 != 0 else None
    except ValueError as e:
        print(f"Ошибка анализа: {e}", file=sys.stderr)
        return 1

    # Вывод
    print("=" * 60)
    print(f"Источник: {source}")
    print("-" * 60)
    print(f"Среднее : {stats['mean']:>10.4f}")
    print(f"Медиана : {stats['median']:>10.4f}")
    print(f"Размах  : {stats['spread']:>10.4f}")
    
    print_series("Исходный ряд", data)
    print_series(f"SMA (окно={args.window})", sma)
    print_series(f"EMA (alpha={args.alpha})", ema)
    if cma:
        print_series(f"Центр. MA (окно={args.window})", cma)
    print("=" * 60)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())