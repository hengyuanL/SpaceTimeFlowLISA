# SpaceTimeFlowLISA
**SpaceTimeFlowLISA**, or the space-time flow local indicator of spatial association, measures spatiotemporal autocorrelation of panel flow data. The method was proposed by Tao, Chen, and Thill (2023) as an extension of **FlowLISA** and **BiFlowLISA** for dynamic origin-destination flows.

Run the codes of SpaceTimeFlowLISA:
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hengyuanL/SpaceTimeFlowLISA/blob/main/SpaceTimeFlowLISA_main.ipynb)

Spatial flows represent meaningful interactions between geographic regions, such as migration, commuting, trade, information exchange, and other origin-destination movements. While FlowLISA measures spatial autocorrelation in cross-sectional flow data, SpaceTimeFlowLISA introduces temporal dependence so that local flow clusters and outliers can be detected in panel flow data.

(PDF fig.1)

The core idea is to construct a space-time flow weight matrix. This matrix links one flow with other flows that are spatially neighboring, temporally neighboring, or both. Tao, Chen, and Thill (2023) define three space-time dependency structures: contemporaneous, lagged, and hybrid. The contemporaneous structure links flows within the same time period, the lagged structure links flows across adjacent time periods, and the hybrid structure combines spatial and temporal flow neighborhoods.

(PDF fig.2)

(PDF fig.3)

(PDF fig.4)

The result interpretation is similar to other LISA methods. There are four categories of significant local patterns, namely "HH" (high-high), "LL" (low-low), "HL" (high-low), and "LH" (low-high). The "HH" and "LL" local patterns indicate space-time flow clusters, where the focal flow and its neighboring flows have similar high or low values. The "HL" and "LH" local patterns indicate local outliers, where the focal flow differs from its surrounding space-time flow neighborhood.

For the synthetic experiment, Tao, Chen, and Thill (2023) used controlled flow data to evaluate whether SpaceTimeFlowLISA can identify designed spatiotemporal local autocorrelation patterns. The synthetic example shows how different weight matrices affect the detection of local clusters and outliers in panel flow settings.

(PDF fig.5)

For the empirical case study, the paper applies SpaceTimeFlowLISA to U.S. interstate migration flows from 2005 to 2017. The flows are standardized by origin population size and analyzed across time to reveal changing migration corridor patterns. Compared with spatial-only FlowLISA, SpaceTimeFlowLISA can detect patterns that are less spatially explicit but temporally dependent, including time-sensitive changes associated with events such as Hurricane Katrina.

(PDF fig.6)

(PDF fig.7)

The longer-period comparison highlights how the hybrid space-time flow weight matrix captures persistent and dynamic migration structures. The method identifies migration corridor havens, deserts, and outliers across years, showing that integrating spatial, temporal, and attributive associations in one local statistic can reveal distributional changes in flow phenomena.

(PDF fig.8)

(PDF fig.9)

To cite:

Tao, R., Chen, Y., & Thill, J. C. (2023). A space-time flow LISA approach for panel flow data. Computers, Environment and Urban Systems, 106, 102042.

Tao, R., & Thill, J. C. (2020). BiFlowLISA: Measuring spatial association for bivariate flow data. Computers, Environment and Urban Systems, 83, 101519.

Tao, R., & Thill, J. C. (2016). Spatial cluster detection in spatial flow data. Geographical Analysis, 48(4), 355-372.