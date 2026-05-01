from sqlmodel import Field, SQLModel
class Verb(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    infinitive: str
    past_simple: str
    past_participle: str
    translation: str