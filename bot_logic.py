import random
import string


def gen_pass(length=8):
  """Generates a random password."""
  password = ""
  for i in range(length):
    password += random.choice(string.ascii_letters + string.digits)
  return password
