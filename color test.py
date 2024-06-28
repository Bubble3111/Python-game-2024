from PIL import Image
from PIL import *
open = Image.open('knight walk/row-1-column-1.png').convert('RGB')

r, g, b = open.split()
r = r.point(lambda i: i * 2)

result = Image.merge('RGB', (r, g, b))

result.show()