import unittest
from base.logger import http_log, main_log, fg_log


class HttpTestCase(unittest.TestCase):
    def test_something(self):
        http_log.log("1")
        main_log.log("2")
        fg_log.log("3")
        http_log.log("4")
        main_log.log("5")
        fg_log.log("6")
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
