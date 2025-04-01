import streamlit as st
from fee_scraper import fetch_school_fees, SCHOOL_FEES_PAGES

st.title("💷 UK Boarding School Fees Explorer")

school = st.selectbox("Select a school", list(SCHOOL_FEES_PAGES.keys()))

if st.button("Fetch Fees"):
    with st.spinner("Looking for the main fees..."):
        result = fetch_school_fees(school)
        if "error" in result:
            st.error(result["error"])
        else:
            st.markdown(f"### 💼 Core Fees for {school}")
            st.markdown(f"[🔗 View official source]({result['url']})")
            for line in result["fees"]:
                st.success(line)
