import seaborn as sns
from faicons import icon_svg
import hcp_utils as hcp
import nilearn as nl
from nilearn import plotting as plot
import shinywidgets
from shinywidgets import output_widget, render_widget

# Import data from shared.py
from shared import app_dir, df

from shiny import App, reactive, render, ui

import hcp_utils as hcp
import nilearn.plotting as plotting
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from shinywidgets import render_plotly

# import data from all_rois_mv_results
data = pd.read_csv("all_rois_mv_results.csv")

glasser = hcp.mmp.labels
# delete the first key in the dictionary
del glasser[0]
glasser_int_keys = {int(key): value for key, value in glasser.items()}
options = {"All": "All Regions"}
options.update(glasser_int_keys)



app_ui = ui.page_sidebar(
    ui.sidebar(
        # ui.input_select(
        #     "measure",
        #     "Reliability measure",
        #     {"discr": "Discriminability", "i2c2" : "I2C2", "finger" : "Fingerprinting"},
        #     selected=["i2c2"],
        # ),
        ui.input_select(
            "plot",
            "Plot",
            {"m" : "Movie", "r" : "Rest", "diff" : "Movie-Rest Difference"},
            selected = ["diff"],
        ),
        ui.input_select(
            "roi",
            "Region of interest (Glasser parcel)",
            # use hcp.mmp.labels as the dictionary of the regions
            options,
        ),
        ui.input_slider("plot_max", "Max value", min=0, max=1, value=0.5, step=0.05)
    ),

    ui.layout_column_wrap(
        ui.card(
            ui.card_header("I2C2"),
            ui.output_ui("i2c2"),
            ui.input_slider("i2c2_max", "Max value", min=0, max=1, value=0.3, step=0.05),
            full_screen = True),
        ui.card(
            ui.card_header("Discriminability"),
            ui.output_ui("discr"),
            ui.input_slider("discr_max", "Max value", min=0, max=1, value=0.3, step=0.05),
            full_screen = True,
        ),
        ui.card(
            ui.card_header("Fingerprinting"),
            ui.output_ui("finger"),
            ui.input_slider("finger_max", "Max value", min=0, max=1, value=0.3, step=0.05),
            full_screen = True,
        ),
    ),
    ui.include_css(app_dir / "styles.css"),
    title="Movie Stuff",
    fillable=True,
)


def server(input, output, session):

    @reactive.calc
    def filtered_df_i2c2():
        if input.roi() == "All":
            filt_df = data[f"i2c2_{input.plot()}"]
        # if roi is selected, then set all other values to 0
        if input.roi() != "All":
            # set all values to 0 except for the value at the index of the selected roi number
            filt_df = np.zeros(len(data))
            filt_df[int(input.roi())-1] = data[f"i2c2_{input.plot()}"][int(input.roi())-1]
        return filt_df
    
    @reactive.calc
    def filtered_df_discr():
        if input.roi() == "All":
            filt_df = data[f"discr_{input.plot()}"]
        # if roi is selected, then set all other values to 0
        if input.roi() != "All":
            # set all values to 0 except for the value at the index of the selected roi number
            filt_df = np.zeros(len(data))
            filt_df[int(input.roi())-1] = data[f"discr_{input.plot()}"][int(input.roi())-1]
        return filt_df
    
    @reactive.calc
    def filtered_df_finger():
        if input.roi() == "All":
            filt_df = data[f"finger_{input.plot()}"]
        # if roi is selected, then set all other values to 0
        if input.roi() != "All":
            # set all values to 0 except for the value at the index of the selected roi number
            filt_df = np.zeros(len(data))
            filt_df[int(input.roi())-1] = data[f"finger_{input.plot()}"][int(input.roi())-1]
        return filt_df



    # @render.text
    # def bill_length():
    #     return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # @render.text
    # def bill_depth():
    #     return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


    # @render.ui
    # def mv_rel():
    #     surf_plot = plotting.view_surf(hcp.mesh.inflated, hcp.cortex_data(hcp.unparcellate(filtered_df(), hcp.mmp)), cmap="viridis", bg_map=hcp.mesh.sulc, vmax = input.plot_max(), threshold = 0.00000001)
    #     html = surf_plot.get_iframe() # get_iframe() or get_standalone()
    #     return ui.HTML(html)
    
    @render.ui
    def i2c2():
        surf_plot = plotting.view_surf(hcp.mesh.inflated, hcp.cortex_data(hcp.unparcellate(filtered_df_i2c2(), hcp.mmp)), cmap="viridis", bg_map=hcp.mesh.sulc, vmax = input.i2c2_max(), threshold = 0.00000001)
        html = surf_plot.get_iframe() # get_iframe() or get_standalone()
        return ui.HTML(html) 

    @render.ui
    def discr():
        surf_plot = plotting.view_surf(hcp.mesh.inflated, hcp.cortex_data(hcp.unparcellate(filtered_df_discr(), hcp.mmp)), cmap="viridis", bg_map=hcp.mesh.sulc, vmax = input.discr_max(), threshold = 0.00000001)
        html = surf_plot.get_iframe() # get_iframe() or get_standalone()
        return ui.HTML(html) 
    
    @render.ui
    def finger():
        surf_plot = plotting.view_surf(hcp.mesh.inflated, hcp.cortex_data(hcp.unparcellate(filtered_df_finger(), hcp.mmp)), cmap="viridis", bg_map=hcp.mesh.sulc, vmax = input.finger_max(), threshold = 0.00000001)
        html = surf_plot.get_iframe() # get_iframe() or get_standalone()
        return ui.HTML(html) 
    



    # @render.data_frame
    # def summary_statistics():
    #     cols = [
    #         "species",
    #         "island",
    #         "bill_length_mm",
    #         "bill_depth_mm",
    #         "body_mass_g",
    #     ]
    #     return render.DataGrid(filtered_df()[cols], filters=True)


app = App(app_ui, server)
