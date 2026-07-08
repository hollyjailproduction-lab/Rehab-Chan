# Rehab-Chan
# Llama-based Discord chatbot for drug rehabilitation consultations in Malang City

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Discord](https://img.shields.io/badge/Discord-Bot-5865F2?logo=discord)
![Llama](https://img.shields.io/badge/LLM-Llama%202%2F3-green?logo=llama)

# About
This Discord bot is designed to provide initial consultations regarding drug rehabilitation specifically for the Malang City area. Built with the Llama Large Language Model (LLM), this bot goes beyond simple conversation. It can intelligently detect user complaints (even with typos) and provide accurate information about local rehabilitation facilities without any AI hallucinations.
# Featured Feature
- Fuzzy Keyword Detection (Anti-Typo)  
It uses string matching logic with a similarity threshold >= 0.6 and whitespace removal. So, even if a user makes a typo (e.g., "sbau" for "sabu" or "gaja" for "ganja"), the bot can still categorize it correctly.
- Local Knowledge Base (Anti-AI-Hallucinations)  
No external databases are used. All rehabilitation facility data (such as BNN Kabupaten Malang & RSJ Lawang) is stored in data files/JSON format. The bot pulls this data directly, ensuring the addresses and contact information provided are 100% accurate and not artificially generated.
- Strict Persona & Rules
  It comes with a system_prompt.txt that sets the bot's personality to be friendly and supportive, while also enforcing strict rules:
    - The bot will NOT act as a counselor if the question does not touch on drugs.
    - The bot is able to respond tactfully to "temptations" or dangerous questions.
    - The bot will not provide a professional medical diagnosis (it will only direct you to a facility).
- Discord Integration  
Easily accessible directly through the Discord server, providing privacy and convenience for users who need it.

# Tech Stack
- Language: Python 3.10+
- Discord Library: discord.py
- LLM Server: Ollama (Llama 2 / Llama 3)
- Data Storage: JSON (Local)

# System Flow
1. User Input: The user types a message in Discord.  
2. Text Normalization: The bot cleans the text (lowercase & removes spaces).  
3. Fuzzy Matching: The bot matches the text against a list of keywords (drugs, inhalants, etc.) using a similarity formula >= 0.6.  
4. Category Classification:
    - If the keyword "Drugs" (methamphetamine, marijuana, etc.) is detected, it will direct you to rehabilitation data.
    - If the keyword "Inhalants" (glue, thinner, etc.) is detected, it will direct you to special treatment.
    - If not detected, the bot will refuse to respond as a counselor (according to the rules in system_prompt.txt).  

5. Data Retrieval: The bot retrieves rehabilitation facility data from the data/ folder (e.g., BNN Malang Regency, Lawang Mental Hospital).
6. Prompt Assembly: The bot combines system_prompt.txt (persona + rules) + JSON data + user question.  
7. LLM Response: The Llama model processes the prompt and sends an informative and human-like response to Discord.

# Detection System & Priority
Bot tidak serta-merta menjawab semua pertanyaan dengan AI. Ia melewati **sistem filter berjenjang** yang aku rancang khusus untuk menjaga keamanan pengguna:

| Priority | Category | Function |
| :--- | :--- | :--- |
| **1** | **Persona** | Detecting personal greetings or questions (Ex: "siapa kamu?"). The bot will respond casually, **WITHOUT** immediately going into counselor mode.. |
| **2** | **Emosi** | Detecting words like "cemas", "takut", "sedih". The bot will respond with empathy first. |
| **3** | **Craving** | Detecting a strong desire to use ("pengen make", "kepikiran").Bots will provide distraction interventions. |
| **4** | **Relapse** | Detecting recurrence ("kambuh", "kepleset"). The bot will respond without judgment and direct to recovery.. |
| **5** | **Jenis Narkoba** | Using **Fuzzy Matching** to detect narcotics (methamphetamine, marijuana), inhalants (glue, thinner), and designer drugs (benzo, fentanyl). |
| **6** | **Emergency** | Detecting critical words ("overdosis", "bunuh diri"). The bot will immediately provide emergency numbers and quick recommendations to the hospital. |
| **7** | **Rehab & Lokasi** | Combining words "rehab" with "Malang"to retrieve data from local JSON |
| **8** | **Pelaporan Hukum** | Detecting fear of the law ("ditangkap", "pasal"). The bot will direct you to the correct reporting procedure. |

# Prerequisite
- Python 3.10+ installed.
- Ollama installed and Llama model pulled (e.g., ollama pull llama3).
- Discord Bot Token (obtained from the Discord Developer Portal).

# Step by step
1. Clone this repository
git clone https://github.com/hollyjailproduction-lab/Rehab-Chan.git  
cd your-repo

2. install dependencies  
pip install -r requirements.txt

3. Set Environment Variables:
Fill in the discord bot token and API key for LLM:  
DISCORD_TOKEN = "your_bot_token_here"
GROQ_API_KEY = "your_LLM_API_Key"  

4. Run the bot  
python bot.py  
