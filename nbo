import streamlit as st
import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def filter_data(data, orbital_types, top_n, ascending=True):
    filtered_data = data[data['Orbital'].isin(orbital_types)]
    sorted_data = filtered_data.sort_values(by='Delta E', ascending=ascending)
    return sorted_data.head(top_n)

def main():
    st.title("Orbital Energy Analyzer")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        data = load_data(uploaded_file)

        # Display raw data
        st.subheader("Raw Data:")
        st.write(data)

        # Filter by orbital type
        selected_orbital = st.selectbox("Select Orbital Type (Optional):", ['All'] + list(data['Orbital'].unique()))
        if selected_orbital != 'All':
            data = data[data['Orbital'] == selected_orbital]

        # Display filtered data
        st.subheader("Filtered Data:")
        st.write(data)

        # Filter by top or bottom energies
        filter_type = st.radio("Select Filter Type:", ["Top", "Bottom"])
        top_n = st.number_input("Number of Orbitals to Display:", min_value=1, max_value=len(data), value=10)

        if filter_type == "Top":
            st.subheader(f"Top {top_n} Orbitals:")
            result = filter_data(data, data['Orbital'].unique(), top_n)
        else:
            st.subheader(f"Bottom {top_n} Orbitals:")
            result = filter_data(data, data['Orbital'].unique(), top_n, ascending=False)

        st.write(result)

if __name__ == "__main__":
    main()
