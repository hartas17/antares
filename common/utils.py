from PIL import Image


def resize_image(image, width=500, height=500):
    if image:
        size = width, height
        im = Image.open(image.path)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(image.path)
