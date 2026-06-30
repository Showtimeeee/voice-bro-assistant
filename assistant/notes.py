import os
from . import config


class NotesManager:
    def __init__(self):
        self.notes = []
        self.load_notes()  # Загружаем сохраненные заметки

    def add_note(self, text):
        if not text:
            return "Не указан текст заметки"
        self.notes.append(text)
        self.save_notes()
        return "Заметка добавлена"

    def count_notes(self):
        count = len(self.notes)
        if count == 0:
            return "У вас нет заметок"
        if count == 1:
            return "У вас 1 заметка"
        return f"У вас {count} заметок"

    def show_notes(self):
        if not self.notes:
            return "Заметок нет"
        notes_list = "\n".join([f"{i+1}. {note}" for i, note in enumerate(self.notes)])
        return f"Ваши заметки:\n{notes_list}"

    def delete_note(self, index):
        try:
            index = int(index) - 1
            if 0 <= index < len(self.notes):
                removed_note = self.notes.pop(index)
                self.save_notes()
                return f"Заметка удалена: {removed_note}"
            return "Неверный номер заметки"
        except:
            return "Ошибка при удалении заметки"

    def save_notes(self):
        try:
            path = config.FILE_PATHS['notes']
            with open(path, 'w', encoding='utf-8') as f:
                for note in self.notes:
                    f.write(note + '\n')
        except Exception as e:
            print(f"Ошибка сохранения заметок: {e}")

    def load_notes(self):
        try:
            path = config.FILE_PATHS['notes']
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    self.notes = [line.strip() for line in f.readlines()]
        except Exception as e:
            print(f"Ошибка загрузки заметок: {e}")
