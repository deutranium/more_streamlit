import plotly.express as px

mappings = {
    "cd": {"Icon": "icon", "Number": "number", "Domain": "domain"},
    "cs": {"Low": "low", "High": "high"},
    "sr": {
        "Low": "low_reliability",
        "Original": "original",
        "High": "high_reliability",
    },
    "treatments": {
        "Citation Design": "citation_design",
        "Source Reliability": "source_reliability",
        "Context Stakeness": "context_stakeness",
    },
}


def filter_by_treatments(
    df,
    cd=["Icon", "Number", "Domain"],
    cs=["Low", "High"],
    sr=["Low", "Original", "High"],
):
    cd = [mappings["cd"][i] for i in cd]
    cs = [mappings["cs"][i] for i in cs]
    sr = [mappings["sr"][i] for i in sr]

    df = df[df["citation_design"].isin(cd)]
    df = df[df["context_stakeness"].isin(cs)]
    df = df[df["source_reliability"].isin(sr)]

    return df


def make_df_plot(df, var, name, color):
    if color != "None":
        plt = px.histogram(
            df, x=var, marginal="box", color=mappings["treatments"][color]
        )
    else:
        plt = px.histogram(df, x=var, marginal="box")
    plt.update_layout(xaxis_title=f"{name} ({var})", yaxis_title="Count", title=name)
    return plt


def make_survey_df_plot(df, var, name, color):
    if color in ["Citation Design", "Source Reliability"]:
        plt = px.histogram(
            df, x=var, marginal="box", color=mappings["treatments"][color]
        )
    else:
        plt = px.histogram(df, x=var, marginal="box")
    plt.update_layout(xaxis_title=f"{name} ({var})", yaxis_title="Count", title=name)
    if var in ["s_mental_demand", "s_temporal_demand", "s_effort", "s_frustration"]:
        plt.update_xaxes(
            tickvals=[1, 2, 3, 4, 5],
            ticktext=["Very low", "Low", "Moderate", "High", "Very High"],
        )
    return plt


def make_dem_df_plot(df, var, name, color):
    if color in ["Citation Design", "Source Reliability"]:
        plt = px.histogram(
            df, x=var, marginal="box", color=mappings["treatments"][color]
        )
    else:
        plt = px.histogram(df, x=var, marginal="box")

    plt.update_layout(xaxis_title=f"{name} ({var})", yaxis_title="Count", title=name)
    return plt


def group_things(df, grouping, agg_method):
    df_agg = df.drop(columns=["context_stakeness"], errors="ignore")

    gp = ["participant_id"] if grouping == "User" else None

    num_cols = df.select_dtypes(include=["number", "bool"]).columns.difference(gp)
    keep_first = [
        c for c in ["citation_design", "source_reliability"] if c in df.columns
    ]

    agg_map = {col: agg_method for col in num_cols}
    for c in keep_first:
        agg_map[c] = "first"

    return df_agg.groupby(gp).agg(agg_map).reset_index()
