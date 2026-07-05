# SpaceTimeFlowLISA
**SpaceTimeFlowLISA** (Tao, Chen, and Thill, 2023) measures spatiotemporal local autocorrelation for panel flow data.

Run the codes of SpaceTimeFlowLISA:
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hengyuanL/SpaceTimeFlowLISA/blob/main/SpaceTimeFlowLISA_main.ipynb)

Spatial flow data represent origin-destination interactions between geographic regions, such as commuting, migration, and exchanges of commodities, capital, energy, or information. These flows are often highly dynamic, but many existing flow analytical methods are cross-sectional. Space-Time Flow LISA extends Spatial Flow LISA to panel flow data by measuring localized spatiotemporal autocorrelation in a one-step analysis.

The key component is a space-time weight matrix for flow data that blends pairwise spatial and temporal connectivities. The method includes three versions of the matrix: contemporaneous, lagged, and hybrid. These options allow the local statistic to capture patterns that are spatially explicit, temporally dependent, or both.

The case study in Tao, Chen, and Thill (2023) uses U.S. interstate migration flows from 2005 to 2017. The method can identify dynamic local patterns in migration systems, including time-sensitive changes such as the outmigration from Louisiana associated with Hurricane Katrina in 2005.

The result interpretation is similar to other LISA methods. Significant local patterns include "HH" (high-high), "LL" (low-low), "HL" (high-low), and "LH" (low-high). Compared with the spatial-only Flow LISA, Space-Time Flow LISA is less impeded by the distance between flow origin and destination because it also uses temporal dependence in panel flow data.

The repository follows the same layout style as BiFlowLISA:

```
core/    Space-Time Flow LISA and supporting algorithms
input/   sample U.S. interstate migration panel flow data and state shapefile
result/  output location for generated local statistics
```

Before running Space-Time Flow LISA, prepare the origin and destination shapefiles:

```python
AREAS1 = clusterpy.importArcData("input/US_States")
AREAS2 = clusterpy.importArcData("input/US_States")
```

Use `core/AllYearDictionary_sample.py` to build the all-year flow dictionary used by the space-time statistic.

The main execution call is:

```python
outputStr = execSpaceTimeFLOWLISA(
    AREAS1,
    AREAS2,
    FlowValue,
    FlowValue2,
    Time1,
    Time2,
    Spatstat,
    NeiLvl,
    Allyeardic,
)
```

Parameters:

```
AREAS1: origin areas
AREAS2: destination areas
FlowValue: OD pairs with non-zero values for the first year
FlowValue2: OD pairs with non-zero values for the second year
Time1: first year
Time2: second year
Spatstat: 1 = Moran's I; 2 = Getis G; 3 = Geary C; 5 = Multi-Geary C
NeiLvl: 33 = contemporaneous; 494 = lagged; 55 = hybrid
Allyeardic: dictionary of OD pairs with non-zero values across all years
```

After executing the code, export the results to the `result/` folder:

```python
outputFile = open("result/file_name.txt", "w")
outputFile.write(outputStr)
```

To cite:

Tao, R., Chen, Y., & Thill, J. C. (2023). A space-time flow LISA approach for panel flow data. Computers, Environment and Urban Systems, 106, 102042. https://doi.org/10.1016/j.compenvurbsys.2023.102042

```
@article{tao2023spacetimeflowlisa,
  author = {Tao, Ran and Chen, Yuzhou and Thill, Jean-Claude},
  title = {A space-time flow LISA approach for panel flow data},
  journal = {Computers, Environment and Urban Systems},
  volume = {106},
  pages = {102042},
  year = {2023},
  doi = {10.1016/j.compenvurbsys.2023.102042}
}
```
