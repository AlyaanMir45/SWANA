import pandas as pd


def remove_duplicates(dataframe: pd.DataFrame) -> pd.DataFrame:
    cleaned_dataframe = dataframe.drop_duplicates()

    return cleaned_dataframe

# THIS FILE IS NOT DONE I NEED TO WORK ON IT LATER