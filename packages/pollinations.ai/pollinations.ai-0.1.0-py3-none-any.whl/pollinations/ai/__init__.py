import random
from ..ext import Image
from .. import abc

samples: list = abc.samples

@abc.resource(deprecated=False)
def sample(*args, **kwargs) -> str:
  return random.choice(samples)

@abc.resource(deprecated=False)
def sample_batch(size: int, *args, **kwargs) -> str:
  return random.choices(samples, k=size)

