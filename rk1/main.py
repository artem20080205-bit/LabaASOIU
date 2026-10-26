"""РК-1. Вариант 14В: CD-диск и библиотека CD-дисков."""


class CD:
    def __init__(self, id, title, duration, library_id):
        self.id = id
        self.title = title
        self.duration = duration  # Длительность в минутах.
        self.library_id = library_id


class Library:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class CDLibrary:
    """Промежуточный класс для связи многие-ко-многим."""

    def __init__(self, cd_id, library_id):
        self.cd_id = cd_id
        self.library_id = library_id


def main():
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

    # В1. Связь один-ко-многим, название диска начинается на А.
    result_1 = [
        (cd.title, library.name)
        for cd in cds
        for library in libraries
        if cd.library_id == library.id and cd.title.startswith("А")
    ]

    # В2. Минимальная длительность в каждой непустой библиотеке.
    result_2 = []
    for library in libraries:
        durations = [
            cd.duration for cd in cds if cd.library_id == library.id
        ]
        if durations:
            result_2.append((library.name, min(durations)))
    result_2 = sorted(result_2, key=lambda row: row[1])

    # В3. Связь многие-ко-многим, сортировка по названиям дисков.
    result_3 = sorted(
        [
            (cd.title, library.name)
            for link in links
            for cd in cds
            for library in libraries
            if link.cd_id == cd.id and link.library_id == library.id
        ],
        key=lambda row: (row[0], row[1]),
    )

    for title, rows in (
        ("В1. Диски с названием на А и их библиотеки", result_1),
        ("В2. Библиотеки по минимальной длительности, мин", result_2),
        ("В3. Все связи с сортировкой по названиям дисков", result_3),
    ):
        print(title)
        for first, second in rows:
            print(f"  {first} | {second}")
        print()


if __name__ == "__main__":
    main()
