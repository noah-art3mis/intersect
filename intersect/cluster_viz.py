from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
import altair as alt


def pca_df(df: pd.DataFrame, col: str, n_components: int) -> pd.DataFrame:
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(df[col].tolist())  # type: ignore
    pca_df = pd.DataFrame(
        principal_components, columns=[f"PC{i+1}" for i in range(n_components)]
    )
    return pd.concat([df, pca_df], axis=1)


def add_clusters(df: pd.DataFrame, n_clusters: int, n_components: int) -> pd.DataFrame:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(df[[f"PC{i+1}" for i in range(n_components)]])
    df["Cluster"] = clusters
    return df


def get_chart(df: pd.DataFrame) -> alt.Chart:
    chart = (
        alt.Chart(df)
        .mark_circle(size=100)
        .encode(
            x="PC1:Q",
            y="PC2:Q",
            color="Cluster:N",
            tooltip=alt.Tooltip(
                [
                    "Rank:N",
                    "Title:N",
                    "Delta:Q",
                    "Similarity:Q",
                ],
                # format=".2f", # coerces all fields
            ),
        )
        .properties(width=600, height=400)
    )

    return chart
