from pydantic import BaseModel


class MetaData(BaseModel):
    filename: str
    sheet_name: str | None = None


class Document(BaseModel):
    content: str
    metadata: MetaData
