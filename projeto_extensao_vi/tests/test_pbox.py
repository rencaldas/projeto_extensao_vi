import unittest

from cipher.pbox import inverse_permute_block, permute_block


class PBoxTests(unittest.TestCase):
    def test_inverse_for_sample_words_and_keys(self):
        words = [0, 1, 0x12345678, 0xFFFFFFFF, 0xA5A5C3C3]
        keys = [0, 0x11111111, 0x89ABCDEF, 0xFFFFFFFF]
        for word in words:
            for key in keys:
                self.assertEqual(inverse_permute_block(permute_block(word, key), key), word)


if __name__ == "__main__":
    unittest.main()

