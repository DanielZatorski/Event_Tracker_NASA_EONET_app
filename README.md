# Open Events Tracker App

## Overview

The **Open Events Tracker** is a Python-based application that leverages NASA's **EONET (Earth Observatory Natural Event Tracker) API v3** to provide a dynamic, interactive platform for tracking real-time natural events such as wildfires, hurricanes, volcanic activity, and more. The app is developed using the **Streamlit framework**, which allows users to visualize and interact with the data in a user-friendly interface.

### Key Features
- **Interactive GUI:** An intuitive interface developed with Streamlit that allows users to explore and track global natural events.
- **Real-Time Event Tracking:** Fetches up-to-date event data from NASA's EONET API.
- **Custom Filters:** Users can filter events by date, type (e.g., wildfires, storms), and geographical location.
- **Data Visualizations:** Visualize event data on interactive maps to analyze occurrences
- **CSV Export:** Download the event data for further analysis

### Components
- **`appscript.py`**: Manages the main application interface and event tracking functionalities using Streamlit.
- **`test_api_data_fetch.py`**: Handles API data fetching, testing, and interaction with NASA's EONET API.


## Requirements
- **Python 3.12**

## Installation & Usage

1. **Clone the repository** to your local machine:
   ```bash
   git clone https://github.com/your-repo/Open-Events-Tracker.git
