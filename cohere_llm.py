import cohere
import json
import pandas as pd
import numpy as np
import weaviate
from weaviate.util import generate_uuid5


client = weaviate.Client(
    url="http://localhost:8080",
    additional_headers={"X-Cohere-Api-Key": "COHERE-API-KEY"},
)


def read_json_file():
    filename = "history_text.json"
    df = pd.read_json(filename)
    return df


def weaviate_create_schema():
    schema = {
        "class": "HistoryText",
        "description": "Contains the paragraphs of text along with their embeddings",
        "vectorizer": "text2vec-cohere",
        "properties": [
            {
                "name": "content",
                "dataType": ["text"],
            }
        ],
        "moduleConfig": {
            "text2vec-cohere": {"model": "embed-english-light-v2.0"},
            "generative-cohere": {"model": "command-nightly"},
        },
    }
    client.schema.create_class(schema)
    print("Schema created successfully")


def weaviate_add_data(df):
    client.batch.configure(batch_size=10)
    with client.batch as batch:
        for index, row in df.iterrows():
            text = row["text"]
            batch_data = {"content": text}
            batch.add_data_object(
                data_object=batch_data,
                class_name="HistoryText",
                uuid=generate_uuid5(batch_data),
            )

    print("Data Added!")


def semantic_search():
    result = (
        client.query.get("HistoryText", ["content"])
        .with_additional(["id", "vector"])
        .with_limit(2)
        .do()
    )
    output = []
    closest_paragraphs = result.get("data").get("Get").get("HistoryText")
    for p in closest_paragraphs:
        output.append(p.get("content"))

    return output


def generative_ai(input_text, k_vectors):
    result = (
        client.query.get("HistoryText", ["content"])
        .with_near_text({"concepts": [input_text]})
        .with_limit(k_vectors)
        .with_generate(single_prompt="Generate a sentence related to {concepts}")
        .do()
    )
    output = []
    closest_paragraphs = result.get("data").get("Get").get("HistoryText")
    for p in closest_paragraphs:
        output.append(p.get("content"))

    return output


if __name__ == "__main__":
    # dataframe = read_json_file()
    # weaviate_create_schema()
    # weaviate_add_data(dataframe)

    input_text = "Hitler"
    k_vectors = 1

    # content = semantic_search()
    # print(json.dumps(content))

    generated = generative_ai(input_text, k_vectors)
    print(json.dumps(generated))
