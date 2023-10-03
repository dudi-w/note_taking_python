from commandQueue import CommandQueue
import command
from notes_manager import NoteManager

class CommaddFactory():

    def __init__(self, commandQueue:CommandQueue, noteManager:NoteManager) -> None:
        self._commandQueue =commandQueue
        self._noteManager = noteManager

    def concrete_command(self, user_request:list)->command.Command | None:
        if user_request[0] == "create":
            try:
                title_index = user_request.index("-t")
                content_index = user_request.index("-c")
                return command.CreateNoteCommand(" ".join(user_request[title_index+1:content_index]), " ".join(user_request[content_index+1:]),self._noteManager)
            except ValueError:
                print("ERROR Please use the following format\ncreate -t <title> -c <content>")
        
        elif user_request[0] == "delete":
            if "-id" in user_request:
                identifier = user_request.index("-id")+1
                return command.DeleteNoteCommand(identifier ,self._noteManager)
            elif "-t" in user_request:
                identifier = " ".join(user_request[user_request.index("-t")+1:])
                return command.DeleteNoteCommand(identifier ,self._noteManager)
            else:
                print("ERROR Please use the following format\ndelete -t <title> \nor \ndelete -c <content>")

        elif user_request[0] == "view":
            if "-id" in user_request:
                identifier = user_request[user_request.index("-id")+1]
                return command.ViewNoteCommand(int(identifier) ,self._noteManager)
            elif "-t" in user_request:
                identifier = " ".join(user_request[user_request.index("-t")+1:])
                return command.ViewNoteCommand(identifier ,self._noteManager)
            else:
                print("ERROR Please use the following format\nview -t <title> \nor \ndelete -c <content>")

        elif user_request[0] == "undo":
            return command.UndoLestCommand(self._commandQueue)
        else:
            print("""Please use the following formats
                  create -t <title> -c <content>
                  delete 
                    -t <title>
                    -c <content>
                  view 
                    -t <title>
                    -c <content>
                  undo
                  """)
        return None


    
