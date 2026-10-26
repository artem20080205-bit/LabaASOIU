"""Консольная оболочка рефакторинга РК-1, вариант 14В."""

from data import sample_data
from queries import query_1, query_2, query_3


def main():
    cds, libraries, links = sample_data()
    results = (
        ("В1. Диски с названием на А и их библиотеки",
         query_1(cds, libraries)),
        ("В2. Библиотеки по минимальной длительности, мин",
         query_2(cds, libraries)),
        ("В3. Все связи с сортировкой по названиям дисков",
         query_3(cds, libraries, links)),
    )
    for title, rows in results:
        print(title)
        for first, second in rows:
            print(f"  {first} | {second}")
        print()


if __name__ == "__main__":
    main()
