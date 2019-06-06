import pandas as pd
import csv


data = pd.read_csv('rad_seance.csv', sep=";", quotechar="\"",
                   names=["treatment", "date", "time", "comment"],
                   dtype=str, header=0)

data["id_date"] = data.treatment.str.cat(data.date)

not_uniques = set(data.groupby("id_date").filter(lambda x: len(x) > 1).id_date)

data_duplicated_only = data.loc[data.id_date.apply(lambda s: s in not_uniques),
                                data.columns[0:4]]

data_duplicated_only.to_csv("ok_cols_start_py.csv", sep=",",
                            quoting=csv.QUOTE_ALL, index=False)
