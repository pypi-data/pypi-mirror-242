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

@abc.resource(deprecated=True)
def help(*args, **kwargs) -> str:
  help_return: str = """
  sample(): returns 1 random sample prompt

  sample_batch(size: int): returns size batch of random sample prompts

  Image(save_file: str (OPTIONAL)): inialize the ai.Image

  Image.generate(prompt: str): generate an image from a prompt

  Image.generate_batch(prompts: list): generate an image from a batch of prompts

  Image.save(save_file: str (OPTIONAL)): save the image to a file

  Image.load(load_file: str (OPTIONAL)): load the image from a file

  Image.image(): return the image object
  
  """""
  return help_return