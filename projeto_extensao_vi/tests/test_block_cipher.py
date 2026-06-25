import unittest

from cipher.block_cipher import decrypt_block, encrypt_block
from cipher.keyschedule import derive_subkeys


class BlockCipherTests(unittest.TestCase):
    def test_block_roundtrip(self):
        subkeys = derive_subkeys("senha academica")
        for block in [0, 1, 0x12345678, 0xFFFFFFFF, 0x496E6E53]:
            self.assertEqual(decrypt_block(encrypt_block(block, subkeys), subkeys), block)


if __name__ == "__main__":
    unittest.main()

