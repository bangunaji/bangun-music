from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Konfigurasi token bot Telegram dan Spotify API
TELEGRAM_TOKEN = "7772517833:AAGmphYFcg45QoeMlMgaCqFbp3AApshIpSE"
SPOTIPY_CLIENT_ID = "d47974f0e1f04c779d0e0726676820f6"
SPOTIPY_CLIENT_SECRET = "2824d642eb584e86bf5d360b6766797a"

# Inisialisasi Spotify API
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Fungsi untuk menangani perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Halo! Ketikkan judul lagu untuk mencari lagu terkait. Saya akan memberikan beberapa hasil pencarian dari Spotify!"
    )

# Fungsi untuk mencari lagu
async def search_song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text.strip()  # Ambil teks yang diketik user
    if not query:
        await update.message.reply_text("Harap ketik judul lagu untuk mencari.")
        return

    try:
        # Cari lagu di Spotify
        results = sp.search(q=query, type="track", limit=5)  # Mengambil 5 hasil teratas
        if results["tracks"]["items"]:
            response = "Berikut beberapa lagu yang saya temukan:\n\n"
            for track in results["tracks"]["items"]:
                track_name = track["name"]
                artist_name = track["artists"][0]["name"]
                track_url = track["external_urls"]["spotify"]
                response += f"🎵 *{track_name}* oleh *{artist_name}*\n🔗 [Dengarkan di Spotify]({track_url})\n\n"
        else:
            response = "Maaf, saya tidak menemukan lagu yang sesuai dengan pencarianmu."

        # Kirim hasil ke user
        await update.message.reply_text(response, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan: {e}")

# Fungsi utama
def main() -> None:
    # Buat aplikasi Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Tambahkan handler untuk perintah /start dan pencarian lagu
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_song))

    # Jalankan bot
    application.run_polling()

if __name__ == "__main__":
    main()
