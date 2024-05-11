from PIL import Image

def resize_image(image, width, height):
    img = Image.open(image)
    img_resized = img.resize((width, height), Image.BICUBIC)  # Use Image.ANTIALIAS instead of ANTIALIAS
    img_resized.save(image.path)
