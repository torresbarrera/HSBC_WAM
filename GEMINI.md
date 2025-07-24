Of course. Here is the plan in a raw text format that you can save as a `.md` file.

```text
# `GEMINI.md` - Project Execution Guide

## 1. Core Philosophy & Guiding Principles

This project will be executed following a strict set of principles to ensure a high-quality, practical outcome. The AI assistant (Gemini) and the developer (you) must adhere to this philosophy throughout the project lifecycle.

1.  **No Overengineering**: We will always favor the simplest, most direct solution that meets the requirements. We will actively avoid adding complexity that isn't immediately necessary for the 12-hour goal.
2.  **Brutally Honest Feedback**: The AI assistant will provide direct, critical feedback on requests, questioning assumptions to build the *right* system, not just the requested one. The developer should also adopt this critical mindset.
3.  **Propose and Explain First**: All code generation or significant actions will be preceded by a clear explanation of the proposed approach and the reasoning behind it. This ensures mutual understanding.
4.  **Simplicity Over Complexity**: A simple, understandable solution is better than a complex, "clever" one.
5.  **Follow Best Practices**: We will adhere to sound software engineering practices, including separation of concerns, writing maintainable and well-commented code, and providing clear usage documentation for all scripts.
6.  **Maintain Living Documentation**: The `TODO.md` file will be the single source of truth for project status. It must be updated as tasks are planned, implemented, and completed.

***

## 2. Project Management: The `TODO.md` System

All tasks will be tracked in a file named `TODO.md`. This file will be created and updated at the beginning and end of each work session.

The `TODO.md` will use the following structure:

| Phase | Module | Task | Status | Owner | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 1.1 | Define final KPIs | `Not Started` | Dev | Must align with JD. |
| ... | ... | ... | ... | ... | ... |

* **Status**: `Not Started`, `In Progress`, `Completed`, `Blocked`.
* **Owner**: `Dev` (You) or `Gemini` (The AI assistant).

***

## 3. Project Plan: Hybrid Work Model Optimization Dashboard

The project is divided into two distinct stages: **Planning** and **Implementation**. We must complete the Planning stage thoroughly before moving to Implementation.

### **Stage 1: Planning & Design (Critical Thinking Phase)**

**Objective**: To have a complete blueprint for the project, including data structures, simulation logic, and dashboard layout, before writing a single line of implementation code.

* **Module 1.1: Project Scoping & KPI Definition**
    * **Goal**: Finalize the exact questions the dashboard will answer for the target audience (Workspace Analytics Manager).
    * **Action**: Discuss and define the 3-5 most impactful KPIs. Examples: Peak Daily Occupancy, Utilization by Space Type, Popular "Collaboration Days," Booking No-Show Rate, Department-level Occupancy.
    * **Output**: A documented list of the chosen KPIs and the business questions they address.

* **Module 1.2: Data Schema & Enhanced Simulation Logic Design**
    * **Goal**: Design the structure of the raw data and the rules for the simulation to ensure realism, including scale and key characteristics.
    * **Action**:
        1.  Define the exact columns for the `raw_workspace_data.csv` file.
            * **Core Data Points**: `Date`, `Time`, `Employee_ID`, `Activity_Type` (e.g., 'Desk Booking', 'Meeting Room Booking', 'Check-in'), `Space_ID`, `Booking_Status` (e.g., 'Confirmed', 'Cancelled', 'No-Show').
            * **Key Dimensions (for realism and regional analysis)**:
                * `Region` (e.g., 'ASP')
                * `Country` (e.g., 'Hong Kong', 'Singapore', 'Malaysia', 'Australia')
                * `City` (e.g., 'Hong Kong', 'Singapore', 'Kuala Lumpur', 'Sydney')
                * `Building` (e.g., 'HKG Main Office Tower 1', 'SGP Marina Bay Financial Centre', 'KUL Menara HSBC')
                * `Floor` (e.g., '10', '11', '12')
                * `Space_Type` (e.g., 'Individual Workstation', 'Small Meeting Room (2-4 pax)', 'Medium Meeting Room (6-8 pax)', 'Large Meeting Room (10+ pax)', 'Quiet Pod', 'Collaboration Zone')
                * `Department` (e.g., 'Global Markets', 'Wealth & Personal Banking', 'Operations', 'IT', 'Human Resources', 'Corporate Services')
        2.  Outline the Python script's logic in pseudocode, incorporating the following realistic simulation parameters:
            * **Simulated Timeframe**: Generate data for a period of **3-6 months** to capture trends.
            * **Total Employee Pool (CS, ASP Region)**: Simulate an employee base of **~12,000 Corporate Services employees** across the ASP region who regularly utilize office space.
            * **Number of Locations**: Focus on **6-8 significant office buildings/locations** across 3-4 key countries in the ASP region (e.g., 2-3 in HKG, 2 in SGP, 1-2 in KUL, 1 in SYD).
            * **Typical Office Capacity per Location**:
                * Major Hubs (HKG, SGP): **1,500 - 3,000 available spaces** (desks + meeting room capacities) per large building.
                * Smaller Offices (KUL, SYD): **500 - 1,000 available spaces** per building.
            * **Hybrid Work Patterns (as daily occupancy percentage of available spaces/employees):**
                * **Peak Days (Tuesday, Wednesday, Thursday):** Simulate **55-70%** overall occupancy/presence.
                * **Off-Peak Days (Monday, Friday):** Simulate **25-45%** overall occupancy/presence.
                * **Regional/Country Variation**: Introduce slight random variation (e.g., +/- 5-10%) in these percentages by country to reflect different local hybrid policies or cultural norms.
            * **Departmental Activity:** Assign employees to departments and vary their likelihood of being in the office or booking specific space types. For example:
                * `Operations` and `Global Markets` might have higher in-office attendance rates.
                * `IT` or `Project Management` might have more flexible attendance.
            * **Space Type Utilization Mix:**
                * Individual workstations: Highest volume of bookings/check-ins.
                * Small/Medium meeting rooms: High booking frequency.
                * Large meeting rooms: Lower frequency, but important for strategic meetings.
                * Quiet pods/Collaboration zones: Moderate usage.
            * **Booking No-Show Rate**: Simulate a **15% no-show rate** for pre-booked spaces.
            * **"Walk-in" vs. "Pre-booked"**: Differentiate between pre-booked spaces and ad-hoc check-ins to reflect real-world usage.
    * **Output**: A documented schema and a detailed pseudocode plan for the data generation script, incorporating these realistic numbers and regional dimensions.

* **Module 1.3: Dashboard Wireframing**
    * **Goal**: Create a low-fidelity design of the final dashboard.
    * **Action**: Sketch the layout. Where do the main KPIs go? What charts will be used and where will they be placed? How will the "Recommendations" section be featured? The focus is on creating a clear narrative flow.
    * **Output**: A simple visual wireframe or a structured text description of the dashboard layout.

### **Stage 2: Implementation & Delivery (Execution Phase)**

**Objective**: To build and deliver a robust, database-driven analytics dashboard.

*   **Module 2.1: Data Generation Script**
    *   **Goal**: Create a clean, well-commented Python script that generates the simulated data.
    *   **Action (Gemini)**: Based on the design from Module 1.2, generate the Python script using `pandas` and `numpy`.
    *   **Output**: A functional `generate_data.py` script and the resulting `raw_workspace_data.csv` file.

*   **Module 2.2: Database Creation & Data Ingestion**
    *   **Goal**: Architect and populate a normalized SQLite database.
    *   **Action (Gemini)**: Create a Python script (`load_to_sqlite.py`) that:
        1.  Defines a clean, normalized database schema (e.g., tables for `Bookings`, `Employees`, `Spaces`).
        2.  Reads the `raw_workspace_data.csv`.
        3.  Populates the SQLite database (`workspace_analytics.db`).
    *   **Output**: A well-structured `workspace_analytics.db` file.

*   **Module 2.3: Dashboard Implementation with Streamlit**
    *   **Goal**: Build an interactive web-based dashboard for data visualization.
    *   **Action (Gemini)**: Create a Python script (`dashboard.py`) using the Streamlit library that:
        1.  Connects to the `workspace_analytics.db`.
        2.  Executes SQL queries to calculate the defined KPIs.
        3.  Renders the charts, tables, and filters defined in the wireframe.
    *   **Output**: A functional `dashboard.py` Streamlit application.

*   **Module 2.4: AI-Powered Insight Generation**
    *   **Goal**: Integrate a generative AI model to provide on-demand, context-aware analysis of the displayed data.
    *   **Action (Gemini)**:
        1.  Add a "Generate Insights" button to the Streamlit dashboard.
        2.  Create a function that, when the button is clicked, gathers the aggregated data from the currently visible charts.
        3.  This data is formatted into a concise JSON object to serve as context for the LLM.
        4.  A carefully engineered prompt instructs the LLM to act as a senior analyst and generate a structured report with data-backed insights and actionable recommendations.
        5.  The generated report is then displayed in the dashboard.
    *   **Technology**: This will use the `google-generativeai` library, with the API key managed via a `.env` file.
    *   **Output**: A dynamic, AI-driven "Key Insights & Recommendations" section in the dashboard.

***

## 4. Tool Integration Strategy

The project will use a modern Python data stack:

*   **Data Generation**: `pandas` and `numpy` for efficient data manipulation.
*   **Database**: `SQLite` for a robust, file-based relational database.
*   **Dashboarding**: `Streamlit` for creating an interactive web application for analysis.
*   **AI Insights**: `google-generativeai` for on-demand, context-aware reporting.
*   **`context7`**: Not required for this project as we are using standard, well-known libraries.
*   **`gas_web_apps`**: No longer required for this implementation path.
```