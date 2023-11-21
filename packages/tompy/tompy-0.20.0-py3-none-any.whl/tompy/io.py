from pathlib import Path

from pandas import DataFrame, read_csv


def csv_read(
    path: str, index_col: None | int = 0, parse_dates: bool = True
) -> None | DataFrame:
    p = Path(path)
    if not p.exists():
        return None
    return read_csv(p, index_col=index_col, parse_dates=parse_dates)


def csv_write(path: str, df: DataFrame) -> None:
    p = Path(path)
    df.to_csv(p)
