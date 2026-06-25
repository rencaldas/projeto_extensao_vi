import unittest

from cipher.keyschedule import ROUNDS, derive_master_key, derive_subkeys


class KeyScheduleTests(unittest.TestCase):
    def test_master_key_is_deterministic(self):
        self.assertEqual(derive_master_key("inn"), derive_master_key("inn"))

    def test_subkeys_are_different(self):
        subkeys = derive_subkeys("inn")
        self.assertEqual(len(subkeys), ROUNDS)
        self.assertEqual(len(set(subkeys)), ROUNDS)


if __name__ == "__main__":
    unittest.main()

