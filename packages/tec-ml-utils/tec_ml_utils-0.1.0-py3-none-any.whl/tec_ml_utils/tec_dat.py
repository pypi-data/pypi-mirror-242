import os
import re
from datetime import date, datetime, timedelta
from os import walk
from os.path import join
from random import shuffle
from typing import TypedDict

import pandas as pd
import tqdm

NEEDED_PARAMETERS = (
    "hmax",
    "FiltWindow",
    "Time Range",
    "Minimum duration of series",
    "time step",
)

DATA_HEADERS = (
    "tsn",
    "time",
    "el",
    "az",
    "latp",
    "lonp",
    "tec",
    "tec_filtered",
    "validity",
)


def date_by_number(year: int = None, day_number: int = 1) -> datetime.datetime:
    """Вычисление даты в заданном году по номеру дня.
    Возвращает значение в формате datetime с 0ч 0мин 0сек."""

    if year is None or year < 1970 or day_number <= 0:
        raise ValueError("Enter correct year/day number.")

    return datetime.combine(
        date(year, 1, 1) + timedelta(days=day_number - 1), datetime.min.time()
    )


def day_number_by_date(
    year: int = 1970, month: int = 1, day: int = 1, dt_format=None
) -> int:
    """Вычисление номера дня в году по дате."""

    if dt_format is not None:
        return dt_format.timetuple().tm_yday
    return date(year, month, day).timetuple().tm_yday


def parse_filename(filename=""):
    """Парсинг имени файла stk2G20_165.dat на:
    stk2 - имя пункта гнсс (4 символа),
    G20 - тип и номер спутника (3 символа),
    165 - номер дня в году.
    Иногда имя файла может начинаться с "_"."""

    # TODO: добавить обработку ошибок
    name = os.path.basename(filename)
    try:
        name, _ = name.split(".")
    except ValueError:
        pass

    return {
        "day_number": int(
            name[8:11]
        ),  # TODO: убрать числа, заменить регулярным выражением
        "receiver_name": name[:4],  # TODO: уточнить англ. термин
        "sat_name": name[4:7],
    }


def dat_to_df(filename: str = "", year: int = 1970) -> pd.DataFrame:
    """Преобразование файла .dat в датафрейм.
    В датафрейме остаются столбцы: time, filtered_tec, tec.
    Дата преобразовывается в datetime pandas."""

    name, _ = os.path.basename(filename).split(".")
    file_name_parts = parse_filename(filename)

    dataframe = pd.read_csv(
        filepath_or_buffer=filename,
        delim_whitespace=True,
        comment="#",
        names=DATA_HEADERS,
    )
    # combine year and DOY and add to dataframe
    dt = date_by_number(year=year, day_number=file_name_parts["day_number"])
    dataframe["time"] = (
        pd.to_timedelta(dataframe["time"], unit="h").add(dt).astype("datetime64[s]")
    )

    return dataframe[["time", "tec_filtered", "tec"]].rename(
        columns={"time": "timestamp", "tec": "vtec"}
    )


def get_file_list(path: str = "", template: str = ".*") -> list[str]:
    """Сбор всех файлов из указанной директории с именами подходящих по шаблону."""

    file_list = []
    for dirpath, dirnames, filenames in walk(path):
        for filename in filenames:
            if re.match(template, filename) is not None:
                file_list.append(join(dirpath, filename))

    return file_list


def get_parts_dataset(df=None, fname="", size=30, step=30):
    """Деление датафрейма на равные части размера окна с шагом step."""

    roll = list(df.rolling(window=size))[size - 1 :: step]
    roll = [window for window in roll if len(window) == size]
    return [(f"{fname}.{i}", part) for i, part in enumerate(roll, 1)]


# def remove_df_part(df, part=None):
#     """Удаление из датасета подмножества - напр. сегмента."""
#     # TODO: упростить? или другой способ, сделать независимым от индексов!

#     df_new = df.merge(part, how="left", indicator=True)
#     df_new = df_new[df_new["_merge"] == "left_only"]
#     df_new.drop("_merge", axis=1, inplace=True)

#     return df_new


# def remove_df_segments(df, segments=[]):
#     """Убрать несколько сегментов. Переиндексация."""

#     if not segments:
#         df.reset_index(drop=True, inplace=True)
#         return df

#     return remove_df_segments(remove_df_part(df, segments[0]), segments[1:])


# def reset_index(df):
#     return df.reset_index(drop=True, inplace=True)


def _get_bounds_chunks(df=None, time_gap=60):
    """Вычисление точек - границ сегментов ряда
    между большими временными перерывами."""

    df["LONG_"] = (df["timestamp"].diff()).dt.seconds > time_gap
    df2 = df[df["LONG_"] == True]

    df.drop("LONG_", axis=1, inplace=True)
    df2.drop("LONG_", axis=1, inplace=True)

    bounds = []

    for r in df2.index:
        bounds.append(df["timestamp"].iloc[r - 1])
        bounds.append(df["timestamp"].iloc[r])

    bounds = [df["timestamp"].iloc[0], *bounds, df["timestamp"].iloc[-1]]

    return [bounds[i : i + 2] for i in range(0, len(bounds), 2)]


def split_df(df=None, time_gap=120):
    """Разделение датафрейма ряда на куски
    разделенные большим временным перерывом.
    Т.к. исходные данные содежат перерывы.
    Длительносить перерыва определяется параметром time_gap.
    Имеет смысл ставить time_gap больше 60.

    TODO: в исходных dat файлах есть информация - использовать ее?
    Хотя ее не всегда можно корректно использовать.
    """

    bounds = _get_bounds_chunks(df, time_gap=time_gap)
    parts = []

    for pair in bounds:
        left, right = pair
        start_row = df.loc[df["timestamp"] == left]
        end_row = df.loc[df["timestamp"] == right]
        parts.append(df[start_row.index[0] : end_row.index[0] + 1])

    return parts


def convert_to_rows_df(data=None, target=None, shuffle_df=False):
    """Конвертация датафреймов X и y для дальнейшего сохранения.
    Результат - датафрейм строк, последний элемент обозначает класс (target),
    остальные - значения временного ряда."""

    res = []

    for df, tg in zip(data, target):
        values = df["value"].values.tolist()
        values.append(tg)
        res.append(values)

    if shuffle_df:
        shuffle(res)

    return pd.DataFrame(res, dtype=float)


class TecDataFrame(TypedDict):
    name: str
    df: pd.DataFrame


def collect_dat(data_path: str = "", year: int = 2009) -> TecDataFrame:
    """Read all .dat files to one structure TectDataFrame with dataframes and names
    from given folder with respect to filename template."""

    file_list = get_file_list(path=data_path, template="^\w{4,4}[G,R]\d\d_\d\d\d\.dat$")

    tec_data = []

    for filename in tqdm.tqdm(file_list):
        name, _ = os.path.basename(filename).split(".")
        try:
            df = dat_to_df(filename=filename, year=year)
        except ValueError as e:
            print(f" Ошибка при обработке файла {name}. Файл пропущен.")
            print(e)
            continue

        tec_data.append(
            {
                "name": name,
                "df": df,
            }
        )

    return tec_data
