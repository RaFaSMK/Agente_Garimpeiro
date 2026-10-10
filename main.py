from fastapi import FastAPI
from pydantic import BaseModel
import json
from ollama import chat


class MotorcycleAd(BaseModel):
    model: str
    year: int
    price: float
    is_sleeper_project: bool
    condition: str


app = FastAPI()
url = "/api/v1"


@app.post(f"{url}/extract-ad")
def createBike(ad_text: str):
    response = chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": """Você é um assistente especialista em extração de dados. 
                              Analise o texto e extraia as informações estritamente no formato JSON.
                              Chaves obrigatórias: "model" (str), "year" (int), "price" (float), 
                              "is_sleeper_project" (bool), "condition" (str).""",
            },
            {"role": "user", "content": ad_text},
        ],
        format="json",
    )

    final_response = response.message.content

    extracted_data = json.loads(final_response)

    official_ad = MotorcycleAd(**extracted_data)

    return official_ad
