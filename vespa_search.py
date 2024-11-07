# Install pyvespa if not already installed
# !pip install pyvespa

import pandas as pd
from vespa.application import Vespa
from vespa.io import VespaQueryResponse


def display_hits_as_df(response: VespaQueryResponse, fields) -> pd.DataFrame:
    """
    Converts Vespa search hits into a DataFrame.
    """
    records = []
    for hit in response.hits:
        record = {}
        for field in fields:
            record[field] = hit["fields"].get(field, None)
        records.append(record)
    return pd.DataFrame(records)


def keyword_search(app, search_query):
    """
    Perform a keyword-based search using the bm25 rank profile.
    """
    query = {
        "yql": "select * from sources * where userQuery() limit 5",
        "query": search_query,
        "ranking": "bm25",
    }
    response = app.query(query)
    return display_hits_as_df(response, ["doc_id", "title", "text"])


def semantic_search(app, search_query):
    """
    Perform a semantic search using the 'semantic' rank profile.
    """
    query = {
        "yql": "select * from sources * where ({targetHits:5}nearestNeighbor(embedding,e))",
        "ranking": "semantic",
        "input.query(e)": "embed(@query)"
    }
    response = app.query(query)
    return display_hits_as_df(response, ["doc_id", "title", "text"])


def get_embedding(app, doc_id):
    """
    Retrieve the embedding for a specific document by doc_id.
    """
    query = {
        "yql": f"select doc_id, title, text, embedding from sources * where doc_id contains '{doc_id}'",
        "hits": 1
    }
    result = app.query(query)
    if result.hits:
        return result.hits[0]["fields"].get("embedding")
    return None


def query_by_embedding(app, embedding_vector):
    """
    Perform a recommendation search using the embedding vector as input.
    """
    query = {
        "yql": "select * from sources * where ({targetHits:5}nearestNeighbor(embedding, user_embedding))",
        "ranking.features.query(user_embedding)": str(embedding_vector),
        "ranking.profile": "recommendation"
    }
    response = app.query(query)
    return display_hits_as_df(response, ["doc_id", "title", "text"])


# Initialize Vespa application connection
app = Vespa(url="http://localhost", port=8080)

# keyword search
query_text = "dog food"
df_keyword = keyword_search(app, query_text)
print("Keyword Search Results:")
print(df_keyword.head())

# semantic search
df_semantic = semantic_search(app, query_text)
print("\nSemantic Search Results:")
print(df_semantic.head())

# recommendation search
doc_id = "431727"
embedding = get_embedding(app, doc_id)
if embedding:
    df_recommendation = query_by_embedding(app, embedding)
    print("\nRecommendation Search Results:")
    print(df_recommendation.head())
else:
    print("\nNo embedding found for the specified doc_id.")
