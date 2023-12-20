from PIL import Image, ImageEnhance


def enhance_image(image_file):
    img = Image.open(image_file)
    enhancer = ImageEnhance.Brightness(img)
    c_enhancer = ImageEnhance.Contrast(img)
    factor = 1.2
    img_output = enhancer.enhance(factor)
    img_output = c_enhancer.enhance(factor)
    img_output.save('images/enhanced_image.jpg')
    return 'images/enhanced_image.jpg'