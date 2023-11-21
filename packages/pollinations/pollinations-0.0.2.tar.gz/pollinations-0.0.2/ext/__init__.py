import requests
from .. import abc

@abc.resource(deprecated=False)
class Image:
  def __init__(self, save_file: str='tkr-Image.jpg', *args, **kwargs) -> None:
      self.__base: str = 'image.pollinations'
      self.save_file: str = save_file
      self.prompt: str = None

  def __repr__(self, *args, **kwargs) -> str:
    return f"Image(save_file={self.save_file})"

  @abc.resource(deprecated=False)
  def generate(self, prompt: str, *args, **kwargs) -> str:
      self.prompt: str = prompt
      request = requests.get(f'{abc.proto}{self.__base}{abc.ai}{prompt}')
      self.data: abc.ImageObject = abc.ImageObject(prompt, request.url, request.headers['Date'], content=request.content)
  
      return self.data
  
  @abc.resource(deprecated=False)
  def save(self, save_file: str=None, *args, **kwargs) -> abc.ImageObject:
    if save_file is None:
      save_file = self.save_file
  
    with open(save_file, 'wb') as handler:
      handler.write(self.data.content)
  
    return self.data
  
  @abc.resource(deprecated=False)
  def load(self, load_file: str=None, *args, **kwargs) -> str:
    if load_file is None:
      load_file = self.save_file
  
    with open(load_file, 'rb') as handler:
      return handler.read()
  
  @abc.resource(deprecated=False)
  def image(self, *args, **kwargs) -> abc.ImageObject:
    return self.data

  