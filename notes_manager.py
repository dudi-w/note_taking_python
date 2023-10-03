from note import Note
import json
from io import open
from multipledispatch import dispatch


class NoteManager:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._note_list_by_title = {}
        self._note_index = {}
        self._free_index = [0]
        self.load_data_from_file()

    def __del__(self):
        self.save_data_to_file()

    def load_data_from_file(self):
        try:
            with open(self._file_path, 'r') as file:
                data = json.load(file)
                for note in data["notes"]:
                    self._note_list_by_title[note["title"]] = Note(
                        note["title"], note["content"])
                    self._note_list_by_title[note["title"]]._id = note["id"]
                    self._note_index[note["id"]] = note["title"]
                self._free_index = data["free_index"]
        except FileNotFoundError:
            print(f"No file found named {self._file_path}")

    def save_data_to_file(self):
        notes = [{"title": note._title, "content": note._content, "id": note._id}
                 for _, note in self._note_list_by_title.items()]
        data = {"notes": notes, "free_index": self._free_index}
        with open(self._file_path, 'w') as file:
            file.write(json.dumps(data, indent=4))

    def ID_assignment(self, note: Note):
        if (len(self._free_index) > 1):
            note._id = self._free_index.pop()
        else:
            note._id = self._free_index[0]
            self._free_index[0] += 1

    def insert(self, note: Note) -> bool:
        if note._title in self._note_list_by_title:
            return False
        self.ID_assignment(note)
        self._note_list_by_title[note._title] = note
        self._note_index[note._id] = note._title
        return True

    @dispatch(int)
    def remove(self, id: int)-> Note: 
        try:
            note = self._note_list_by_title.pop(self._note_index[id])
            self._note_index.pop(id)
            self._free_index.append(id)
            return note
        except KeyError:
            print(f'ERROR: Note with ID = {id} not found.')
            return None

    @dispatch(str)
    def remove(self, title: str)-> Note:
        try:
            note = self._note_list_by_title.pop(title)
            self._note_index.pop(note._id)
            self._free_index.append(note._id)
            return note
        except KeyError:
            print(f'ERROR: Note with title = {title} not found.')
            return None


if __name__ == "__main__":
    note1 = Note("abc8", "efgj")
    note2 = Note("abc6", "efgj")
    note3 = Note("abc32", "efgj")

    nm = NoteManager("notes.json")
    # nm.remove(5)
    nm.insert(note3)
    nm.remove(1)
    nm.remove("abc8")
