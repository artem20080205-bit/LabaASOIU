"""Чистые функции запросов варианта В."""


def query_1(cds, libraries):
    """Названия дисков на А и библиотеки: один-ко-многим."""
    return [
        (cd.title, library.name)
        for cd in cds
        for library in libraries
        if cd.library_id == library.id and cd.title.startswith("А")
    ]


def query_2(cds, libraries):
    """Библиотеки по минимальной длительности, по возрастанию."""
    result = []
    for library in libraries:
        durations = [
            cd.duration for cd in cds if cd.library_id == library.id
        ]
        if durations:
            result.append((library.name, min(durations)))
    return sorted(result, key=lambda row: row[1])


def query_3(cds, libraries, links):
    """Все связи многие-ко-многим с сортировкой по дискам."""
    return sorted(
        [
            (cd.title, library.name)
            for link in links
            for cd in cds
            for library in libraries
            if link.cd_id == cd.id and link.library_id == library.id
        ],
        key=lambda row: (row[0], row[1]),
    )
