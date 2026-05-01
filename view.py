from nicegui import ui
from database import get_session
from verb_dao import VerbDAO 
from models import Verb
def show_menu():
    ui.label("Меню:")
    ui.button("1.Показать все глаголы", on_click=show_verbs)
    ui.button("2.Добавить глагол", on_click=add_verb)
    ui.button("3.Редактировать глагол", on_click=edit_verb)
    ui.button("4.Удалить глагол", on_click=delete_verb)   
    ui.button("0.Выход", on_click=stop_app)
from nicegui import ui

def stop_app():
    ui.notify("Приложение закрывается")
    ui.run_javascript('window.close()')

def add_verb():
    with get_session() as session:
        verb_dao = VerbDAO(session)

        infinitive = ui.input("Infinitive")
        past_simple = ui.input("Past Simple")
        past_participle = ui.input("Past Participle")
        translation = ui.input("Translation")

        def save():
            verb_dao.create_verb(
                infinitive.value,
                past_simple.value,
                past_participle.value,
                translation.value
            )
            ui.notify("Глагол добавлен!")

        ui.button("Сохранить", on_click=save)

def edit_verb():
    with get_session() as session:
        verb_dao = VerbDAO(session)
        verb_id = int(ui.input("Введите ID глагола для редактирования").value)
        verb = verb_dao.get_verb_by_id(verb_id)
        if verb:
            infinitive = ui.input(f"Infinitive [{verb.infinitive}]").value or verb.infinitive
            past_simple = ui.input(f"Past Simple [{verb.past_simple}]").value or verb.past_simple
            past_participle = ui.input(f"Past Participle [{verb.past_participle}]").value or verb.past_participle
            translation = ui.input(f"Translation [{verb.translation}]").value or verb.translation
            verb_dao.update_verb(verb_id, infinitive=infinitive, past_simple=past_simple, past_participle=past_participle, translation=translation)
            ui.notify("Глагол обновлён!")
        else:
            ui.notify("Глагол с таким ID не найден.")

def delete_verb():
    with get_session() as session:
        verb_dao = VerbDAO(session)
        verb_id = int(ui.input("Введите ID глагола для удаления").value)
        success = verb_dao.delete_verb(verb_id)
        if success:
            ui.notify("Глагол удалён!")
        else:
            ui.notify("Глагол с таким ID не найден.")
    
    

table = None  # глобальная переменная

def show_verbs():
    global table

    with get_session() as session:
        verb_dao = VerbDAO(session)
        verbs = verb_dao.get_all_verbs()

        columns = [
            {'name': 'id', 'label': 'ID', 'field': 'id'},
            {'name': 'infinitive', 'label': 'Infinitive', 'field': 'infinitive'},
            {'name': 'past_simple', 'label': 'Past Simple', 'field': 'past_simple'},
            {'name': 'past_participle', 'label': 'Past Participle', 'field': 'past_participle'},
            {'name': 'translation', 'label': 'Translation', 'field': 'translation'},
        ]

        rows = [
            {
                'id': v.id,
                'infinitive': v.infinitive,
                'past_simple': v.past_simple,
                'past_participle': v.past_participle,
                'translation': v.translation,
            }
            for v in verbs
        ]

    
        if table:
            table.rows = rows
        else:
            table = ui.table(columns=columns, rows=rows).classes('w-full')


     # Explicitly export the function
__all__ = ['show_verbs']
