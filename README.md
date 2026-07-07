# SpaceTimeFlowLISA
**SpaceTimeFlowLISA**, or the space-time flow local indicator of spatial association, measures spatiotemporal autocorrelation of panel flow data. The method was proposed by Tao, Chen, and Thill (2023) as an extension of **FlowLISA** and **BiFlowLISA** for dynamic origin-destination flows.

Run the codes of SpaceTimeFlowLISA:
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hengyuanL/SpaceTimeFlowLISA/blob/main/SpaceTimeFlowLISA_main.ipynb)

The core idea is to construct a space-time flow weight matrix. This matrix links one flow with other flows that are spatially neighboring, temporally neighboring, or both. Tao, Chen, and Thill (2023) define three space-time dependency structures: contemporaneous, lagged, and hybrid. The contemporaneous structure links flows within the same time period, the lagged structure links flows across adjacent time periods, and the hybrid structure combines spatial and temporal flow neighborhoods.

<img width="1715" height="1046" alt="image" src="https://github.com/user-attachments/assets/6877809b-4f08-41cf-8966-00bc74b9830a" />
<img width="959" height="1118" alt="image" src="https://github.com/user-attachments/assets/aeb95ab2-8a25-4212-98ee-8139be3090c5" />

In Eq. (4), $FI_{ST(i,j,t)}$ is the STFlowLISA value of the flow between origin $i$ and destination $j$ at time $t$. $f_{(i,j,t)}$ represents the value (or volume) of the flow between regions $i$ and $j$ at time $t$. It incorporates the same cross-product formulation as the local Moran’s $I$ statistic. $N$ is the total number of flows in the study area throughout the entire study period. $\bar{f}$ is the average value of all $N$ flows. $w_{ij,uv}$ is the spatial flow weight between $f_{(i,j)}$ and $f_{(u,v)}$. In a simple binary configuration, $w_{ijt,uvt'}$ equals 1 if $f_{(u,v,t')}$ is connected with $f_{(i,j,t)}$ according to the definition of $W_{STF}$. Otherwise, it equals 0. In addition, the spatial-temporal weights are row-standardized, so that the total weight of each flow sums to 1, regardless of how many connections it has.

<img width="952" height="153" alt="image" src="https://github.com/user-attachments/assets/95aee487-a23c-4e97-85cb-82e0591a7d8c" />

The result interpretation is similar to other LISA methods. There are four categories of significant local patterns, namely "HH" (high-high), "LL" (low-low), "HL" (high-low), and "LH" (low-high). The "HH" and "LL" local patterns indicate space-time flow clusters, where the focal flow and its neighboring flows have similar high or low values. The "HL" and "LH" local patterns indicate local outliers, where the focal flow differs from its surrounding space-time flow neighborhood.

For the synthetic experiment, Tao, Chen, and Thill (2023) used controlled flow data to evaluate whether SpaceTimeFlowLISA can identify designed spatiotemporal local autocorrelation patterns. The synthetic example shows how different weight matrices affect the detection of local clusters and outliers in panel flow settings.

<img width="1343" height="1172" alt="image" src="https://github.com/user-attachments/assets/4809afce-84d4-4080-b823-9f1c67a3cf17" />

<img width="1935" height="493" alt="image" src="https://github.com/user-attachments/assets/edf3a54d-18c6-49a7-8e23-a4bd0fead631" />

For the empirical case study, the paper applies SpaceTimeFlowLISA to U.S. interstate migration flows from 2005 to 2017. The flows are standardized by origin population size and analyzed across time to reveal changing migration corridor patterns. Compared with spatial-only FlowLISA, SpaceTimeFlowLISA can detect patterns that are less spatially explicit but temporally dependent, including time-sensitive changes associated with events such as Hurricane Katrina.

<img width="1645" height="1413" alt="image" src="https://github.com/user-attachments/assets/5e5ce7e6-ddf5-4c4b-9538-f6295c47de09" />

The longer-period comparison highlights how the hybrid space-time flow weight matrix captures persistent and dynamic migration structures. The method identifies migration corridor havens, deserts, and outliers across years, showing that integrating spatial, temporal, and attributive associations in one local statistic can reveal distributional changes in flow phenomena.

<img width="1739" height="1555" alt="image" src="https://github.com/user-attachments/assets/afbfb162-f7ea-4bb0-8859-4ac2aa5238d1" />


To cite:

Tao, R., Chen, Y., & Thill, J. C. (2023). A space-time flow LISA approach for panel flow data. Computers, Environment and Urban Systems, 106, 102042.

Tao, R., & Thill, J. C. (2020). BiFlowLISA: Measuring spatial association for bivariate flow data. Computers, Environment and Urban Systems, 83, 101519.

Tao, R., & Thill, J. C. (2016). Spatial cluster detection in spatial flow data. Geographical Analysis, 48(4), 355-372.
