
from dataclasses import dataclass


@dataclass
class GeneralConfig:
    TokenLimit: int
    temperature: float


config = GeneralConfig(
    TokenLimit=1000,
    temperature=0.7
)

print(config)
print(config.TokenLimit)
print(config.temperature)
