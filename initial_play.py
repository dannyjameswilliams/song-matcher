

from keys import weaviate_key, weaviate_url, openai_key


# connecting
import weaviate
import weaviate.classes as wvc
import os

import requests
import json

client = weaviate.connect_to_weaviate_cloud(
    cluster_url = weaviate_url,
    auth_credentials=weaviate.auth.AuthApiKey(weaviate_key),
    headers={
        "X-OpenAI-Api-Key": openai_key  # Replace with your inference API key
    }
)

try:  

    print(f"Client ready?: {client.is_ready()}")

    if not client.collections.exists("Question"):
        questions = client.collections.create(
            name="Question",
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
            generative_config=wvc.config.Configure.Generative.openai()  # Ensure the `generative-openai` module is used for generative queries
        )

    resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
    data = json.loads(resp.text)  # Load data

    question_objs = list()
    for i, d in enumerate(data):
        question_objs.append({
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        })

    questions = client.collections.get("Question")
    questions.data.insert_many(question_objs)

    response = questions.query.near_text(
        query="biology",
        limit=2
    )

    print(response.objects[0].properties)


finally:
    client.close()