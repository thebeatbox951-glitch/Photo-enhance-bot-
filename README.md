import os
import requests
from PIL import Image
from io import BytesIO
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ====== CONFIG ======
BOT_TOKEN = "8659416686:AAH0CNPKp5Hom6LfcJoMPbFGMdlhryGSFc0"
STABILITY_API_KEY = "sk-eAKFQTQ145B09AfWf4svhobBsAD5cWHx5WiUi6ST7fZn15bv"

DOWNLOAD_DIR = "downloads"
ENHANCED_DIR = "enhanced"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(ENHANCED_DIR, exist_ok=True)

# ====== START COMMAND ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n📸 Please upload your photo to enhance quality."
    )

# ====== IMAGE ENHANCEMENT FUNCTION ======
def enhance_image(image_path):
    url = "https://api.stability.ai/v2beta/stable-image/upscale"

    with open(image_path, "rb") as f:
        files = {"image": f}

        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
        }

        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        return response.content
    else:
        print("Error:", response.text)
        return None

# ====== HANDLE PHOTO ======
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    await message.reply_text("⏳ Enhancing your image, please wait...")

    photo = message.photo[-1]
    file = await photo.get_file()

    input_path = os.path.join(DOWNLOAD_DIR, f"{file.file_id}.jpg")
    output_path = os.path.join(ENHANCED_DIR, f"enhanced_{file.file_id}.jpg")

    await file.download_to_drive(input_path)

    enhanced_data = enhance_image(input_path)

    if enhanced_data:
        with open(output_path, "wb") as f:
            f.write(enhanced_data)

        with open(output_path, "rb") as f:
            await message.reply_photo(photo=f, caption="✨ Enhanced Image")
    else:
        await message.reply_text("❌ Failed to enhance image.")

# ====== MAIN ======
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()# Photo-enhance-bot-
A Telegram bot for enhancing photos using Python
