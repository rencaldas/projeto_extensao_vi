import unittest

from cipher.sbox import inv_sbox, sbox


class SBoxTests(unittest.TestCase):
    def test_inverse_for_all_nibbles(self):
        for value in range(16):
            self.assertEqual(inv_sbox(sbox(value)), value)


if __name__ == "__main__":
    unittest.main()

