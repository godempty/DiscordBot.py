import random
def randomID(len):
  choice="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890#$%!&"
  ret ="".join(random.choices(choice,k=len))
  return ret
  