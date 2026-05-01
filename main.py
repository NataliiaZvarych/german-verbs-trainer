from database import create_db_and_tables, engine
from models import Verb
from sqlmodel import Session
from verb_dao import VerbDAO

from nicegui import ui

def start_web():
    from view import show_menu
    show_menu()
    ui.run(title="German Verbs Trainer", port=8000)

def main():
    create_db_and_tables()
    with Session(engine) as session:
        verb_dao = VerbDAO(session)
        while True:
            print("\nМеню:")
            print("1. Добавить глагол")
            print("2. Показать все глаголы")
            print("3. Удалить глагол")
            print("4. Редактировать глагол")
            print("0. Выйти")
            choice = input("Выберите действие: ")
            if choice == "1":
                print("\nДобавление нового глагола:")
                infinitive = input("Infinitive: ")
                past_simple = input("Past Simple: ")
                past_participle = input("Past Participle: ")
                translation = input("Translation: ")
                new_verb = verb_dao.create_verb(infinitive, past_simple, past_participle, translation)
                print(f"Создан глагол: {new_verb}")
            elif choice == "2":
                all_verbs = verb_dao.get_all_verbs()
                print("\nВсе глаголы:")
                header = f"{'ID':<4} {'Infinitive':<15} {'Past Simple':<15} {'Past Participle':<18} {'Translation':<20}"
                print(header)
                print('-' * len(header))
                for verb in all_verbs:
                    print(f"{verb.id:<4} {verb.infinitive:<15} {verb.past_simple:<15} {verb.past_participle:<18} {verb.translation:<20}")
            elif choice == "3":
                verb_id = input("Введите ID глагола для удаления: ")
                if verb_id.isdigit():
                    success = verb_dao.delete_verb(int(verb_id))
                    if success:
                        print("Глагол удалён.")
                    else:
                        print("Глагол с таким ID не найден.")
                else:
                    print("Некорректный ID.")
            elif choice == "4":
                verb_id = input("Введите ID глагола для редактирования: ")
                if verb_id.isdigit():
                    verb = verb_dao.get_verb_by_id(int(verb_id))
                    if verb:
                        print(f"Текущий: {verb.infinitive}, {verb.past_simple}, {verb.past_participle}, {verb.translation}")
                        infinitive = input(f"Infinitive [{verb.infinitive}]: ") or verb.infinitive
                        past_simple = input(f"Past Simple [{verb.past_simple}]: ") or verb.past_simple
                        past_participle = input(f"Past Participle [{verb.past_participle}]: ") or verb.past_participle
                        translation = input(f"Translation [{verb.translation}]: ") or verb.translation
                        updated = verb_dao.update_verb(int(verb_id),
                            infinitive=infinitive,
                            past_simple=past_simple,
                            past_participle=past_participle,
                            translation=translation)
                        print("Глагол обновлён.")
                    else:
                        print("Глагол с таким ID не найден.")
                else:
                    print("Некорректный ID.")
            elif choice == "0":
                print("Выход.")
                break
            else:
                print("Некорректный выбор. Попробуйте снова.")


if __name__ in {"__main__", "__mp_main__"}:
    mode = input("Выберите режим: 1 — консоль, 2 — веб-интерфейс: ")
    if mode == "2":
        start_web()
    else:
        main()