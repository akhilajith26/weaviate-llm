import weaviate
import cohere
import json


client = weaviate.Client(
    url="http://localhost:8080",
    additional_headers={"X-Cohere-Api-Key": "xUTO6837g2n7XptN7tuTqKG8AU18viEgiwtHPHOu"},
)

# delete class
# client.schema.delete_class("HistoryText")

# Check data
# print(client.query.aggregate("HistoryText").with_meta_count().do())


# query

# semantic search
# res = (
#     client.query.get("HistoryText", ["content"])
#     .with_additional(["id", "vector"])
#     .with_limit(2)
#     .do()
# )
# print(json.dumps(res))

# generative
# res = (
#     client.query.get("HistoryText", ["content"])
#     .with_near_text({"concepts": ["world war"]})
#     .with_limit(1)
#     .with_generate(
#         single_prompt="Generate a question to which the answer is {concepts}"
#     )
#     .do()
# )
# print(json.dumps(res))
