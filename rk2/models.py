"""Классы данных из РК-1 без консольного ввода и вывода."""


class CD:
    def __init__(self, id, title, duration, library_id):
        self.id = id
        self.title = title
        self.duration = duration
        self.library_id = library_id


class Library:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class CDLibrary:
    def __init__(self, cd_id, library_id):
        self.cd_id = cd_id
        self.library_id = library_id
