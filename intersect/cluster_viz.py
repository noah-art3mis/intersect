from sklearn.decomposition import PCA
import pandas as pd
import altair as alt


def pca_df(df: pd.DataFrame, col) -> pd.DataFrame:
    n_components = 2
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(df[col].tolist())
    return pd.DataFrame(
        principal_components, columns=[f"PC{i+1}" for i in range(n_components)]
    )


def get_chart(df: pd.DataFrame) -> alt.Chart:

    chart = (
        alt.Chart(df)
        .mark_circle(size=100)
        .encode(
            x="PC1:Q",
            y="PC2:Q",
            color=alt.value("steelblue"),
        )
        .properties(width=600, height=400)
    )

    return chart
