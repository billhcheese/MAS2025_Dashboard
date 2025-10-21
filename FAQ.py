import streamlit as st

st.set_page_config(page_icon="Assets/metro-atl-speaks.svg")

custom_css = """
<style>
.stMainBlockContainer {
            max-width:65rem;
        }
.stSelectbox div[data-baseweb="select"] > div:first-child {
    border: 2px solid #808080; /* Example: 2px solid green border */
    border-radius: 5px; /* Optional: rounded corners */
}
/* This selector might need adjustment based on your Streamlit version and specific setup */
.stHeaderLogo img {
    width: auto; /* Adjust as needed */
    height: 100px; /* Maintain aspect ratio */
}
.stAppHeader { /* This class targets the top navigation container */
    background-color: #f9f9f9;
    min-height: 50px; /* Adjust height as needed */
    padding-top: 20px; /* Add padding for vertical spacing */
    padding-bottom: 20px;
}

/* Navigation menu items - comprehensive targeting */
.rc-overflow-item,
[data-testid="stHeader"] .rc-overflow-item,
.stAppHeader .rc-overflow-item,
header .rc-overflow-item,
.stApp > header .rc-overflow-item,
.stAppHeader *,
[data-testid="stHeader"] *,
header *,
.stApp > header * {
    font-size: 18px !important;
    font-weight: 600 !important;
    
}

.rc-overflow-item { /* This class targets the individual navigation items */
    font-size: 20px; /* Adjust font size as needed */
    padding: 15px; /* Adjust padding for button size */
}

/* Floating scroll down icon */
.scroll-indicator {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    background-color: #2364a0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
    opacity: 0.8;
}

.scroll-indicator::before {
    content: "↓";
    color: white;
    font-size: 24px;
    font-weight: bold;
}

/* Remove bouncing animation - keeping it static */
</style>
"""

# Inject the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)
st.logo("Assets/arc-logo-black-trans.png",size="large")

# Create title with logo
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("Assets/metro-atl-speaks.svg", width=350)
with col_title:
    st.markdown("""
    <div style='color: #2364a0; font-size: 40px; font-weight:Semibold ; margin-top: 13px;'>
        <p>FAQ</p>
    </div>
    """, unsafe_allow_html=True)

with st.expander("What is the Metro Atlanta Speaks Survey?", expanded=True):
    st.write("""
        The Atlanta Regional Commission (ARC), in collaboration with Kennesaw State University’s A.L. Burruss Institute
        of Public Service & Research, has conducted the Metro Atlanta
        Speaks Survey (MAS), since 2013, to take the pulse of metro Atlanta residents and inform the region's planning and
        decision-making. The survey, now in its 11th year, is the largest survey of perceptions and attitudes in the Atlanta
        region. MAS offers a statistically representative snapshot of residents across the Atlanta area on various topics including
        transportation, the economy, workforce development, housing and affordability, quality of life, and other
        emerging regional issues. Extensive demographic crosstabs, at the regional level, enhance the value of the results for
        narrowing in on differences of opinion.
        """)

with st.expander("What is the methodology of the Metro Atlanta Speaks Survey?"):
    st.write("""
        For the first eight years of the survey, random-digit dial (RDD) was the method, with cellphone share (compared to
        landline) increasing each year. For the last five years, with technological change and also due to need to reduce costs,
        the survey became mixed mode, with an online component added to the RDD element. Find more details at the MAS
        report on the website https://atlantaregional.org/what-we-do/research-and-data/metro-atlanta-speaks-survey-report/
        """)

with st.expander("I have more questions that are not on this FAQ, what should I do?"):
    st.write("""
        You can find more details about the MAS 2025 Survey at https://atlantaregional.org/what-we-do/research-and-data/metro-atlanta-speaks-survey-report/. 
        If you cannot find an answer to your question there, contact Bill Huang at bhuang@atlantaregional.org .
        """)

with st.expander("Why are some demographic groups not shown in the dashboard?"):
    st.write("""
        Some demographic groups are difficult to survey to a significant level of confidence because they are small percentages of the current population,
         and we do not have enough random samples to be confident in the accuracy of the results. We collected results from people who identify with
        gender in a different way other than Male or Female. While, these responses influence the survey's tabulations, the sample count was too low to view this groups
        responses through that specific gender demographic group tabulation. You can see the full list of surveyed groups in the report at 
        https://atlantaregional.org/what-we-do/research-and-data/metro-atlanta-speaks-survey-report/ even though we may not display them in the dashboard.
        """)

with st.expander("Why aren't questions on 'X topic' or more questions on 'Y topic' asked in the survey?"):
    st.markdown("""
        Costs of doing any extensive surveying continue to mount. Reasons such as
        1. expanding the number of questions asked in a survey tends to reduce response rate and increase costs
        2. asking just one question in a topic area is generally unhelpful
        3. ARC has many "mission-centric areas (like transportation and land use) that we focus on 
        4. There are politically sensitive issues in which a regional commission shouldn't be involved.
        
        That said, reach out to Bill Huang at bhuang@atlantaregional.org if you want to suggest a question that might be viable for the survey.
        """)

with st.expander("Can I export the data or download the dashboard graphics?"):
    st.write("""
        Yes you can! If you hover over the top right hand corner of the graphs, you will see a "..." symbol button.
        Clicking on that will give you the option download the dashboard graphics.
        To access the data, you can find the tables on https://atlantaregional.org/what-we-do/research-and-data/metro-atlanta-speaks-survey-report/. 
        """)

with st.expander("Could I get crosstabs of the demographic results by county, rather than just by region? For instance, I'd like to know what older people in Fayette County think about transit."):
    st.write("""
        No. While extracting those results would technically be possible, that level of data is statistically insignificant. As
        such, they might be used inadvertently to inform or support inaccurate conclusions or decisions.
        """)

with st.expander("What area(s) is (are) cover by the MAS survey?"):
    st.write("""
        The areas covered have varied by iteration of the survey. The "prime" focus has always been the Atlanta Regional
        Commission area. As such, for the last five years, MAS has covered the eleven counties of ARC along with the City of
        Atlanta. For five of the earlier years of the survey, the ten ARC counties (of that time) plus three added counties were
        covered, to meet the needs of a client sponsor. In the first year for MAS (2013), ten counties were covered, with
        results only representative regionally.
        """)

with st.expander("Why do some graphs not include certain years, answers, or questions?"):
    st.write("""
        Not every question was asked every year and not every answer for a question was avaliable every year. The survey
        also was not conducted every year. The MAS data before 2016 data is unavaliable in this dashboard.
        For example, the MAS survey was not conducted in 2022.
        """)

with st.expander("What is the level of statistical significance of the survey results?"):
    st.write("""
        Again, there is variation. At the regional level (whatever the overall region has been, in any given year), results have
        also had margins of error (MOEs) of under 2%, usually under 1.5%, meaning that the "true" result is only a maximum
        of 2% higher or lower than the sampled result that is reported. For the core, larger counties, as well as for the City of
        Atlanta, MOEs have ranged from 3% to 5%. For smaller suburban and exurban counties, MOEs have ranged from 5%
        to 7%.
        """)

with st.expander("How many people are surveyed (i.e. what is the N)?"):
    st.write("""
        The N has changed with the coverage and the methodology. In the first year of the survey (2013), with regional-only
        significance, 2,200 people were surveyed. Since then, the N has varied from about 4,000 to about 5,500. The number
        surveyed by jurisdiction has varied between 200 and 500. Fulton has been surveyed above 600 in various years due 
        to oversampling for reporting on the City of Atlanta sub geography.
        """)

# Logo display
st.markdown("---")  # Add a separator line

st.text("Survey Results Courtesy of the Kennesaw State University's A.L. Burruss Institute of Public Service & Research and the ARC Research & Innovation")

# Create centered columns with better alignment
col1, col2, col3 = st.columns([1, 1, 1], gap="large")

with col1:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("Assets/Fw_ltnUt_400x400.png", width=300, use_container_width=False)
    st.link_button("Visit KSU Burruss Institute", "https://www.kennesaw.edu/external-affairs/burruss-institute/index.php")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("Assets/logo-with-text.svg", width=200, use_container_width=False)
    st.link_button("Visit Atlanta Regional Commission", "https://atlantaregional.org/")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p><span style='color: #2364a0; font-size: 15px; font-weight: Bold;'>More data from ARC Research & Innovation</span></p>", unsafe_allow_html=True)
    st.link_button("Visit ARC Research & Innovation", "https://atlantaregional.org/what-we-do/research-and-data/")
    st.link_button("Visit ARC Open Data", "https://opendata.atlantaregional.com/")
    st.link_button("Visit ARC 33°n Blog", "https://33n.atlantaregional.com/")
    st.markdown("</div>", unsafe_allow_html=True)
