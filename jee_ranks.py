# # streamlit_app.py

import streamlit as st
import psycopg2
import pandas as pd

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()



# Fetch the data and columns
data = run_query("SELECT * FROM josaa")
df = pd.DataFrame(data)
df.columns = ['Institute', 'Program', 'Quota', 'Seat_Type', 'Gender', 'Opening_Rank', 'Closing_Rank', 'Year', 'Round']

# import streamlit as st
# import pandas as pd

# Load your dataframe
# df = pd.read_csv('data.csv')
# Create Streamlit UI
st.title("JEE Rank vs College Filter")
pd.set_option('display.max_columns', None)

with st.sidebar:
    # First Dropdown - Institute
    institutes = ["ALL"] + list(df["Institute"].unique())
    selected_institute = st.selectbox("Select Institute", institutes)
    if selected_institute != "ALL":
        filtered_df = df[df["Institute"] == selected_institute]
    else:
        filtered_df = df.copy()

    # Second Dropdown - Program
    programs = ["ALL"] + list(filtered_df["Program"].unique())
    selected_program = st.selectbox("Select Program", programs)
    if selected_program != "ALL":
        filtered_df = filtered_df[filtered_df["Program"] == selected_program]

    # Third Dropdown - Quota
    quotas = ["ALL"] + list(filtered_df["Quota"].unique())
    selected_quota = st.selectbox("Select Quota", quotas)
    if selected_quota != "ALL":
        filtered_df = filtered_df[filtered_df["Quota"] == selected_quota]

    # Fourth Dropdown - type
    seat_type = ["ALL"] + list(filtered_df["Seat_Type"].unique())
    selected_seat_type = st.selectbox("Select Seat Type", seat_type)
    if selected_seat_type != "ALL":
        filtered_df = filtered_df[filtered_df["Seat_Type"] == selected_seat_type]

    # Fifth Dropdown - Gender
    genders = ["ALL"] + list(filtered_df["Gender"].unique())
    selected_gender = st.selectbox("Select Gender", genders)
    if selected_gender != "ALL":
        filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]

    # Sixth Dropdown - Year
    years = ["ALL"] + list(filtered_df["Year"].unique())
    selected_year = st.selectbox("Select Year", years)
    if selected_year != "ALL":
        filtered_df = filtered_df[filtered_df["Year"] == selected_year]

    # Seventh Dropdown - Round
    rounds = ["ALL"] + list(filtered_df["Round"].unique())
    selected_round = st.selectbox("Select Round", rounds)
    if selected_round != "ALL":
        filtered_df = filtered_df[filtered_df["Round"] == selected_round]

    # Continue with other dropdowns or data display as needed

st.write(filtered_df.shape)  # Display the filtered dataframe

# Range Slider for Closing Rank
closing_rank_range = st.slider("Select Closing Rank Range", min_value=filtered_df["Closing_Rank"].min(), max_value=filtered_df["Closing_Rank"].max(), 
value=(filtered_df["Closing_Rank"].min(), filtered_df["Closing_Rank"].max()))

# Filter dataframe based on Closing Rank range
filtered_df = filtered_df[(filtered_df["Closing_Rank"] >= closing_rank_range[0]) & (filtered_df["Closing_Rank"] <= closing_rank_range[1])]


# Sort by column
st.write("Sort by Closing Rank")
ascending_checkbox = st.checkbox("Ascending")
descending_checkbox = st.checkbox("Descending")
sort_by_col = "Closing_Rank"

if ascending_checkbox:
    filtered_df = filtered_df.sort_values(by=sort_by_col, ascending=True)
elif descending_checkbox:
    filtered_df = filtered_df.sort_values(by=sort_by_col, ascending=False)

show_button = st.button("Show filtered results")
if show_button == 1:
    st.dataframe(filtered_df)

