"""РК-1. Вариант 14А: CD-диск и библиотека CD-дисков."""


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

    # А1. Все связи один-ко-многим, сортировка по библиотекам.
    result_1 = sorted(
        [(cd.title, library.name)
         for cd in cds
         for library in libraries
         if cd.library_id == library.id],
        key=lambda row: row[1],
    )

    # А2. Суммарная длительность дисков каждой библиотеки.
    result_2 = []
    for library in libraries:
        durations = [
            cd.duration for cd in cds if cd.library_id == library.id
        ]
        result_2.append((library.name, sum(durations)))
    result_2 = sorted(result_2, key=lambda row: row[1], reverse=True)

    # А3. Библиотеки со словом "библиотека" и их диски.
    # Здесь используется только связь многие-ко-многим.
    result_3 = {
        library.name: [
            cd.title for link in links for cd in cds
            if link.library_id == library.id and link.cd_id == cd.id
        ]
        for library in libraries
        if "библиотека" in library.name.lower()
    }

    for title, rows in (
        ("А1. Все диски с сортировкой по библиотекам", result_1),
        ("А2. Библиотеки по суммарной длительности, мин", result_2),
    ):
        print(title)
        for first, second in rows:
            print(f"  {first} | {second}")
        print()

    print('А3. Библиотеки со словом "библиотека" и их диски')
    for library_name, titles in result_3.items():
        print(f"  {library_name} | {'; '.join(titles)}")


if __name__ == "__main__":
    main()
