import unittest
from textwrap import dedent
from io import StringIO
from lru_cache_app import lru_cache


class LruTestCase(unittest.TestCase):

    def setUp(self):
        self.stdout = StringIO()
        self.stdin = StringIO()

    def test_lru_cache(self):
        self.stdin.write('SIZE 3\nGET foo\nSET foo 1\n')
        self.stdin.write('GET foo\nSET foo 1.1\nGET foo\n')
        self.stdin.write('SET spam 2\nGET spam\n')
        self.stdin.write('SET ham third\nSET parrot four\n')
        self.stdin.write('GET foo\nGET spam\nGET ham\n')
        self.stdin.write('GET ham parrot\nGET parrot\n')
        self.stdin.write('EXIT\n')
        self.stdin.seek(0)
        lru_cache(input=self.stdin, output=self.stdout)
        s = """
            SIZE OK
            NOTFOUND
            SET OK
            GOT 1
            SET OK
            GOT 1.1
            SET OK
            GOT 2
            SET OK
            SET OK
            NOTFOUND
            GOT 2
            GOT third
            ERROR
            GOT four
            """
        self.assertEqual(self.stdout.getvalue().strip(), dedent(s).strip())


if __name__ == '__main__':
    unittest.main()
