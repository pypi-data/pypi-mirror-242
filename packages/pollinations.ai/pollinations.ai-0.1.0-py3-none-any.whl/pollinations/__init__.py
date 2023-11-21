from .abc import samples

__version__ = '0.1.0'

import random

class Sample:
  @property
  def prompt(self) -> str:
    return random.choice(samples)

  def batch(self, size: int=10, *args, **kwargs) -> list:
    return random.choices(samples, k=size)

def main(*args, **kwargs) -> str:
  pollinations_ai_info: str = """
  [[ pollinations.ai ]]

  Architect:
    pollinations
      file: __init__.py

      folders:
        - abc
        - ai
        - ext

      [[ ai usage ]]
      ```python

      import pollinations.ai as ai

      ImageAi = ai.Image()
      ImageAi.generate(
          ai.sample()
      )
      
      ImageAi.save()
      ```
  """
  print(pollinations_ai_info)
  return pollinations_ai_info

help: object = main