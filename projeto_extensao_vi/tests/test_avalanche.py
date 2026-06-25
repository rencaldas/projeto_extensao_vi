import unittest

from avalanche_demo import bit_count
from cipher.block_cipher import trace_encrypt_block
from cipher.keyschedule import ROUNDS


class AvalancheTests(unittest.TestCase):
    def test_key_change_has_visible_avalanche(self):
        trace_a = trace_encrypt_block(0x496E6E53, "Q", ROUNDS)
        trace_b = trace_encrypt_block(0x496E6E53, "Y", ROUNDS)
        second_round_changed = bit_count(trace_a[1] ^ trace_b[1])
        final_changed = bit_count(trace_a[-1] ^ trace_b[-1])
        self.assertGreaterEqual(second_round_changed, 12)
        self.assertGreaterEqual(final_changed, 12)


if __name__ == "__main__":
    unittest.main()
