
import pandas as pd

from shiny import App, Inputs, Outputs, Session, render, ui, reactive

data = pd.read_csv("all_rois_mv_results.csv")


app_ui = ui.page_fluid(
    ui.input_slider("input_number", "Enter a number from 1 to 379:", min=1, max=379, value=1),
    ui.output_table("result"),
    class_="p-3",
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def update_filtered_data():
            filtered_data = data[data['roi'] == input.input_number]
            return filtered_data
        
        # Call the observer whenever the input ROI number changes
    
    @render.table
    def result():
            return (
            filtered_data.style.set_table_attributes(
                'class="dataframe shiny-table table w-auto"'
            )
        )



app = App(app_ui, server)

