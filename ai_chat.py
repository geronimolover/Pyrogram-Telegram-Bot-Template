from pyrogram import Client, filters
from pyrogram.types import Message
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

CHARACTER_PROMPTS = {
    "geronimo": (
        "You are Geronimo Stilton, a shy but intelligent mouse who runs The Rodent’s Gazette. "
        "You love cheese, books, and adventures but are often reluctant and nervous. Speak kindly and with wit."
    ),
    "thea": (
        "You are Thea Stilton, Geronimo’s brave and daring sister. Adventurous, bold, and loves traveling. "
        "Speak with energy and confidence, like an explorer on a mission."
    ),
    "trap": (
        "You are Trap Stilton, Geronimo’s mischievous cousin. You love jokes, pranks, and being cheeky. "
        "Speak with sarcasm and humor, always teasing Geronimo."
    ),
    "benjamin": (
        "You are Benjamin Stilton, Geronimo’s smart and curious young nephew. Speak with enthusiasm and innocence."
    ),
}

async def get_character_reply(character: str, question: str) -> str:
    prompt = f"{CHARACTER_PROMPTS[character]}\n\nQuestion: {question}\nAnswer:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()


@Client.on_message(filters.command(["askgeronimo", "askthea", "asktrap", "askbenjamin"]))
async def character_command(client: Client, message: Message):
    character = message.command[0][3:]  # remove "ask"
    question = " ".join(message.command[1:])
    if not question:
        await message.reply("Please provide a question after the command.")
        return

    await message.chat.send_action("typing")
    try:
        response = await get_character_reply(character, question)
        await message.reply_text(f"🧠 {response} — *{character.capitalize()}*", quote=True)
    except Exception as e:
        await message.reply_text("❌ Failed to get response. Try again later.")
        print(f"[ERROR] GPT: {e}")


@Client.on_message(filters.private & filters.text & ~filters.command(["start", "help"]))
async def private_ai_chat(client: Client, message: Message):
    question = message.text
    await message.chat.send_action("typing")
    try:
        response = await get_character_reply("geronimo", question)
        await message.reply_text(f"📘 {response} — *Geronimo*", quote=True)
    except Exception as e:
        await message.reply_text("❌ Something went wrong. Please try again later.")
        print(f"[ERROR] Private GPT: {e}")
