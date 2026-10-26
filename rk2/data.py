"""Те же демонстрационные данные, что и в РК-1."""

from models import CD, Library, CDLibrary


def sample_data():
    libraries = [
        Library(1, "Городская библиотека CD"),
        Library(2, "Архивная библиотека CD"),
        Library(3, "Фонотека"),
    ]
    cds = [
        CD(1, "Акустика", 42, 3),
        CD(2, "Рок", 55, 1),
        CD(3, "Джаз", 48, 2),
        CD(4, "Классика", 64, 1),
        CD(5, "Атмосфера", 36, 2),
    ]
    links = [
        CDLibrary(1, 1), CDLibrary(1, 3),
        CDLibrary(2, 1), CDLibrary(2, 2),
        CDLibrary(3, 2), CDLibrary(4, 3),
        CDLibrary(5, 1),
    ]
    return cds, libraries, links
