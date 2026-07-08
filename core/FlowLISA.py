import time as tm

import numpy as np

from core.getFlowNeighbors import getFlowNeighborsContiguity
from core.SpaceTimeFlowLISA import execSpaceTimeFLOWLISA
from core.spatstats import calculateGearyC, calculateGetisG, calculateMoranI, calculateMultiGearyC

__all__ = ["execFLOWLISA", "execSpaceTimeFLOWLISA"]


def execFLOWLISA(AREAS1, AREAS2, FlowValue, Spatstat, NeiLvl):
    start = tm.time()
    print("Running FlowLISA by Ran Tao, built on clusterpy by Duque et al.")

    y = FlowValue
    yOutput = {k: [v] if Spatstat != 5 else list(v) for k, v in y.items()}
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
    elif Spatstat == 2:
        output.append("O, D, V, GetisG, p-value")
    elif Spatstat == 3:
        output.append("O, D, V, GearyC, p-value")
    elif Spatstat == 5:
        output.append("O, D, V1, V2, MC, p-value")
    for key, value in yOutput.items():
        output.append("{}, {}".format(key, ", ".join(map(str, value))))
    return "\n".join(output)
