import time as tm

import numpy as np

from core.getFlowNeighbors import STweightsFromFlows, getFlowNeighborsContiguity
from core.spatstats import calculateGearyC, calculateGetisG, calculateMoranI, calculateMultiGearyC

__all__ = ["execFLOWLISA", "execSpaceTimeFLOWLISA"]


def execFLOWLISA(AREAS1, AREAS2, FlowValue, Spatstat, NeiLvl):
    start = tm.time()
    print("Running FlowLISA by Ran Tao, built on clusterpy by Duque et al.")

    y = FlowValue
    yOutput = {k: [v] if Spatstat != 5 else v for k, v in y.items()}
    yKeys = list(y.keys())
    Wflow = getFlowNeighborsContiguity(AREAS1, AREAS2, y, NeiLvl)

    dataMean = np.mean(list(y.values()))
    dataStd = np.std(list(y.values()))
    GMoranI = 0

    for s in yKeys:
        neighbors = Wflow.get(s, [])
        if Spatstat == 1:
            MoranI = calculateMoranI(s, neighbors, dataMean, dataStd, y, len(yKeys)) if neighbors else 0
            yOutput[s].extend([MoranI, 0])
            GMoranI += MoranI
        if Spatstat == 2:
            GetisG = calculateGetisG(neighbors, dataMean, dataStd, y, len(yKeys)) if neighbors else 0
            yOutput[s].extend([GetisG, 0])
        if Spatstat == 3:
            GearyC = calculateGearyC(s, neighbors, y) if neighbors else 0
            yOutput[s].extend([GearyC, 0])
        elif Spatstat == 5:
            MC = 999 if not neighbors else calculateMultiGearyC(s, neighbors, y, y, 2)
            yOutput[s].extend([MC, 0])

    output = ["Global Moran's I value is: {}".format(GMoranI)]
    if Spatstat == 1:
        output.append("O, D, V, MoranI, p-value, I_Result")
    elif Spatstat == 5:
        output.append("O, D, V1, V2, MC, p-value")
    for key, value in yOutput.items():
        output.append("{}, {}".format(key, ", ".join(map(str, value))))
    return "\n".join(output)


def execSpaceTimeFLOWLISA(AREAS1, AREAS2, FlowValue, FlowValue2, Time1, Time2, Spatstat, NeiLvl, Allyeardic):
    start = tm.time()
    print("Running Space-Time FlowLISA by Ran Tao, Yuzhou Chen, and Jean-Claude Thill.")

    dic_flow1 = {}
    for key, value in FlowValue.items():
        dic_flow1[(key[0], key[1], Time1)] = value
    dic_flow2 = {}
    for key, value in FlowValue2.items():
        dic_flow2[(key[0], key[1], Time2)] = value
    dic_flow4 = dic_flow1.copy()
    dic_flow4.update(dic_flow2)

    y = FlowValue2
    yOutput = {k: [v] for k, v in y.items()} if Spatstat != 5 else y
    yKeys = list(y.keys())
    Wflow = STweightsFromFlows(AREAS1, AREAS2, FlowValue, FlowValue2, Time1, Time2, NeiLvl)

    all_values = list(Allyeardic.values())
    dataLength = len(y)
    dataMean = np.mean(all_values)
    dataStd = np.std(all_values)
    GMoranI = 0

    for s in yKeys:
        st_key = (s[0], s[1], Time2)
        neighbors = Wflow.get(st_key, [])
        if Spatstat == 1:
            MoranI = calculateMoranI(st_key, neighbors, dataMean, dataStd, dic_flow4, dataLength) if neighbors else 0
            yOutput[s].extend([MoranI, 0])
            GMoranI += MoranI
        if Spatstat == 2:
            GetisG = calculateGetisG(neighbors, dataMean, dataStd, dic_flow4, dataLength) if neighbors else 0
            yOutput[s].extend([GetisG, 0])
        if Spatstat == 3:
            GearyC = calculateGearyC(st_key, neighbors, dic_flow4) if neighbors else 0
            yOutput[s].extend([GearyC, 0])
        if Spatstat == 5:
            MC = calculateMultiGearyC(s, neighbors, y, y, 2) if neighbors else 999
            yOutput[s].extend([MC, 0])

    output = ["Global Moran's I value is: {}".format(GMoranI)]
    if Spatstat == 1:
        output.append("O, D, Time, V, MoranI, p-value, I_Result")
    elif Spatstat == 5:
        output.append("O, D, Time, V1, V2, MC, p-value")
    for key, value in yOutput.items():
        output.append("({}, {}, {}), {}".format(key[0], key[1], Time2, ", ".join(map(str, value))))
    return "\n".join(output)