import unittest

from ansys_skill_platform.benchmarks import CantileverBenchmark


class CantileverBenchmarkTests(unittest.TestCase):
    def test_default_tip_displacement(self):
        benchmark = CantileverBenchmark()
        self.assertAlmostEqual(
            benchmark.analytical_tip_displacement_m,
            -0.0030476190476190477,
            places=12,
        )

    def test_relative_error(self):
        benchmark = CantileverBenchmark()
        self.assertLess(benchmark.relative_error_percent(-0.00304), 1.0)


if __name__ == "__main__":
    unittest.main()
