import streamlit as st
import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def filter_data(data, ignore_values, top_n, filter_type):
    # Ignore rows containing specified values
    for value in ignore_values:
        data = data[~data['Orbital'].str.contains(value, na=False)]

    # Display top or bottom kcal/mol values
    if filter_type == 'Top':
        st.subheader(f"Top {top_n} Orbitals:")
        result = data.nlargest(top_n, 'kcal/mol')
    else:
        st.subheader(f"Bottom {top_n} Orbitals:")
        result = data.nsmallest(top_n, 'kcal/mol')

    st.write(result)

def main():
    st.title("Orbital Energy Analyzer")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        data = load_data(uploaded_file)

        # Display raw data
        st.subheader("Raw Data:")
        st.write(data)

        # Ignore specified orbitals
        ignore_values = st.multiselect("Ignore Orbitals:", ['RY*', 'BD', 'CR', 'LP'])

        # Filter by top or bottom energies
        filter_type = st.radio("Select Filter Type:", ["Top", "Bottom"])
        top_n = st.number_input("Number of Orbitals to Display:", min_value=1, max_value=len(data), value=10)

        # Apply filters and display results
        filter_data(data, ignore_values, top_n, filter_type)

if __name__ == "__main__":
    main()
