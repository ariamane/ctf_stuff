# An example of image generation in Python
# Kinda just copied it from Pillow docs and stackoverflow :P


from PIL import Image

# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
img = Image.new('RGBA', (690, 420), "black") # create a new black image
pixels = img.load() # create the pixel map

# (412, 309)
pixels[412, 309] = (52, 146, 235, 123)

# (12, 209)
pixels[12, 209] = (42, 16, 125, 231)

# (264, 143)
pixels[264, 143] = (122, 136, 25, 213)


w, h = img.size
print(w != 690 or h != 420)
print(img.getpixel((412, 309)) != (52, 146, 235, 123))
print(img.getpixel((12, 209)) != (42, 16, 125, 231))
print(img.getpixel((264, 143)) != (122, 136, 25, 213))

img.show()
