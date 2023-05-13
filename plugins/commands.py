from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from Script import script
import asyncio
import sys
import os
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pyrogram import Client

START_TXT = script.START_TXT
HELP_TXT = script.HELP_TXT 
ABOUT_TXT = script.ABOUT_TXT

# Initialize Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get("SPOTIPY_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET")))

@Client.on_message(filters.text & filters.incoming)
async def get_song_details(client, message):
    song_name = message.text
    results = sp.search(q=song_name, limit=1)
    if results:
        # Send song name
        name = results['tracks']['items'][0]['name']
        
        # Send artist names
        artists = results['tracks']['items'][0]['artists']
        for artist in artists:
            art = artist['name']
        
        # Send album name
        album = results['tracks']['items'][0]['album']['name']
        
        # Get popularity details
        popularity = results['tracks']['items'][0]['popularity']
        
        # Create caption with song details
        caption = f"<b>{name}</b>\n\nArtist: {art}\nAlbum: {album}\nPopularity: {popularity}"
        
        # Send thumbnail image URL
        thumbnail_url = results['tracks']['items'][0]['album']['images'][0]['url']
        await message.reply_photo(thumbnail_url, caption=name)
        
    else:
        await message.reply_text("Sorry, couldn't find any matching results for that song name.")
	
@Client.on_message(filters.command("start") & filters.private)
async def start(bot, cmd):
	await cmd.reply_text(
		START_TXT.format(cmd.from_user.first_name), 
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton("🔮Help", callback_data='help_cb'),
					InlineKeyboardButton("⚔About", callback_data='about_cb')
				],
				[
					InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/kinu6'),
					InlineKeyboardButton("⚙️Update Channel", url="https://t.me/TMWAD")
				]
			]
		)
	)
    
  
@Client.on_message(filters.command("help") & filters.private)
async def help(bot, cmd):	
	await cmd.reply_text(
		HELP_TXT, 
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton("⚔About", callback_data='about_cb'),
					InlineKeyboardButton("⚡Back", callback_data='start_cb')
				],
				[
					InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/kinu6'),
					InlineKeyboardButton("⚙️Update Channel", url="https://t.me/TMWAD")
				]
			]
		)
	)
    
@Client.on_message(filters.command("about") & filters.private)
async def about(bot, cmd):	
	await cmd.reply_text(
		ABOUT_TXT, 
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton("🔮Help", callback_data='help_cb'),
					InlineKeyboardButton("⚡Back", callback_data='start_cb')
				],
				[
					InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/kinu6'),
					InlineKeyboardButton("⚙️Update Channel", url="https://t.me/TMWAD")
				]
			]
		)
	)
