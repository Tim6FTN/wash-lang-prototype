

class OpenStatement:
    def __init__(self, parent):
        self.parent = parent


class OpenURLStatement(OpenStatement):
    def __init__(self, parent, url):
        super().__init__(parent)
        self.url = url


class OpenFileStatement(OpenStatement):
    def __init__(self, parent, file_path):
        super().__init__(parent)
        self.file_path = file_path


class OpenStringStatement(OpenStatement):
    def __init__(self, parent, html):
        super().__init__(parent)
        self.html = html


wash_classes = [
    OpenURLStatement, OpenFileStatement, OpenStringStatement
]