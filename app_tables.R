# Load required libraries
library(shiny)
library(dplyr)

# Load your data
data <- read.csv("all_rois_mv_results.csv")
## TODO: add p-values

# Define UI
ui <- fluidPage(
  titlePanel("Movie vs. Rest Reliability Explorer"),
  sidebarLayout(
    sidebarPanel(
      selectInput("roi", "Select ROI:", choices = 1:379, selected = 1)
    ),
    mainPanel(
      # First section: i2c2 results
      h2("I2C2 Results"),
      tableOutput("i2c2_table"),
      
      # Second section: discr results
      h2("Discriminability Results"),
      tableOutput("discr_table"),
      
      # Third section: finger results
      h2("Fingerprinting Results"),
      tableOutput("finger_table")
    )
  )
)

# Define server logic
server <- function(input, output) {
  # Filtered data for i2c2 section
  i2c2_data <- reactive({
    data %>%
      filter(roi == input$roi) %>%
      select(roi, i2c2_m, i2c2_r, i2c2_diff) %>%
      rename("ROI" = "roi",
            "Movie" = "i2c2_m", 
             "Rest" = "i2c2_r", 
             "Movie-Rest Difference" = "i2c2_diff")
  })
  
  # Render i2c2 table
  output$i2c2_table <- renderTable({
    i2c2_data()
  })
  
  # Filtered data for discr section
  discr_data <- reactive({
    data %>%
      filter(roi == input$roi) %>%
      select(roi, discr_m, discr_r, discr_diff) %>%
      rename("ROI" = "roi",
            "Movie" = "discr_m", 
             "Rest" = "discr_r", 
             "Movie-Rest Difference" = "discr_diff")
  })
  
  # Render discr table
  output$discr_table <- renderTable({
    discr_data()
  })
  
  # Filtered data for finger section
  finger_data <- reactive({
    data %>%
      filter(roi == input$roi) %>%
      select(roi, finger_m, finger_r, finger_diff) %>%
      rename("ROI" = "roi",
            "Movie" = "finger_m", 
             "Rest" = "finger_r", 
             "Movie-Rest Difference" = "finger_diff")
  })
  
  # Render finger table
  output$finger_table <- renderTable({
    finger_data()
  })
}

# Run the application
shinyApp(ui = ui, server = server)
