# Workspace Analytics Dashboard

This project provides a comprehensive solution for analyzing and optimizing workspace utilization in a hybrid work environment. It simulates realistic workspace data for HSBC's ASP (Asia-Pacific) region and presents the findings in an interactive, web-based dashboard.

The primary goal is to provide a Workspace Analytics Manager with actionable insights into key performance indicators (KPIs) such as office occupancy, space utilization, and booking behaviors, enabling data-driven decisions for real estate and workspace management.

## Key Features

*   **Realistic Data Simulation**: Generates a rich dataset modeling ~12,000 employees across multiple countries, buildings, and departments.
*   **Normalized Database**: Uses a SQLite database to store the data in a structured and efficient manner, demonstrating good data architecture principles.
*   **Interactive Dashboard**: A web-based dashboard built with Streamlit allows for dynamic filtering and visualization of the data.
*   **AI-Powered Insights**: Features an on-demand, context-aware assistant that generates analytical insights and recommendations based on the filtered data.
*   **KPI-Driven Analysis**: Focuses on core KPIs:
    1.  **Occupancy & Peak Trends**: Tracks daily, weekly, and monthly usage to understand peak demand.
    2.  **Space Utilization**: Measures how effectively different types of spaces (desks, meeting rooms) are being used.
    3.  **Booking Efficiency**: Analyzes booking no-show rates and ad-hoc usage patterns.

## Tech Stack

*   **Python**: The core language for scripting and analysis.
*   **Pandas & NumPy**: For data generation and manipulation.
*   **SQLite**: As the relational database.
*   **Streamlit & Plotly**: For building the interactive web dashboard.
*   **Google Generative AI**: For the AI-powered insight generation.

---

## How to Set Up and Run This Project

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

*   Python 3.10+

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python3 -m venv .venv

# Note: You do not need to activate it manually; the following scripts will use it directly.
```

### 3. Set Up Environment Variables

This project uses Google's Generative AI to provide insights. You need to provide your own API key.

1.  Create a new file named `.env` in the root of the project directory.
2.  Add the following line to the `.env` file, replacing `YOUR_API_KEY` with your actual key:

    ```
    GEMINI_API_KEY="YOUR_API_KEY"
    LLM_MODEL="gemini-1.5-flash"
    ```

### 4. Install Dependencies

Install all the necessary Python libraries into the virtual environment.

```bash
.venv/bin/pip install pandas numpy streamlit plotly google-generativeai python-dotenv
```

### 5. Generate the Raw Data

Run the data generation script. This will create a `raw_workspace_data.csv` file containing the simulated data.

```bash
.venv/bin/python generate_data.py
```

### 5. Create and Populate the Database

Run the ingestion script. This reads the CSV file and populates the `workspace_analytics.db` SQLite database.

```bash
.venv/bin/python load_to_sqlite.py
```

### 6. Run the Dashboard

Start the Streamlit web server to view the interactive dashboard.

```bash
.venv/bin/streamlit run dashboard.py
```

Your web browser should open to a local URL (e.g., `http://localhost:8501`). If not, copy the URL from your terminal into your browser.

---

## Project Structure

```
/HSBC_WAM/
├── .venv/                     # Isolated Python virtual environment
├── raw_workspace_data.csv     # Raw, simulated data file (generated)
├── workspace_analytics.db     # SQLite database file (generated)
├── generate_data.py           # Script to simulate and generate the raw CSV data
├── load_to_sqlite.py          # Script to load CSV data into the SQLite database
├── dashboard.py               # The main Streamlit dashboard application script
├── README.md                  # This file
├── GEMINI.md                  # The project execution plan and context
└── TODO.md                    # The task tracker for the project
```
