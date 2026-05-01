from sqlmodel import Session, select
from models import Verb

class VerbDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_verb(self, infinitive: str, past_simple: str, past_participle: str, translation: str) -> Verb:
        verb = Verb(
            infinitive=infinitive,
            past_simple=past_simple,
            past_participle=past_participle,
            translation=translation
        )
        self.session.add(verb)
        self.session.commit()
        self.session.refresh(verb)
        return verb

    def get_all_verbs(self) -> list[Verb]:
        return self.session.exec(select(Verb)).all()

    def get_verb_by_id(self, verb_id: int) -> Verb | None:
        return self.session.get(Verb, verb_id)

    def update_verb(self, verb_id: int, **kwargs) -> Verb | None:
        verb = self.get_verb_by_id(verb_id)
        if not verb:
            return None
        for key, value in kwargs.items():
            setattr(verb, key, value)
        self.session.commit()
        self.session.refresh(verb)
        return verb

    def delete_verb(self, verb_id: int) -> bool:
        verb = self.get_verb_by_id(verb_id)
        if not verb:
            return False
        self.session.delete(verb)
        self.session.commit()
        return True