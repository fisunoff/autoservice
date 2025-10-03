import pydantic


class WikiBaseData(pydantic.BaseModel):
    brands: list[str]
    syndrome: str
    solution: str


class WikiData(WikiBaseData):
    id: int
