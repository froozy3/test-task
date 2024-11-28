import httpx
from fastapi import HTTPException

CAT_API_URL = "https://api.thecatapi.com/v1/breeds"


def validate_beer(breed: str) -> bool:
    try:
        response = httpx.get(CAT_API_URL)
        response.raise_for_status()
        breeds = response.json()

        for breed_data in breeds:
            if breed_data['name'].upper() == breed.strip().upper():
                return True
        return False
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Error connecting to the TheCatAPI: {e}")
