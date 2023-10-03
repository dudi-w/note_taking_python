# from command import Command
from io import open
import json


class CommandQueue:
    def __init__(self, file_path: str) -> None:
        self._stack = []
        self._file_path = file_path

    def __del__(self):
        self.save_data_to_file()

    def save_data_to_file(self):
        data = []
        try:
            with open(self._file_path, 'r') as file:
                data = json.load(file)
        except Exception:
            print(f"No file found named {self._file_path}")

        commands = [command.to_dict() for command in self._stack]
        with open(self._file_path, 'w') as file:
            listJoin = data + commands
            file.write(json.dumps(listJoin, indent=4))

    def inqueue(self, command) -> None:
        command.execute()
        self._stack.append(command)

    def dequeue(self) -> None:
        if (self._stack):
            command = self._stack.pop()
            command.undo()
        else:
            print("ERROR")  # todo masssege


# if __name__ == "__main__":
#     nm = NoteManager("notes.json")
#     command_queue = CommandQueue("commands.json")
#     comm = CreateNoteCommand("test", "wdcasfcac", nm)
#     command_queue.inqueue(comm)
