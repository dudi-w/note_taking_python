class Note:
    def __init__(self, title: str, content: str) -> None:
        self._title = title
        self._content = content
        self._id = None

    def __str__(self):
        return self._title + " " + self._content + str(self._id)


if __name__ == "__main__":
    n = Note("dcwcs", "wcwc")
    print(n._title)
    print(n.__dict__)
    
