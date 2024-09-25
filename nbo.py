import pandas as pd
import streamlit as st
import io

# Function to filter and process NBO data
def process_nbo_data(file, ignore_orbitals, top_values):
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(file)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return pd.DataFrame()

    # Check if 'kcal/mol' column exists
    if 'kcal/mol' not in df.columns:
        st.warning("Column 'kcal/mol' not found in the uploaded CSV file.")
        return pd.DataFrame()

    if ignore_orbitals:
        # Create a regex pattern to match any of the ignore_orbitals
        pattern = '|'.join(ignore_orbitals)
        # Check if any cell in a row contains the pattern
        mask = df.astype(str).apply(lambda row: row.str.contains(pattern, case=False)).any(axis=1)
        # Invert the mask to keep rows without specified orbitals
        df_filtered = df[~mask]
    else:
        df_filtered = df

    if df_filtered.empty:
        st.warning("No data left after filtering with the specified orbitals.")
        return pd.DataFrame()

    # Sort the DataFrame by 'kcal/mol' in descending order
    df_sorted = df_filtered.sort_values(by='kcal/mol', ascending=False)

    # Take the top rows based on the specified number
    top_rows = df_sorted.head(top_values)

    # Convert the top rows DataFrame to CSV for download
    csv = top_rows.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Top Rows as CSV",
        data=csv,
        file_name='top_sorted_result.csv',
        mime='text/csv',
    )

    st.success(f"Top {top_values} rows based on 'kcal/mol' processed successfully.")
    return top_rows

# Streamlit web application
def main():
    st.set_page_config(page_title="NBO Data Processing", layout="wide")
    st.title("NBO Data Processing")

    # Option to upload CSV file
    uploaded_file = st.file_uploader("Upload NBO CSV File", type=["csv"])

    if uploaded_file is not None:
        try:
            # Attempt to read a few rows to ensure it's a valid CSV
            preview_df = pd.read_csv(uploaded_file, nrows=5)
            st.write("### Preview of Uploaded Data")
            st.dataframe(preview_df)
            # Reset the file pointer to the beginning
            uploaded_file.seek(0)
        except Exception as e:
            st.error(f"Error reading the uploaded file: {e}")
            return

    # Options for orbitals to ignore and number of top values
    ignore_orbitals = st.multiselect(
        "Select Orbitals to Ignore",
        options=['CR', 'LP', 'RY*'],
        default=[]
    )
    top_values = st.slider(
        "Select Number of Top Values",
        min_value=1,
        max_value=100,
        value=5,
        step=1
    )

    # Process the data when the user clicks the 'Process' button
    if st.button("Process"):
        if uploaded_file is not None:
            top_rows = process_nbo_data(uploaded_file, ignore_orbitals, top_values)
            if not top_rows.empty:
                st.write("### Processed Top Rows")
                st.dataframe(top_rows)
        else:
            st.warning("Please upload a CSV file to proceed.")

if __name__ == "__main__":
    main()
