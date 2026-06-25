import os
import tempfile
import unittest

from cipher.file_io import decrypt_bytes, encrypt_bytes, process_file


class RoundTripTests(unittest.TestCase):
    def test_bytes_roundtrip_various_sizes(self):
        samples = [b"", b"a", b"abc", b"abcd", bytes(range(31)), bytes(range(256))]
        for sample in samples:
            encrypted = encrypt_bytes(sample, "Inn Seguros 2026")
            self.assertNotEqual(encrypted, sample)
            self.assertEqual(decrypt_bytes(encrypted, "Inn Seguros 2026"), sample)

    def test_file_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "input.bin")
            enc = os.path.join(tmp, "encrypted.bin")
            dec = os.path.join(tmp, "decrypted.bin")
            content = b"arquivo binario\x00\x01\x02com tamanho estranho"
            with open(src, "wb") as handle:
                handle.write(content)
            process_file("encrypt", "senha", src, enc)
            process_file("decrypt", "senha", enc, dec)
            with open(dec, "rb") as handle:
                self.assertEqual(handle.read(), content)


if __name__ == "__main__":
    unittest.main()

