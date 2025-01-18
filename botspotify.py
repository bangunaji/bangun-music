from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Konfigurasi token bot Telegram
TELEGRAM_TOKEN = "7772517833:AAGmphYFcg45QoeMlMgaCqFbp3AApshIpSE"

# Konfigurasi Spotify API
SPOTIPY_CLIENT_ID = "d47974f0e1f04c779d0e0726676820f6"
SPOTIPY_CLIENT_SECRET = "2824d642eb584e86bf5d360b6766797a"

# Inisialisasi Spotipy
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Fungsi untuk perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Halo! Saya adalah bot Spotify. Gunakan perintah /search <judul lagu> untuk mencari lagu.")

# Fungsi untuk mencari lagu
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Harap masukkan judul lagu setelah perintah /search.")
        return

    results = sp.search(q=query, type="track", limit=1)
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        track_url = track["external_urls"]["spotify"]
        response = f"Lagu ditemukan: {track_name} oleh {artist_name}\nDengarkan di Spotify: {track_url}"
    else:
        response = "Maaf, lagu tidak ditemukan."

    await update.message.reply_text(response)

# Fungsi utama
def main() -> None:
    # Buat aplikasi Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Tambahkan handler untuk perintah
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))

    # Jalankan bot
    application.run_polling()

if __name__ == "__main__":
    main()
