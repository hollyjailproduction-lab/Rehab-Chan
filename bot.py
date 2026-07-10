import json
import discord
from groq import Groq
from dotenv import load_dotenv

conversation_history = []
user_memory = {}

load_dotenv()

# === Groq (LLAMA 3) client ===
client_ai = Groq(api_key=GROQ_API_KEY)

# === Load data lokal ===
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# ==================== USER MEMORY ====================
user_memory = {}

# ==================== KATEGORI DETECTION ====================
def fuzzy_match(text, word):
    """
    Mengembalikan True jika text mirip dengan word walau typo ringan.
    Cocok untuk kasus seperti:
    sabu -> sabbu, sabo
    ganja -> ganjja
    heroin -> herroin
    alprazolam -> aprozolam, alprozalam
    """
    t = text.replace(" ", "")
    w = word.replace(" ", "")

    if w in t:
        return True

    matches = sum(1 for a, b in zip(t, w) if a == b)

    similarity = matches / max(len(t), len(w))

    return similarity >= 0.6

def fuzzy_any(text, words):
    return any(fuzzy_match(text, w) for w in words)

def detect_category(text):
    t = text.lower()

    # 1. Persona
    if any(k in t for k in [
        "siapa kamu",
        "hobimu",
        "hobi kamu",
        "suka apa",
        "makanan favorit",
        "minuman favorit",
        "punya saudara",
        "punya keluarga",
        "punya kakak",
        "punya adik",
        "siapa penciptamu",
        "yang buat kamu"
    ]):
        return "persona"

    # 2. Emotional triggers
    elif any(k in t for k in ["cemas", "takut", "sedih", "marah", "bingung", "gelisah"]):
        return "emosi"

    # 3. Craving
    elif any(k in t for k in ["craving", "pengen make", "kepikiran make", "pengen pakai lagi"]):
        return "craving"

    # 4. Relapse
    elif any(k in t for k in ["relapse", "kambuh", "kepleset lagi", "kumat"]):
        return "relapse"

    # 5. Drugs
    elif fuzzy_any(t, ["sabu", "ganja", "kokain", "heroin", "mdma", "lsd", "shrooms"]):
        return "narkoba"

    elif fuzzy_any(t, ["lem", "thinner", "ngelem", "aerosol", "inhalant"]):
        return "inhalant"

    elif fuzzy_any(t, ["benzo", "alprazolam", "xanax", "etizolam"]):
        return "designer_benzo"

    elif fuzzy_any(t, ["fentanyl", "opioid", "carfentanil", "u-47700"]):
        return "designer_opioid"

    elif fuzzy_any(t, ["sakau", "withdrawal", "ketagihan"]):
        return "withdrawal"

    # 6. Emergency
    elif fuzzy_any(t, ["mati", "bunuh diri", "overdosis", "ga bisa napas"]):
        return "emergency_cue"

    # 7. Rehab (more specific)
    elif "rehab" in t or "tempat rehab" in t:
        return "rehab"

    elif ("malang" in t) and fuzzy_any(t, ["dimana", "alamat", "dekat", "cari", "rumah sakit"]):
        return "rehab"
    
    elif any(k in t for k in ["lapor", "melapor", "ditangkap", "takut hukum", "uu narkotika", "undang", "pasal"]):
        return "pelaporan"


    return None



# === LOAD DATASET ===
def load_dataset(category):
    try:
        with open(f"data/{category}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except: 
        return None


# === DISCORD SETUP ===
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# === MAIN EVENT ===
@client.event
async def on_message(message):
    if message.author.bot:
        return

    uid = str(message.author.id)
    user_text = message.content

    # INIT MEMORY
    if uid not in user_memory:
        user_memory[uid] = []

    user_memory[uid].append({"role": "user", "content": user_text})

    # COMMANDS
    if user_text == "!test":
        await message.channel.send("Bot aktif ✔️")
        return

    if user_text == "!reset":
        user_memory[uid] = []
        await message.channel.send("Memory kamu sudah di-reset ✔️")
        return

    # DETECT CATEGORY
    category = detect_category(user_text)
    dataset_content = ""

    if category:
        data = load_dataset(category)
        if data:
            if category == "persona":
                dataset_content = "\n\nDATA_PERSONA:\n" + json.dumps(data, ensure_ascii=False)
            else:
                dataset_content = "\n\nDATA_TERKAIT:\n" + json.dumps(data, ensure_ascii=False)

    # BUILD PROMPT
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n\n" + dataset_content}
    ] + user_memory[uid][-4:]

    # CALL LLM
    response = client_ai.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content
    user_memory[uid].append({"role": "assistant", "content": reply})

    await message.channel.send(reply)


# === RUN BOT ===
client.run(DISCORD_TOKEN)