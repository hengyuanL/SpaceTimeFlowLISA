"""Build the panel-flow dictionary required by Space-Time FlowLISA."""

from pathlib import Path

import pandas as pd


def build_space_time_flow_dictionary(input_dir, years=range(2005, 2019), filename_template="OPopweighted_{}_ReadytoUse.txt"):
    input_path = Path(input_dir)
    all_year_dict = {}
    for year in years:
        flow_df = pd.read_csv(input_path / filename_template.format(year), sep=r"\s+")
        year_dict = dict(zip(zip(flow_df["O"], flow_df["D"]), flow_df["Flow"]))
        all_year_dict.update({(origin, destination, year): flow for (origin, destination), flow in year_dict.items()})
    return all_year_dict


def export_space_time_flow_dictionary(space_time_flow_dict, output_csv):
    rows = [
        {"O": origin, "D": destination, "Year": year, "Flow": flow}
        for (origin, destination, year), flow in space_time_flow_dict.items()
    ]
    pd.DataFrame(rows).to_csv(output_csv, index=False)


def read_space_time_flow_dictionary(csv_path):
    df = pd.read_csv(csv_path)
    return {(row["O"], row["D"], row["Year"]): row["Flow"] for _, row in df.iterrows()}


__all__ = [
    "build_space_time_flow_dictionary",
    "export_space_time_flow_dictionary",
    "read_space_time_flow_dictionary",
]
