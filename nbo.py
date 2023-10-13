import pandas as pd
import streamlit as st

# Function to filter and process NBO data
def process_nbo_data(file_path, ignore_orbitals, top_values):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Create a boolean mask to identify rows containing specified orbitals
    mask = df.apply(lambda row: any([orbital in str(cell) for cell in row for orbital in ignore_orbitals]), axis=1)

    # Invert the mask to keep rows without specified orbitals
    df_filtered = df[~mask]

    # Check if 'kcal/mol' column exists
    if 'kcal/mol' in df_filtered.columns:
        # Sort the DataFrame by 'kcal/mol' in descending order
        df_sorted = df_filtered.sort_values(by='kcal/mol', ascending=False)
        
        # Take the top rows based on the specified number
        top_rows = df_sorted.head(top_values)

        # Save the top rows to a new CSV file
        top_rows.to_csv('top_sorted_result.csv', index=False)
        
        st.success(f"Top {top_values} rows based on 'kcal/mol' saved to 'top_sorted_result.csv'")
        return top_rows
    else:
        st.warning("Column 'kcal/mol' not found in the filtered DataFrame.")
        return pd.DataFrame()

# Streamlit web application
st.title("NBO Data Processing")

# Option to upload CSV file
uploaded_file = st.file_uploader("Upload NBO CSV File", type=["csv"])

# Options for orbitals to ignore and number of top values
ignore_orbitals = st.multiselect("Orbitals to Ignore", ['CR', 'LP', 'RY*'])
top_values = st.slider("Select Number of Top Values", min_value=1, max_value=20, value=5)

# Process the data when the user clicks the 'Process' button
if st.button("Process"):
    if uploaded_file is not None:
        # Process NBO data and display information
        top_rows = process_nbo_data(uploaded_file, ignore_orbitals, top_values)
        st.dataframe(top_rows)
    else:
        st.warning("Please upload a CSV file.")
