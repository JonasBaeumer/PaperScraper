import pandas as pd
import numpy as np


def read_excl_file(filepath, sheetname):
    df = pd.read_excel(filepath, sheet_name=sheetname)
    for i in range(len(df)):
        row_entry = df.iloc[i]
        series_sorted = get_sorted_series(row_entry[1:], row_entry[0], len(row_entry))
        # Then we append all the string until the next on is the avg. rating
        series_sorted = series_sorted.astype(str)
        while not str(series_sorted[2])[0].isdigit():
            series_sorted[1] += series_sorted[2]
            series_sorted[2] = np.nan
            move_up_elements(series_sorted, 2)

        df.iloc[i] = series_sorted

    return df


def get_sorted_series(series, first_index, originallength):
    # Create a new series and go over it only add item to the next position if it is not empty
    ordered_array = []
    if pd.Series([first_index]).isnull().all():
        ordered_array.append(np.nan)
    else:
        ordered_array = [first_index]
    for element in series.to_numpy():
        if not pd.Series([element]).isnull().all():
            ordered_array.append(element)

    while len(ordered_array) != originallength:
        ordered_array.append(np.nan)

    series = pd.Series(ordered_array)
    return series


def move_up_elements(arr, start):
    arr[start:] = np.roll(arr[start:], -1)


def write_to_excel(filepath, sheetname, df):
    df.to_excel(filepath, sheet_name=sheetname, index=False)


if __name__ == '__main__':
    # print(pd.Series([np.nan]).isnull().all())
    sheets = ['Developer Tools', 'Functional libraries and util',  'User Interface', 'Integrations']
    filepath = '/Users/jonas/Desktop/Bachelor-Thesis/Papers/Storage Forge Categories Kopie.xlsx'
    for sheet in sheets:
        df = read_excl_file(filepath, sheet)
        write_to_excel(filepath, sheet, df)
    test = 'test'
