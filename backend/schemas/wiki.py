import pydantic


class WikiBaseData(pydantic.BaseModel):
    brands: list[str]
    syndrome: str
    solution: str
    components: list[str] | None = pydantic.Field(default_factory=list)


class WikiData(WikiBaseData):
    id: int
