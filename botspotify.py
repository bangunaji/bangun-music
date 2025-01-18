import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load variabel lingkungan
load_dotenv()

# Konfigurasi Spotify API
SPOTIFY_CLIENT_ID = os.getenv("d47974f0e1f04c779d0e0726676820f6")
SPOTIFY_CLIENT_SECRET = os.getenv("2824d642eb584e86bf5d360b6766797a")
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Fungsi untuk menangani perintah /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Halo! Saya adalah bot Spotify. Gunakan /search <judul lagu> untuk mencari lagu.")

# Fungsi untuk menangani perintah /search
def search(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Kirimkan judul lagu setelah perintah /search.")
        return

    query = " ".join(context.args)
    try:
        results = sp.search(q=query, type="track", limit=5)
        if results["tracks"]["items"]:
            reply = "Hasil pencarian:\n"
            for track in results["tracks"]["items"]:
                reply += f"- {track['name']} oleh {track['artists'][0]['name']}\n  Link: {track['external_urls']['spotify']}\n\n"
            update.message.reply_text(reply)
        else:
            update.message.reply_text("Tidak ada hasil ditemukan.")
    except Exception as e:
        update.message.reply_text("Terjadi kesalahan saat mencari lagu.")
        print(e)

# Main function
def main():
    # Token Telegram Bot
    TELEGRAM_TOKEN = os.getenv("7772517833:AAGmphYFcg45QoeMlMgaCqFbp3AApshIpSE")

    # Inisialisasi Updater dan Dispatcher
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Daftarkan handler
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search))

    # Jalankan bot
    print("Bot sedang berjalan...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
