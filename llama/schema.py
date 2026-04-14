from pydantic import BaseModel, Field

class OpenAIREsponse(BaseModel):
    result:str = Field(dscription="최종 답변")
    confidence: float = Field(description="0~1 사이의 신뢰도")
