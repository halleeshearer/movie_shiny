import nilearn as nl
import hcp_utils as hcp
import nilearn.plotting as plotting
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# import data from all_rois_mv_results
data = pd.read_csv("all_rois_mv_results.csv")

# plot the i2c2_m column of data with nilearn plotting surface
#plotting.view_surf(hcp.mesh.inflated, hcp.cortex_data(hcp.unparcellate(data.i2c2_m, hcp.mmp)), cmap="viridis")
plotting.plot_surf_stat_map(hcp.mesh.inflated, hcp.cortex_data(hcp.unparcellate(data.i2c2_m, hcp.mmp)), cmap="viridis")
