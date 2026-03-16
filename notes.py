import os


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
            with open('notes.txt', 'w', encoding='utf-8') as f:
                for note in self.notes:
                    f.write(note + '\n')
        except Exception as e:
            print(f"Ошибка сохранения заметок: {e}")

    def load_notes(self):
        try:
            if os.path.exists('notes.txt'):
                with open('notes.txt', 'r', encoding='utf-8') as f:
                    self.notes = [line.strip() for line in f.readlines()]
        except Exception as e:
            print(f"Ошибка загрузки заметок: {e}")


# reminders.py
class ReminderManager:
    def __init__(self):
        self.reminders = []
        self.load_reminders()

    def add_reminder(self, text):
        if not text:
            return "Не указан текст напоминания"
        self.reminders.append(text)
        self.save_reminders()
        return "Напоминание добавлено"

    def show_reminders(self):
        if not self.reminders:
            return "Напоминаний нет"
        reminders_list = "\n".join([f"{i+1}. {reminder}" for i, reminder in enumerate(self.reminders)])
        return f"Ваши напоминания:\n{reminders_list}"

    def delete_reminder(self, index):
        try:
            index = int(index) - 1
            if 0 <= index < len(self.reminders):
                removed_reminder = self.reminders.pop(index)
                self.save_reminders()
                return f"Напоминание удалено: {removed_reminder}"
            return "Неверный номер напоминания"
        except:
            return "Ошибка при удалении напоминания"

    def save_reminders(self):
        try:
            with open('reminders.txt', 'w', encoding='utf-8') as f:
                for reminder in self.reminders:
                    f.write(reminder + '\n')
        except Exception as e:
            print(f"Ошибка сохранения напоминаний: {e}")

    def load_reminders(self):
        try:
            if os.path.exists('reminders.txt'):
                with open('reminders.txt', 'r', encoding='utf-8') as f:
                    self.reminders = [line.strip() for line in f.readlines()]
        except Exception as e:
            print(f"Ошибка загрузки напоминаний: {e}")
