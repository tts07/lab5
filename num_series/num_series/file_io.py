import re
from pathlib import Path
from typing import List, Union

PathLike = Union[str, Path]
_SEPARATORS = re.compile(r"[,;\s]+")


def load_series_txt(path: PathLike) -> List[float]:
    """Читает числа из txt — по одному на строку."""
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    result: List[float] = []
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for lineno, raw in enumerate(f, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    result.append(float(line))
                except ValueError as err:
                    raise ValueError(f"{file_path}:{lineno}: '{line}' не число") from err
    except OSError as err:
        raise ValueError(f"Не удалось прочитать {file_path}: {err!r}") from err

    if not result:
        raise ValueError(f"Файл {file_path} не содержит чисел")
    return result


def load_series_csv(path: PathLike) -> List[float]:
    """Читает числа из csv — через разделитель, возможно с заголовком."""
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    result: List[float] = []
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for lineno, raw in enumerate(f, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                tokens = [t for t in _SEPARATORS.split(line) if t]
                if not tokens:
                    continue
                try:
                    values = [float(t) for t in tokens]
                except ValueError:
                    if lineno == 1:
                        continue
                    raise ValueError(f"{file_path}:{lineno}: '{line}' содержит нечисловые значения")
                result.extend(values)
    except OSError as err:
        raise ValueError(f"Не удалось прочитать {file_path}: {err!r}") from err

    if not result:
        raise ValueError(f"Файл {file_path} не содержит чисел")
    return result