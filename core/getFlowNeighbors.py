from core.getNeighbors import getNeighborsAreaContiguity


def _area_rook_neighbors(areas):
    if hasattr(areas, "Wrook"):
        return {k: list(v) for k, v in areas.Wrook.items()}
    _, wrook = getNeighborsAreaContiguity(areas)
    return {k: list(v) for k, v in wrook.items()}


def getFlowNeighborsContiguity(AREAS1, AREAS2, FlowValue, Level):
    grid1 = _area_rook_neighbors(AREAS1)
    grid2 = _area_rook_neighbors(AREAS2)
    flow_keys = set(FlowValue.keys())
    wflow1, wflow1o, wflow1d, wflow2, wflow12 = {}, {}, {}, {}, {}

    for key1Zero in range(len(grid1)):
        for key2Zero in range(len(grid2)):
            key1 = key1Zero + 1
            key2 = key2Zero + 1
            if (key1, key2) not in flow_keys:
                continue
            flowkey = (key1, key2)
            wflow1[flowkey], wflow1o[flowkey], wflow1d[flowkey], wflow2[flowkey], wflow12[flowkey] = [], [], [], [], []
            list1 = list(set(grid1.get(key1Zero, []) + [key1Zero]))
            list2 = list(set(grid2.get(key2Zero, []) + [key2Zero]))
            for origin in list1:
                for destination in list2:
                    candidate = (origin + 1, destination + 1)
                    if candidate == (key1, key2) or candidate not in flow_keys:
                        continue
                    wflow12[flowkey].append(candidate)
                    if origin + 1 != key1 and destination + 1 != key2:
                        wflow2[flowkey].append(candidate)
                    elif origin + 1 == key1:
                        wflow1d[flowkey].append(candidate)
                    elif destination + 1 == key2:
                        wflow1o[flowkey].append(candidate)
                    else:
                        wflow1[flowkey].append(candidate)

    if Level == 1:
        return wflow1
    if Level == 18:
        return wflow1o
    if Level == 19:
        return wflow1d
    if Level == 2:
        return wflow2
    if Level in (12, 120):
        if Level == 120:
            for key in wflow12:
                wflow12[key].append(key)
        return wflow12
    return {}


def STweightsFromFlows(AREAS1, AREAS2, FlowValue1, FlowValue2, Time1, Time2, Level):
    grid1 = _area_rook_neighbors(AREAS1)
    grid2 = _area_rook_neighbors(AREAS2)
    yKeys = set(FlowValue2.keys())
    yKeysMinusOne = set(FlowValue1.keys())

    wCont, wContO, wContD, wContOD, wCont2 = {}, {}, {}, {}, {}
    wLagged, wLaggedO, wLaggedD, wLaggedOD, wLagged2 = {}, {}, {}, {}, {}
    wHybrid = {}

    for key1Zero in range(len(grid1)):
        for key2Zero in range(len(grid2)):
            key1 = key1Zero + 1
            key2 = key2Zero + 1
            if (key1, key2) not in yKeys:
                continue
            flowkey = (key1, key2, Time2)
            for target in (wCont, wContO, wContD, wContOD, wCont2, wLagged, wLaggedO, wLaggedD, wLaggedOD, wLagged2, wHybrid):
                target[flowkey] = []

            list1 = list(set(grid1.get(key1Zero, []) + [key1Zero]))
            list2 = list(set(grid2.get(key2Zero, []) + [key2Zero]))

            for origin in list1:
                for destination in list2:
                    od = (origin + 1, destination + 1)
                    if od != (key1, key2) and od in yKeys:
                        candidate = (od[0], od[1], Time2)
                        wCont[flowkey].append(candidate)
                        if od[0] != key1 and od[1] != key2:
                            wCont2[flowkey].append(candidate)
                        elif od[0] == key1:
                            wContO[flowkey].append(candidate)
                            wContOD[flowkey].append(candidate)
                            wHybrid[flowkey].append(candidate)
                        elif od[1] == key2:
                            wContD[flowkey].append(candidate)
                            wContOD[flowkey].append(candidate)
                            wHybrid[flowkey].append(candidate)

                    if od != (key1, key2) and od in yKeysMinusOne:
                        candidate = (od[0], od[1], Time1)
                        wLagged[flowkey].append(candidate)
                        if od[0] != key1 and od[1] != key2:
                            wLagged2[flowkey].append(candidate)
                        elif od[0] == key1:
                            wLaggedO[flowkey].append(candidate)
                            wLaggedOD[flowkey].append(candidate)
                            wHybrid[flowkey].append(candidate)
                        elif od[1] == key2:
                            wLaggedD[flowkey].append(candidate)
                            wLaggedOD[flowkey].append(candidate)
                            wHybrid[flowkey].append(candidate)
                    elif od == (key1, key2) and od in yKeysMinusOne:
                        same_flow = (key1, key2, Time1)
                        wCont[flowkey].append(same_flow)
                        wContO[flowkey].append(same_flow)
                        wContD[flowkey].append(same_flow)
                        wContOD[flowkey].append(same_flow)
                        wLaggedOD[flowkey].append(same_flow)
                        wHybrid[flowkey].append(same_flow)
                        wCont2[flowkey].append(same_flow)

    if Level == 3:
        return wCont
    if Level == 31:
        return wContO
    if Level == 32:
        return wContD
    if Level == 33:
        return wContOD
    if Level == 312:
        return wCont2
    if Level == 49:
        return wLagged
    if Level == 491:
        return wLaggedO
    if Level == 492:
        return wLaggedD
    if Level == 494:
        return wLaggedOD
    if Level == 413:
        return wLagged2
    if Level == 55:
        return wHybrid
    return {}