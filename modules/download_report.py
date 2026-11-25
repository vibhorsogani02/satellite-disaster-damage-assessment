
import streamlit as st
import pandas as pd


def show_csv_download(classified_regions):

    st.subheader("Download Damage Report")

    if not classified_regions:
        st.warning("No damage regions available.")
        return

    # Convert results into DataFrame
    df = pd.DataFrame(classified_regions)

    # Convert DataFrame into CSV
    csv_data = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="disaster_damage_report.csv",
        mime="text/csv"
    )
