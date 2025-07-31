import streamlit as st
import pandas as pd
from utils.utils import add_you

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
import altair as alt


def pca_df(df: pd.DataFrame, col: str, n_components: int) -> pd.DataFrame:
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(df[col].tolist())  # type: ignore
    pca_df = pd.DataFrame(
        principal_components, columns=[f"PC{i+1}" for i in range(n_components)] # type: ignore
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
                    "title:N",
                    "days_ago:Q",
                    "score_semantic:Q",
                    "description:N",
                ],
                # format=".2f", # coerces all fields
            ),
        )
        .properties(width=600, height=400)
    )

    return chart



def render_cluster_visualization(df: pd.DataFrame, input_text: str, input_embedding: list[float]) -> None:
    """Render cluster visualization with PCA"""
    st.write("### Cluster Visualization (KMeans + PCA)")
    with st.spinner():
        st.write("Select tabs for different clustering")
        st.write("Hover over items to see more details")

        df_without_you = df.copy()
        df_you = add_you(df_without_you, input_text, input_embedding)  # type: ignore
        df_pca = pca_df(df_you, "embedding", n_components=2)

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["No clusters", "2 clusters", "3 clusters", "4 clusters", "5 clusters"]
        )

        def generate_chart(_df, n_clusters):
            _df = add_clusters(df_pca, n_clusters, n_components=2)
            _df.loc[_df["title"] == "Your text", "Cluster"] = " You"
            chart = get_chart(_df)
            st.altair_chart(chart, use_container_width=True)

        with tab1:
            generate_chart(df_pca, 1)
        with tab2:
            generate_chart(df_pca, 2)
        with tab3:
            generate_chart(df_pca, 3)
        with tab4:
            generate_chart(df_pca, 4)
        with tab5:
            generate_chart(df_pca, 5) 