import core.shapefile
import pandas as pd
from core.SpaceTimeFlowLISA import execSpaceTimeFLOWLISA

# Import panel flow data from .txt files
flowdf1 = pd.read_csv('input/US_state_migration_Opopweighted_2005_ReadytoUse.txt', sep=r'\s+')
F_dt1 = dict(zip(zip(flowdf1['O'], flowdf1['D']), flowdf1['Flow']))

flowdf2 = pd.read_csv('input/US_state_migration_Opopweighted_2006_ReadytoUse.txt', sep=r'\s+')
F_dt2 = dict(zip(zip(flowdf2['O'], flowdf2['D']), flowdf2['Flow']))

FlowAllYearDic = {}
for year in range(2005, 2019):
    flowdf = pd.read_csv('input/US_state_migration_Opopweighted_{}_ReadytoUse.txt'.format(year), sep=r'\s+')
    for _, row in flowdf.iterrows():
        FlowAllYearDic[(row['O'], row['D'], year)] = row['Flow']

# Import Origin and Destination shapefiles using core.shapefile
StationPolygon1 = core.shapefile.Reader('input/US_States.shp')
StationPolygon2 = core.shapefile.Reader('input/US_States.shp')

# Extract polygon shapes
shapes1 = StationPolygon1.shapes()
shapes2 = StationPolygon2.shapes()

# Prepare AREAS input for Queen's and Rook's contiguity
AREAS1 = [[shape.points] for shape in shapes1]
AREAS2 = [[shape.points] for shape in shapes2]

# Execute SpaceTimeFlowLISA function
outputStr = execSpaceTimeFLOWLISA(AREAS1, AREAS2, F_dt1, F_dt2, 2005, 2006, 1, 55, FlowAllYearDic)
"""
    Execute SpaceTimeFlowLISA to analyze spatiotemporal autocorrelation in panel flow data

    Parameters of execSpaceTimeFLOWLISA(AREAS1, AREAS2, FlowValue, FlowValue2, Time1, Time2, Spatstat, NeiLvl, Allyeardic):
    1. AREAS1: Origin areas (list of polygons)
    2. AREAS2: Destination areas (list of polygons)
    3. FlowValue: Dictionary of (O, D) flow values for the first year
    4. FlowValue2: Dictionary of (O, D) flow values for the second year
    5. Time1: First year
    6. Time2: Second year
    7. Spatstat:
        1 -> Local Moran's I
        2 -> Local Getis-Ord G
        3 -> Local Geary's C
    8. NeiLvl: Space-time neighborhood level
        33 -> contemporaneous
        494 -> lagged
        55 -> hybrid
    9. Allyeardic: Dictionary of all-year panel flow values

    Returns:
    - A formatted output string containing results
"""

# Save output to text file
output_filename = 'result/SpaceTimeFlowLISA_I_US_migration_Nei55_2005_2006.txt'
with open(output_filename, 'w') as outputFile:
    outputFile.write(outputStr)

print(f"Processing complete. Results saved to {output_filename}")
