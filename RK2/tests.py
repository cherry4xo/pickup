import unittest
from main import Book, Bookstore, get_one_to_many, get_avg_price_per_store, get_books_in_a_stores

class TestRefactoredCode(unittest.TestCase):
    def setUp(self):
        self.bookstores = [
            Bookstore(1, "Академическая литература"),
            Bookstore(2, "Книжный мир"),
            Bookstore(3, "Азбука знаний"),
            Bookstore(4, "Библиотека мира"),
        ]

        self.books = [
            Book(1, "Философия науки", 500, 1),
            Book(2, "Математика для всех", 400, 1),
            Book(3, "История России", 700, 2),
            Book(4, "Алгебра и анализ", 450, 2),
            Book(5, "Биология", 550, 3),
        ]

    def test_one_to_many_relationship(self):
        expected = [
            ("Философия науки", 500, "Академическая литература"),
            ("Математика для всех", 400, "Академическая литература"),
            ("История России", 700, "Книжный мир"),
            ("Алгебра и анализ", 450, "Книжный мир"),
            ("Биология", 550, "Азбука знаний"),
        ]
        result = get_one_to_many(self.books, self.bookstores)
        self.assertEqual(result, expected)

    def test_avg_price_per_store(self):
        expected = [
            ("Академическая литература", 450.0),
            ("Азбука знаний", 550.0),
            ("Книжный мир", 575.0),
        ]
        result = get_avg_price_per_store(self.books, self.bookstores)
        self.assertEqual(result, expected)

    def test_books_in_a_stores(self):
        expected = {
            "Академическая литература": ["Философия науки", "Математика для всех"],
            "Азбука знаний": ["Биология"],
        }
        result = get_books_in_a_stores(self.books, self.bookstores)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
