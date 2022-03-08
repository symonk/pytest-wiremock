from dataclasses import dataclass


@dataclass
class LogNormalSettingsModel:
    median: int
    sigma: int
    fixed_delay: int
    type_: str = "lognormal"
