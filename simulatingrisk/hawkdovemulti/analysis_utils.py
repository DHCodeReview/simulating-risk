"""
utility methods for analyzing data collected generated by this model
"""
import altair as alt
import polars as pl

from simulatingrisk.hawkdovemulti.model import RiskState


def groupby_population_risk_category(df):
    """takes a polars dataframe populated with model data generated
    by hawk/dove multi model, groups by population risk category and
    adds group labels."""
    # currently written for polars dataframe

    # group on risk category to get totals for the  number of runs that
    # ended up in each different type
    poprisk_grouped = df.group_by("population_risk_category").agg(pl.col("RunId").sum())
    poprisk_grouped = poprisk_grouped.rename(
        {"population_risk_category": "risk_category", "RunId": "count"}
    )
    poprisk_grouped = poprisk_grouped.sort("risk_category")

    # add column with readable group labels for the numeric categories
    poprisk_grouped = poprisk_grouped.with_columns(
        pl.Series(
            name="type",
            values=poprisk_grouped["risk_category"].map_elements(RiskState.category),
        )
    )
    return poprisk_grouped


def graph_population_risk_category(poprisk_grouped):
    """given a dataframe grouped by :meth:`groupby_population_risk_category`,
    generate an altair chart graphing the number of runs in each type,
    grouped and labeled by the larger categories."""
    return (
        alt.Chart(poprisk_grouped)
        .mark_bar(width=15)
        .encode(
            x=alt.X(
                "risk_category",
                title="risk category",
                axis=alt.Axis(tickCount=13),  # 13 categories
                scale=alt.Scale(domain=[1, 13]),
            ),
            y=alt.Y("count", title="Number of runs"),
            color=alt.Color("type", title="type"),
        )
        .properties(title="Distribution of runs by final population risk category")
    )
