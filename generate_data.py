

import pandas as pd
import numpy as np
import datetime

# --- Simulation Parameters (from GEMINI.md) ---

# Timeframe
start_date = datetime.date(2025, 1, 1)
end_date = datetime.date(2025, 6, 30)
N_DAYS = (end_date - start_date).days

# Employee Pool
TOTAL_EMPLOYEES = 12000
DEPARTMENTS = {
    'Global Markets': 0.15,
    'Wealth & Personal Banking': 0.20,
    'Operations': 0.25,
    'IT': 0.20,
    'Human Resources': 0.10,
    'Corporate Services': 0.10
}

# Location Details
LOCATIONS = {
    'Hong Kong': {
        'cities': {
            'Hong Kong': ['HKG Main Office Tower 1', 'HKG Tower 2']
        },
        'occupancy_variation': 0.05, # Higher traffic
        'capacity_per_building': [2500, 2000]
    },
    'Singapore': {
        'cities': {
            'Singapore': ['SGP Marina Bay Financial Centre', 'SGP Business Park']
        },
        'occupancy_variation': 0.05,
        'capacity_per_building': [2800, 1800]
    },
    'Malaysia': {
        'cities': {
            'Kuala Lumpur': ['KUL Menara HSBC']
        },
        'occupancy_variation': -0.05, # Slightly lower traffic
        'capacity_per_building': [1000]
    },
    'Australia': {
        'cities': {
            'Sydney': ['SYD International Tower']
        },
        'occupancy_variation': -0.03,
        'capacity_per_building': [800]
    }
}

SPACE_TYPES = {
    'Individual Workstation': {'capacity': 1, 'booking_prob': 0.60},
    'Quiet Pod': {'capacity': 1, 'booking_prob': 0.10},
    'Small Meeting Room (2-4 pax)': {'capacity': 4, 'booking_prob': 0.15},
    'Medium Meeting Room (6-8 pax)': {'capacity': 8, 'booking_prob': 0.10},
    'Large Meeting Room (10+ pax)': {'capacity': 15, 'booking_prob': 0.03},
    'Collaboration Zone': {'capacity': 10, 'booking_prob': 0.02}
}

# Hybrid Work Patterns
DAY_OF_WEEK_OCCUPANCY = {
    0: 0.35, # Mon
    1: 0.62, # Tue
    2: 0.68, # Wed
    3: 0.65, # Thu
    4: 0.30  # Fri
}
NO_SHOW_RATE = 0.15
ADHOC_BOOKING_RATE = 0.20 # 20% of bookings are ad-hoc walk-ins

# --- Helper Functions ---

def create_employee_data(n_employees, departments):
    """Creates a DataFrame of employees with their assigned department."""
    employee_ids = range(1, n_employees + 1)
    employee_deps = np.random.choice(
        list(departments.keys()),
        size=n_employees,
        p=list(departments.values())
    )
    return pd.DataFrame({'Employee_ID': employee_ids, 'Department': employee_deps})

def create_space_inventory():
    """Creates a DataFrame representing all available spaces across all locations."""
    spaces = []
    space_id_counter = 1
    for country, country_data in LOCATIONS.items():
        for city, buildings in country_data['cities'].items():
            for i, building in enumerate(buildings):
                capacity = country_data['capacity_per_building'][i]
                for space_type, type_data in SPACE_TYPES.items():
                    num_spaces = int(capacity * type_data['booking_prob'] / type_data['capacity'])
                    for _ in range(num_spaces):
                        spaces.append({
                            'Space_ID': space_id_counter,
                            'Region': 'ASP',
                            'Country': country,
                            'City': city,
                            'Building': building,
                            'Floor': np.random.randint(5, 25),
                            'Space_Type': space_type,
                            'Capacity': type_data['capacity']
                        })
                        space_id_counter += 1
    return pd.DataFrame(spaces)

# --- Main Simulation Logic ---

def generate_raw_data():
    """
    Generates a realistic raw_workspace_data.csv file based on the defined
    simulation parameters.

    This script simulates daily workspace bookings and check-ins over a specified
    period, incorporating hybrid work patterns, regional variations, and
    departmental behaviors.
    """
    print("Starting data generation...")
    print("1. Creating employee and space inventories...")
    employees_df = create_employee_data(TOTAL_EMPLOYEES, DEPARTMENTS)
    spaces_df = create_space_inventory()

    all_bookings = []
    date_range = pd.to_datetime(pd.date_range(start=start_date, end=end_date))

    print(f"2. Simulating bookings for {len(date_range)} days...")
    for current_date in date_range:
        day_of_week = current_date.dayofweek
        if day_of_week > 4: # Skip weekends
            continue

        # Determine number of employees in office today
        base_occupancy = DAY_OF_WEEK_OCCUPANCY[day_of_week]
        
        # Each employee decides to come in based on the day's probability
        # Adding some randomness per employee
        u = np.random.rand(TOTAL_EMPLOYEES)
        employees_present_today = employees_df[u < base_occupancy]
        
        if employees_present_today.empty:
            continue

        # Assign employees to buildings for the day
        # For simplicity, randomly assign to a building within a country
        # A more complex model could have home locations
        present_employees_with_loc = []
        for dep in employees_present_today['Department'].unique():
            dep_employees = employees_present_today[employees_present_today['Department'] == dep]
            # Assign all employees from a department to the same country for the day to simulate team days
            country = np.random.choice(list(LOCATIONS.keys()))
            for emp_id in dep_employees['Employee_ID']:
                 present_employees_with_loc.append({'Employee_ID': emp_id, 'Department': dep, 'Country': country})
        
        if not present_employees_with_loc:
            continue
            
        daily_employees_df = pd.DataFrame(present_employees_with_loc)
        
        # Simulate bookings for these present employees
        for _, employee in daily_employees_df.iterrows():
            # Decide booking type: ad-hoc or pre-booked
            is_adhoc = np.random.rand() < ADHOC_BOOKING_RATE
            
            # Choose a space in their assigned country
            possible_spaces = spaces_df[spaces_df['Country'] == employee['Country']]
            if possible_spaces.empty:
                continue

            chosen_space = possible_spaces.sample(1, weights=possible_spaces['Capacity']).iloc[0]

            # Determine booking status
            if not is_adhoc and np.random.rand() < NO_SHOW_RATE:
                status = 'No-Show'
            else:
                status = 'Confirmed'

            booking_time = (datetime.datetime.combine(current_date, datetime.time(9, 0)) + 
                            datetime.timedelta(hours=np.random.uniform(-1, 8))).time()

            all_bookings.append({
                'Date': current_date.date(),
                'Time': booking_time,
                'Employee_ID': employee['Employee_ID'],
                'Department': employee['Department'],
                'Activity_Type': 'Check-in' if is_adhoc else 'Desk Booking',
                'Space_ID': chosen_space['Space_ID'],
                'Booking_Status': status,
                'Region': chosen_space['Region'],
                'Country': chosen_space['Country'],
                'City': chosen_space['City'],
                'Building': chosen_space['Building'],
                'Floor': chosen_space['Floor'],
                'Space_Type': chosen_space['Space_Type']
            })

    print("3. Finalizing DataFrame and saving to CSV...")
    final_df = pd.DataFrame(all_bookings)
    
    # Ensure correct data types
    for col in ['Employee_ID', 'Space_ID', 'Floor']:
        final_df[col] = pd.to_numeric(final_df[col])

    final_df['Date'] = pd.to_datetime(final_df['Date'])

    # Save the file
    output_filename = 'raw_workspace_data.csv'
    final_df.to_csv(output_filename, index=False)
    print(f"\nSuccessfully generated '{output_filename}' with {len(final_df)} records.")
    print("Data generation complete.")


if __name__ == '__main__':
    generate_raw_data()

