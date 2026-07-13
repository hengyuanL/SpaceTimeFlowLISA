import numpy as np


def _value(data, key):
    value = data[key]
    if isinstance(value, (list, tuple, np.ndarray)):
        return float(value[0])
    return float(value)


def calculateGetisG(keyList, dataMean, dataStd, dataDictionary, dataLength):
    neighborNumber = len(keyList)
    if neighborNumber == 0 or dataStd == 0:
        return 0
    total = sum(_value(dataDictionary, i) for i in keyList)
    numerator = total - (dataMean * neighborNumber)
    denominator = dataStd * ((float(dataLength * neighborNumber - (neighborNumber ** 2)) / (dataLength - 1)) ** 0.5)
    return np.double(numerator) / np.double(denominator)


def calculateMoranI(ikey, keyList, dataMean, dataStd, dataDictionary, dataLength):
    neighborNumber = len(keyList)
    if neighborNumber == 0 or dataStd == 0:
        return 0
    total = sum(np.double(_value(dataDictionary, j) - dataMean) for j in keyList)
    numerator = dataLength * (_value(dataDictionary, ikey) - dataMean) * total
    denominator = (dataStd ** 2) * neighborNumber
    return np.double(numerator) / np.double(denominator)


def calculateGearyC(ikey, keyList, dataDictionary):
    return sum(np.double((_value(dataDictionary, ikey) - _value(dataDictionary, j)) ** 2) for j in keyList)


def calculateMultiGearyC(ikey, keyList, dataDictionary, dataDictionaryPer, numVar):
    total = 0
    values = list(dataDictionaryPer.values())
    for i in range(numVar):
        column = np.array([float(item[i]) for item in values], dtype=float)
        dataMean = np.mean(column)
        dataStd = np.std(column)
        if len(keyList) == 0 or dataStd == 0:
            continue
        subtotal = 0
        for j in keyList:
            std_i_value = (dataDictionary[ikey][i] - dataMean) / dataStd
            std_j_value = (dataDictionaryPer[j][i] - dataMean) / dataStd
            subtotal += np.double((std_i_value - std_j_value) ** 2)
        total += subtotal
    return total / numVar
