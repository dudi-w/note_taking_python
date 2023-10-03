from commandQueue import CommandQueue
from notes_manager import NoteManager
from commaddFactory import CommaddFactory 

def main():
    cm = CommandQueue("commands.json")
    nm = NoteManager("notes.json")
    factory = CommaddFactory(cm, nm)
    while (True):
        user_request = input("Enter your command\n").split()
        if user_request[0] == "exit":
            break
        command = factory.concrete_command(user_request)
        if command:
            cm.inqueue(command)


if __name__ == "__main__":
    main()
