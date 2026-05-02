from PIL import Image, ImageEnhance, ImageFilter

class PhotoEnhancer:
    def __init__(self, image_path):
        self.image = Image.open(image_path)

    def enhance_brightness(self, factor):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)

    def enhance_contrast(self, factor):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)

    def convert_to_grayscale(self):
        self.image = self.image.convert('L')

    def apply_sepia(self):
        width, height = self.image.size
        pixels = self.image.load()  # create the pixel map
        for py in range(height):
            for px in range(width):
                r, g, b = self.image.getpixel((px, py))
                # Apply sepia filter
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                # ensure the values are within bounds
                if tr > 255:
                    tr = 255
                if tg > 255:
                    tg = 255
                if tb > 255:
                    tb = 255
                pixels[px, py] = (tr, tg, tb)

    def apply_blur(self, radius):
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))

    def resize(self, width, height):
        self.image = self.image.resize((width, height), Image.ANTIALIAS)

    def save_image(self, output_path):
        self.image.save(output_path)
