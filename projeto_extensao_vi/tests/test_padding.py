import unittest

from cipher.padding import add_padding, remove_padding


class PaddingTests(unittest.TestCase):
    def test_roundtrip_edge_sizes(self):
        for size in range(0, 13):
            data = bytes(range(size))
            padded = add_padding(data)
            self.assertEqual(len(padded) % 4, 0)
            self.assertEqual(remove_padding(padded), data)

    def test_full_block_padding_is_added(self):
        self.assertEqual(add_padding(b"ABCD")[-4:], b"\x04\x04\x04\x04")


if __name__ == "__main__":
    unittest.main()

