# Library imports
import telebot
import requests
import json
import spotipy
from telebot import types
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from spotifysearch.client import Client

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



bot = telebot.TeleBot("TOKEN-TG")
auth_manager = SpotifyClientCredentials(client_id="Client-TOKEN", client_secret="TOKEN-SPOTIFY")
spotify = spotipy.Spotify(auth_manager=auth_manager)

uris = []
preview_urls = []
names = []

def make_inline_buttons_list(names, artists):
    buttons = []
    for i in range(len(names)):
        buttons.append(types.InlineKeyboardButton(text=names[i]+" - "+artists[i], callback_data=str(i)))
    return buttons

def spotify_search_track(query):
    results = spotify.search(q=query, type="track", limit=5)
    tracks = results['tracks']['items']


    length = len(tracks)
    preview_urls = []
    for i in range(length):
        preview_urls.append(tracks[i]['preview_url'])

    artist = []
    for i in range(length):
        artist.append(tracks[i]['artists'][0]['name'])

    uri = []
    for i in range(length):
        uri.append(tracks[i]['uri'])

    names = []
    for i in range(length):
        names.append(tracks[i]['name'])

    return preview_urls, uri, names, artist

def spotify_uri_to_url(uri):
    return "https://open.spotify.com/embed/track/" + uri.split(":")[2]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт, цей бот дозволяє шукати пісні і прослуховувати демо!")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Для пошуку просто напиши назву пісні і вибери із запропонованих")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    urls, uri, name, artist = spotify_search_track(message.text)
    global uris
    uris = uri
    global preview_urls
    preview_urls = urls
    global names
    names = name
    buttons = make_inline_buttons_list(name, artist)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    bot.reply_to(message, text="message.text", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    data = call.data
    button = types.InlineKeyboardButton(text="listen on spotify", url=spotify_uri_to_url(uris[int(data)]))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(button)
    bot.send_message(call.message.chat.id, text = "<a href='" + preview_urls[int(data)] + "'>"+names[int(data)]+"</a>", parse_mode = 'HTML', reply_markup=keyboard )





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.polling()