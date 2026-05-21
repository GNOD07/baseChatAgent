from pydantic import BaseModel

class ResponseFormat(BaseModel):
    punny_response: str
    weather_condition: str | None = None