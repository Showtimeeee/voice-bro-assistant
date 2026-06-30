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

    def notes_count(self, command):
        try:
            return self.notes.count_notes()
        except Exception as e:
            return f"Произошла ошибка: {str(e)}"

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
            dt, text = self.reminders.parse(command)
            if text is None:
                return "Что напомнить?"

            if dt:
                self.reminders.add(text, dt)
                return f"Напоминание установлено на {dt.strftime('%d.%m %H:%M')}: {text}"
            else:
                self.reminders.add(text)
                return f"Напоминание сохранено: {text}"
        except Exception as e:
            return f"Произошла ошибка: {str(e)}"

    def show_reminders(self, command):
        try:
            return self.reminders.show_all()
        except Exception as e:
            return f"Произошла ошибка при отображении напоминаний: {str(e)}"

    def delete_reminder(self, command):
        try:
            words = command.split()
            if 'удалить' in words:
                try:
                    reminder_number = int(words[-1])
                    return self.reminders.delete(reminder_number)
                except:
                    pass
            return "Не указан номер напоминания для удаления"
        except Exception as e:
            return f"Произошла ошибка при удалении напоминания: {str(e)}"
