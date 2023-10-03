from abc import ABC, abstractmethod
from colorama import Fore
from note import Note
from notes_manager import NoteManager
from commandQueue import CommandQueue
import json


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class CreateNoteCommand(Command):
    def __init__(self, title: str, content: str, noteManager: NoteManager) -> None:
        self._title = title
        self._content = content
        self._noteManager = noteManager

    def execute(self) -> None:
        new_note = Note(self._title, self._content)
        if self._noteManager.insert(new_note):
            print(f"""created a note
            title : {self._title} 
            content : {self._content}
            i.d. : {new_note._id}""")
        else:
            print(Fore.LIGHTYELLOW_EX +
                  f"title = {new_note._title} for a note already exists\nIf you want to delete it please use 'delete'" +
                  Fore.RESET)

    def undo(self) -> None:
        self._noteManager.remove(self._title)

    def to_dict(self) -> dict:
        return {"type": self.__class__.__name__, "title": self._title, "content": self._content}


class ViewNoteCommand(Command):
    map_func = {"int": "view_note_by_id",
                "str": "view_note_by_title"}

    def __init__(self, identifier, noteManager: NoteManager) -> None:
        self._identifier = identifier
        self._noteManager: NoteManager = noteManager

    def execute(self) -> None:
        identifier_type = self._identifier.__class__.__name__
        if identifier_type in ViewNoteCommand.map_func:
            getattr(self, ViewNoteCommand.map_func[identifier_type])(
                self._identifier)
        else:
            print("identifier ERORR")

    def view_note_by_id(self, id: int):
        if id in self._noteManager._note_index:
            note = self._noteManager._note_list_by_title[self._noteManager._note_index[id]]
            print(json.dumps(note.__dict__, indent=4))
        else:
            print(f"ERROR: Note with ID = {id} not found")

    def view_note_by_title(self, title: str):
        if title in self._noteManager._note_list_by_title:
            print(json.dumps(
                self._noteManager._note_list_by_title[title].__dict__, indent=4))
        else:
            print(f"ERROR: Note with title = {title} not found")

    def undo(self) -> None:
        pass

    def to_dict(self) -> dict:
        return {"type": self.__class__.__name__, "identifier": self._identifier}


class DeleteNoteCommand(Command):
    def __init__(self, identifier, noteManager: NoteManager) -> None:
        self._identifier = identifier
        self._noteManager: NoteManager = noteManager
        self._note = None

    def execute(self) -> None:
        self._note = self._noteManager.remove(self._identifier)
        # if note

    def undo(self) -> None:
        if self._note:
            CreateNoteCommand(self._note._title,
                              self._note._content, self._noteManager).execute()
        else:
            pass  # todo

    def to_dict(self) -> dict:
        return {"type": self.__class__.__name__, "identifier": self._identifier}


class UndoLestCommand(Command):
    def __init__(self, commandQueue: CommandQueue) -> None:
        self._CommandQueue: CommandQueue = commandQueue

    def execute(self) -> None:
        self._CommandQueue.dequeue()

    def undo(self) -> None:
        self._CommandQueue.dequeue()

    def to_dict(self) -> dict:
        return {"type": self.__class__.__name__}


if __name__ == "__main__":
    nm = NoteManager("notes.json")
    cm = ViewNoteCommand("dwcs", nm)
    cm.execute()
