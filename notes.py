class NotesManager:
    def __init__(self):
        self.notes = []

    def add_note(self, text):
        self.notes.append(text)
        return "Заметка добавлена"

    def show_notes(self):
        if not self.notes:
            return "Заметок нет"
        return "\n".join([f"{i+1}. {note}" for i, note in enumerate(self.notes)])
