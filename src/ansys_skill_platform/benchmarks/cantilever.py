"""Euler-Bernoulli reference calculation for a rectangular cantilever beam."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CantileverBenchmark:
    """Analytical reference for a tip-loaded rectangular cantilever."""

    length_m: float = 1.0
    width_m: float = 0.05
    height_m: float = 0.05
    young_modulus_pa: float = 210e9
    poisson_ratio: float = 0.3
    tip_load_n: float = -1000.0

    @property
    def second_moment_area_m4(self) -> float:
        return self.width_m * self.height_m**3 / 12.0

    @property
    def analytical_tip_displacement_m(self) -> float:
        return (
            self.tip_load_n
            * self.length_m**3
            / (3.0 * self.young_modulus_pa * self.second_moment_area_m4)
        )

    def relative_error_percent(self, fea_tip_displacement_m: float) -> float:
        reference = abs(self.analytical_tip_displacement_m)
        return abs(abs(fea_tip_displacement_m) - reference) / reference * 100.0

    def as_dict(self) -> dict[str, float]:
        return {
            "length_m": self.length_m,
            "width_m": self.width_m,
            "height_m": self.height_m,
            "young_modulus_pa": self.young_modulus_pa,
            "poisson_ratio": self.poisson_ratio,
            "tip_load_n": self.tip_load_n,
            "second_moment_area_m4": self.second_moment_area_m4,
            "analytical_tip_displacement_m": self.analytical_tip_displacement_m,
        }
