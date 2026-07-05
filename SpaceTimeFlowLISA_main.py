import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core"))

from SpaceTimeFlowLISA import execSpaceTimeFLOWLISA


# Import panel flow data from input files.
# The input flow data should not contain zero-value OD pairs.
flowdf1 = pd.read_csv("input/OPopweighted_2005_ReadytoUse.txt", sep=r"\s+")
flowdf2 = pd.read_csv("input/OPopweighted_2006_ReadytoUse.txt", sep=r"\s+")

F_dt1 = dict(zip(zip(flowdf1["O"], flowdf1["D"]), flowdf1["Flow"]))
F_dt2 = dict(zip(zip(flowdf2["O"], flowdf2["D"]), flowdf2["Flow"]))


# Build or load the all-year dictionary before running Space-Time Flow LISA.
# See core/AllYearDictionary_sample.py for an example workflow.
allyear_df = pd.read_csv("input/Allyeardict.csv")
Allyeardict = dict(
    ((row["O"], row["D"], row["Year"]), row["Flow"])
    for _, row in allyear_df.iterrows()
)


# Import origin and destination areas before execution.
# The original implementation was built around clusterpy area objects:
#
# AREAS1 = clusterpy.importArcData("input/US_States")
# AREAS2 = clusterpy.importArcData("input/US_States")
AREAS1 = None
AREAS2 = None


# Execute Space-Time Flow LISA after AREAS1 and AREAS2 are prepared.
# Spatstat: 1 = Moran's I; 2 = Getis G; 3 = Geary C; 5 = Multi-Geary C
# NeiLvl: 33 = contemporaneous; 494 = lagged; 55 = hybrid
if AREAS1 is not None and AREAS2 is not None:
    outputStr = execSpaceTimeFLOWLISA(
        AREAS1,
        AREAS2,
        F_dt1,
        F_dt2,
        2005,
        2006,
        1,
        55,
        Allyeardict,
    )

    output_filename = "result/SpaceTimeFlowLISA_I_US_migration_2005_2006_Nei55.txt"
    with open(output_filename, "w") as outputFile:
        outputFile.write(outputStr)

    print("Processing complete. Results saved to {}".format(output_filename))
else:
    print("Prepare AREAS1 and AREAS2 from input/US_States before running Space-Time Flow LISA.")
