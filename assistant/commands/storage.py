class StorageCommands:
    def add_note(self, command):
        try:
            text = command.replace("запиши", "").replace("заметка", "").strip()
            if not text:
                return "Пожалуйста, укажите текст заметки"
            self.notes.add_note(text)
            return f"Заметка успешно добавлена: {text}"
        except Exception as e:
            return f"Произошла ошибка при добавлении заметки: {str(e)}"

    def show_notes(self, command):
        try:
            return self.notes.show_notes()
        except Exception as e:
            return f"Произошла ошибка при отображении заметок: {str(e)}"

    def delete_note(self, command):
        try:
            words = command.split()
            if 'удалить' in words:
                try:
                    note_number = int(words[-1])
                    return self.notes.delete_note(note_number)
                except:
                    pass
            return "Не указан номер заметки для удаления"
        except Exception as e:
            return f"Произошла ошибка при удалении заметки: {str(e)}"

    def set_reminder(self, command):
        try:
            text = command.replace("напомни", "").strip()
            if not text:
                return "Пожалуйста, укажите текст напоминания"
            self.reminders.add_reminder(text)
            return f"Напоминание установлено: {text}"
        except Exception as e:
            return f"Произошла ошибка при установке напоминания: {str(e)}"

    def show_reminders(self, command):
        try:
            return self.reminders.show_reminders()
        except Exception as e:
            return f"Произошла ошибка при отображении напоминаний: {str(e)}"

    def delete_reminder(self, command):
        try:
            words = command.split()
            if 'удалить' in words:
                try:
                    reminder_number = int(words[-1])
                    return self.reminders.delete_reminder(reminder_number)
                except:
                    pass
            return "Не указан номер напоминания для удаления"
        except Exception as e:
            return f"Произошла ошибка при удалении напоминания: {str(e)}"
