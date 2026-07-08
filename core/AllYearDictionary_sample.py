"""Build the Allyeardic dictionary required by Space-Time FlowLISA.

This is the Python 3/core-format version of Code/AllYearDictionary_sample.py
from bobyellow/SpaceTimeFlowLISA.
"""

from pathlib import Path

import pandas as pd


def build_all_year_dictionary(input_dir, years=range(2005, 2019), filename_template="OPopweighted_{}_ReadytoUse.txt"):
    input_path = Path(input_dir)
    all_year_dict = {}
    for year in years:
        flow_df = pd.read_csv(input_path / filename_template.format(year), sep=r"\s+")
        year_dict = dict(zip(zip(flow_df["O"], flow_df["D"]), flow_df["Flow"]))
        all_year_dict.update({(origin, destination, year): flow for (origin, destination), flow in year_dict.items()})
    return all_year_dict


def export_all_year_dictionary(all_year_dict, output_csv):
    rows = [
        {"O": origin, "D": destination, "Year": year, "Flow": flow}
        for (origin, destination, year), flow in all_year_dict.items()
    ]
    pd.DataFrame(rows).to_csv(output_csv, index=False)


def read_all_year_dictionary(csv_path):
    df = pd.read_csv(csv_path)
    return {(row["O"], row["D"], row["Year"]): row["Flow"] for _, row in df.iterrows()}


__all__ = ["build_all_year_dictionary", "export_all_year_dictionary", "read_all_year_dictionary"]
