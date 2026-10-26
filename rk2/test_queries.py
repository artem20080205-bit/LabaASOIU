"""Три модульных теста: по одному на каждый запрос."""

import unittest
from models import CD, Library, CDLibrary
from queries import query_1, query_2, query_3


class QueryTests(unittest.TestCase):
    def setUp(self):
        # Данные отличаются от демонстрации РК-1.
        self.libraries = [
            Library(1, "Библиотека 1"),
            Library(2, "Библиотека 2"),
            Library(3, "Пустая библиотека"),
        ]
        self.cds = [
            CD(1, "Рок", 70, 1),
            CD(2, "Альбом", 40, 2),
            CD(3, "Джаз", 30, 1),
            CD(4, "Акустика", 50, 2),
        ]
        self.links = [
            CDLibrary(1, 2), CDLibrary(2, 1),
            CDLibrary(2, 2), CDLibrary(3, 1),
        ]

    def test_query_1(self):
        expected = [
            ("Альбом", "Библиотека 2"),
            ("Акустика", "Библиотека 2"),
        ]
        self.assertEqual(query_1(self.cds, self.libraries), expected)
        self.assertEqual(query_1([], self.libraries), [])
        self.assertEqual(query_1(self.cds, []), [])

    def test_query_2(self):
        # Минимум отличается от среднего, максимума и суммы.
        expected = [("Библиотека 1", 30), ("Библиотека 2", 40)]
        self.assertEqual(query_2(self.cds, self.libraries), expected)
        self.assertEqual(query_2([], self.libraries), [])
        self.assertEqual(query_2(self.cds, []), [])

    def test_query_3(self):
        expected = [
            ("Альбом", "Библиотека 1"),
            ("Альбом", "Библиотека 2"),
            ("Джаз", "Библиотека 1"),
            ("Рок", "Библиотека 2"),
        ]
        self.assertEqual(
            query_3(self.cds, self.libraries, self.links), expected
        )
        self.assertEqual(query_3(self.cds, self.libraries, []), [])
        self.assertEqual(query_3([], self.libraries, self.links), [])


if __name__ == "__main__":
    unittest.main()
