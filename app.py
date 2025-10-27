import pandas as pd
import plotly.express as px
import streamlit as st
import st_utils as U
import st_constants as C


with st.sidebar:
    st.header("Treatment filters")
    cd = st.multiselect(
        "Citation Design",
        ["Icon", "Number", "Domain"],
        default=["Icon", "Number", "Domain"],
    )
    cs = st.multiselect("Context Stakeness", ["Low", "High"], ["Low", "High"])
    sr = st.multiselect(
        "Source Reliability", ["Low", "Original", "High"], ["Low", "Original", "High"]
    )

    st.markdown("**Colour plots by**")
    with st.expander("Info:"):
        st.info(
            "Please choose the treatment variable to be displayed as colour in plots on the right. Please note that for user level variables (like demographics), you will not see any change by choosing 'Context Stakeness'. This happens because 'Context Stakeness' is a within-group variable and a user doesn't have a unique value of context stakeness associated to them"
        )
    plot_color = st.selectbox(
        "Plot colour",
        ["None", "Citation Design", "Context Stakeness", "Source Reliability"],
    )
    st.markdown("---")

    st.header("Distributions to display")
    st.markdown("**Task level**")
    task_vars = st.multiselect(
        "Task level dependent variables",
        [
            "Task Duration",
            "Number of clicks",
            "Number of clicks on Search Result elements",
            "Number of clicks on AI Overview elements",
            "Number of clicks on citation design elements",
            "Was the show more button clicked?",
            "Number of clicks to external websites",
            "Amount of time when the cursor was on AI Overview",
            "Amount of time when the cursor was on Search Result elements",
            "Amount of time when the cursor was on Citation Design elements",
            "Total amount of time when the cursor was on AI Overview and Search Results",
            "Fraction of time cursor was on Search Results",
            "Fraction of time cursor was on AI Overview",
            "Fraction of time cursor was on Citation Design",
            "Number of mouse movements",
            "Number of scrolls",
            "Number of down (default direction) scrolls",
            "Number of up scrolls",
            "Median scroll duration across all scrolls",
            "Median scroll duration across up scrolls",
            "Median scroll duration across down scrolls",
            "Median scroll distance",
            "Median scroll distance for up scrolls",
            "Median scroll distance for down scrolls",
        ],
        default=[
            "Task Duration",
            "Number of clicks",
            "Number of clicks on Search Result elements",
        ],
    )

    st.markdown("Survey level")
    survey_vars = st.multiselect(
        "Survey level variables",
        [
            "Survey Duration",
            "How mentally demanding were the tasks?",
            "How hurried or rushed was the pace of the tasks?",
            "How hard did you have to work to accomplish your level of performance?",
            "How insecure, discouraged, irritated, stressed, and annoyed were you?",
            "Search Frequency",
            "Information Navigation",
            "Search Engine",
        ],
        default=[
            "How mentally demanding were the tasks?",
            "How hurried or rushed was the pace of the tasks?",
        ],
    )

    st.markdown("Demographics")
    dem_vars = st.multiselect(
        "Demographics",
        [
            "Gender",
            "Employment",
            "Highest education level completed",
            "Age",
            "Ethnicity (simplified)",
        ],
        default=[
            "Gender",
            "Employment",
        ],
    )

    st.markdown("---")
    st.header("Other configurations")

    st.subheader("Group by")
    col1, col2 = st.columns(2)
    with col1:
        grouping = st.radio("Group by", ["None", "User"])
    with col2:
        if grouping == "None":
            agg_method = st.selectbox(
                "Aggregation method",
                ["mean", "median", "max", "min"],
                index=0,
                disabled=True,
            )
        else:
            agg_method = st.selectbox(
                "Aggregation method", ["mean", "median", "max", "min"], index=0
            )


PATH = "0_final_data.csv"
df = pd.read_csv(PATH)
df["task_duration"] = df["task_duration"] / 1000
user_df = pd.read_csv("0_final_user_data.csv")

df = U.filter_by_treatments(df, cd=cd, cs=cs, sr=sr)


if grouping != "None":
    df = U.group_things(df, grouping, agg_method)

st.header("Variable distributions")
st.info(
    """
        Please choose the relevant filters etc. using sidebar on the left. If you're not able to see it yet, please click on the button on top left of your screen and now you should be able to!
        
        Every plot below gives you the count of corresponding values of x-axis. """
)

st.subheader("I. Task level (dependent) variables")
st.markdown(
    """Below, we have the distribution of all the (dependent) variables you chose in the left sidebar. One data point represents a `(user, task)` pair.

You can also group this data by 'user_id' using the sidebar on the left!
            """
)

for task_var in task_vars:
    this_var = C.task_var_mappings[task_var]
    plot = U.make_df_plot(df, this_var, task_var, plot_color)
    st.plotly_chart(plot)


st.markdown("---")
st.markdown("---")

st.subheader("II. User level variables")
st.markdown(
    """These variables contain user specific information, including their demographics and web search experience"""
)
st.markdown("#### From survey")

for survey_var in survey_vars:
    this_var = C.survey_var_mappings[survey_var]
    plot = U.make_survey_df_plot(user_df, this_var, survey_var, plot_color)
    st.plotly_chart(plot)

st.markdown("#### From Prolific")

for dem_var in dem_vars:
    this_var = C.dem_var_mappings[dem_var]
    plot = U.make_dem_df_plot(user_df, this_var, dem_var, plot_color)
    st.plotly_chart(plot)
