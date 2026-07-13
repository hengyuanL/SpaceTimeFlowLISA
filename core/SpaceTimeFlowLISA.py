"""Space-Time FlowLISA implementation.

This module is the Python 3/core-format migration of the original
Space-Time FlowLISA implementation from bobyellow/SpaceTimeFlowLISA.
It preserves the Space-Time FlowLISA workflow, including Monte Carlo
p-value and significance output.
"""

import numpy as np

from core.SpaceTimeWeights import STweightsFromFlows
from core.SpaceTimeStatistics import calculateGearyC, calculateGetisG, calculateMoranI, calculateMultiGearyC

__all__ = ["execSpaceTimeFLOWLISA"]


def _numeric_value(value):
    if isinstance(value, (list, tuple, np.ndarray)):
        return float(value[0])
    return float(value)


def _numeric_values(data):
    return [_numeric_value(value) for value in data.values()]


def _as_sequence(value):
    if isinstance(value, (list, tuple, np.ndarray)):
        return list(value)
    return [value]


def _format_number(value):
    if isinstance(value, (float, np.floating)):
        return "{:.6g}".format(float(value))
    return str(value)


def _classify_local(value, statistic, p_value, data_mean, alpha):
    if p_value > alpha or statistic == 0:
        return "NS"
    if statistic > 0:
        return "HH" if value > data_mean else "LL"
    return "HL" if value > data_mean else "LH"


def _build_space_time_values(flow_value1, flow_value2, time1, time2):
    previous = {(origin, destination, time1): value for (origin, destination), value in flow_value1.items()}
    current = {(origin, destination, time2): value for (origin, destination), value in flow_value2.items()}
    combined = previous.copy()
    combined.update(current)
    return combined


def _randomized_space_time_values(keys, source_values, rng):
    if not keys:
        return {}
    if len(source_values) >= len(keys):
        values = rng.permutation(source_values)[: len(keys)]
    else:
        values = rng.choice(source_values, size=len(keys), replace=True)
    return dict(zip(keys, values))


def _global_p_value(observed, simulations):
    if not simulations:
        return 1.0
    more_extreme = sum(abs(value) >= abs(observed) for value in simulations)
    return (more_extreme + 1.0) / (len(simulations) + 1.0)


def _global_moran_summary(global_moran, simulations, alpha):
    if not simulations:
        return "Global Moran's I value is: {}".format(global_moran)
    lower = float(np.quantile(simulations, alpha / 2.0))
    upper = float(np.quantile(simulations, 1.0 - alpha / 2.0))
    p_value = _global_p_value(global_moran, simulations)
    if global_moran >= upper:
        state = "significantly positive"
    elif global_moran <= lower:
        state = "significantly negative"
    else:
        state = "insignificant"
    return "Global Moran's I value is: {}. It is {} at {} level (p-value: {:.6g})".format(
        global_moran, state, alpha, p_value
    )


def execSpaceTimeFLOWLISA(
    AREAS1,
    AREAS2,
    FlowValue,
    FlowValue2,
    Time1,
    Time2,
    Spatstat,
    NeiLvl,
    Allyeardic,
    permutations=100,
    alpha=0.05,
    random_state=None,
):
    """Execute Space-Time FlowLISA for two consecutive panel-flow periods.

    Parameters follow the original STFA script. ``permutations`` controls the
    Monte Carlo randomization count used for local p-values and the global
    Moran's I significance statement. The default follows the original STFA
    script's 100 Monte Carlo simulations while keeping examples practical to run.
    """
    print("Running Space-Time FlowLISA by Ran Tao, Yuzhou Chen, and Jean-Claude Thill.")

    st_values = _build_space_time_values(FlowValue, FlowValue2, Time1, Time2)
    Wflow = STweightsFromFlows(AREAS1, AREAS2, FlowValue, FlowValue2, Time1, Time2, NeiLvl)

    source_values = _numeric_values(Allyeardic) if Allyeardic else _numeric_values(st_values)
    data_length = len(FlowValue2)
    data_mean = float(np.mean(source_values)) if source_values else 0.0
    data_std = float(np.std(source_values)) if source_values else 0.0

    y_output = {}
    global_moran = 0.0
    observed_stats = {}

    for od_key, raw_value in FlowValue2.items():
        st_key = (od_key[0], od_key[1], Time2)
        neighbors = Wflow.get(st_key, [])
        row = _as_sequence(raw_value)
        if Spatstat == 1:
            statistic = calculateMoranI(st_key, neighbors, data_mean, data_std, st_values, data_length) if neighbors else 0
            global_moran += statistic
            row.extend([statistic, 1.0])
            observed_stats[st_key] = statistic
        elif Spatstat == 2:
            statistic = calculateGetisG(neighbors, data_mean, data_std, st_values, data_length) if neighbors else 0
            row.extend([statistic, 1.0])
            observed_stats[st_key] = statistic
        elif Spatstat == 3:
            statistic = calculateGearyC(st_key, neighbors, st_values) if neighbors else 0
            row.extend([statistic, 1.0])
            observed_stats[st_key] = statistic
        elif Spatstat == 5:
            statistic = calculateMultiGearyC(st_key, neighbors, st_values, st_values, 2) if neighbors else 999
            row.extend([statistic, 1.0])
            observed_stats[st_key] = statistic
        else:
            raise ValueError("Unsupported Spatstat: {}".format(Spatstat))
        y_output[od_key] = row

    simulations = []
    if permutations and permutations > 0 and source_values and observed_stats:
        rng = np.random.default_rng(random_state)
        st_keys = list(st_values.keys())
        for _ in range(permutations):
            random_values = _randomized_space_time_values(st_keys, source_values, rng)
            simulated_global = 0.0
            for od_key in FlowValue2.keys():
                st_key = (od_key[0], od_key[1], Time2)
                neighbors = Wflow.get(st_key, [])
                if Spatstat == 1:
                    simulated = calculateMoranI(st_key, neighbors, data_mean, data_std, random_values, data_length) if neighbors else 0
                    simulated_global += simulated
                    if abs(simulated) >= abs(observed_stats[st_key]):
                        y_output[od_key][-1] += 1
                elif Spatstat == 2:
                    simulated = calculateGetisG(neighbors, data_mean, data_std, random_values, data_length) if neighbors else 0
                    if abs(simulated) >= abs(observed_stats[st_key]):
                        y_output[od_key][-1] += 1
                elif Spatstat == 3:
                    simulated = calculateGearyC(st_key, neighbors, random_values) if neighbors else 0
                    if simulated >= observed_stats[st_key]:
                        y_output[od_key][-1] += 1
                elif Spatstat == 5:
                    simulated = calculateMultiGearyC(st_key, neighbors, st_values, random_values, 2) if neighbors else 999
                    if simulated >= observed_stats[st_key]:
                        y_output[od_key][-1] += 1
            if Spatstat == 1:
                simulations.append(simulated_global)

        denominator = float(permutations + 1)
        for row in y_output.values():
            row[-1] = row[-1] / denominator

    output = [_global_moran_summary(global_moran, simulations, alpha) if Spatstat == 1 else "Global Moran's I value is: {}".format(global_moran)]
    if Spatstat == 1:
        output.append("O, D, Time, V, MoranI, p-value, I_Result")
    elif Spatstat == 2:
        output.append("O, D, Time, V, GetisG, p-value, G_Result")
    elif Spatstat == 3:
        output.append("O, D, Time, V, GearyC, p-value, C_Result")
    elif Spatstat == 5:
        output.append("O, D, Time, V1, V2, MC, p-value")

    for od_key, row in y_output.items():
        values = ", ".join(_format_number(value) for value in row)
        if Spatstat in (1, 2, 3):
            label = _classify_local(_numeric_value(row[0]), row[-2], row[-1], data_mean, alpha)
            output.append("({}, {}, {}), {}, {}".format(od_key[0], od_key[1], Time2, values, label))
        else:
            output.append("({}, {}, {}), {}".format(od_key[0], od_key[1], Time2, values))
    return "\n".join(output)
