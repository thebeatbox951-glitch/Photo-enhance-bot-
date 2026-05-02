import os
import logging
from PIL import Image, ImageEnhance, ImageFilter
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me a photo to enhance.')

def enhance_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def enhance_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def apply_grayscale(image):
    return image.convert('L')

def apply_sepia(image):
    width, height = image.size
    pixels = image.load()
    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            pixels[px, py] = (min(tr, 255), min(tg, 255), min(tb, 255))
    return image

def apply_blur(image):
    return image.filter(ImageFilter.GaussianBlur(radius=5))

def resize_image(image, width, height):
    return image.resize((width, height))

def handle_photo(update: Update, context: CallbackContext) -> None:
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    image = Image.open('user_photo.jpg')

    # Get command from text
    command = context.args[0] if context.args else None

    if command == 'brightness':
        enhanced_image = enhance_brightness(image, 1.5)  # Example factor for brightness
    elif command == 'contrast':
        enhanced_image = enhance_contrast(image, 1.5)     # Example factor for contrast
    elif command == 'grayscale':
        enhanced_image = apply_grayscale(image)
    elif command == 'sepia':
        enhanced_image = apply_sepia(image)
    elif command == 'blur':
        enhanced_image = apply_blur(image)
    elif command == 'resize':
        enhanced_image = resize_image(image, 800, 600)  # Example size
    else:
        update.message.reply_text('Unknown command!')
        return

    enhanced_image.save('enhanced_photo.jpg')
    update.message.reply_photo(photo=open('enhanced_photo.jpg', 'rb'))

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo & Filters.command, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()