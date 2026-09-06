from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import wikipedia
from ddgs import DDGS
from googletrans import Translator

app = Flask(__name__)
CORS(app)

ddgs = DDGS()
translator = Translator()

# Wikipedia dili Türkçe
wikipedia.set_lang("tr")

# Matematik çöz
def solve_math(question):
    try:
        safe = re.sub(r'[^0-9+\-*/(). ]', '', question)
        if safe.strip() != "":
            return eval(safe)
        return None
    except:
        return None

# Küçük sohbet (small talk)
def small_talk(question):
    q = question.lower()
    if any(word in q for word in ["Okan Hoca kimdir", "Okan Hoca", "okan hoca", "Okanır kimdir", "okan hoca kimdir", "okanır kimdir", "Okan kimdir", "okan kimdir", "okanır"]):
        return "Okan ALYELKEN, namıdeğer okanır Kırdar Bilgiören Koleji'nde çalışan matematik hocasıdır.Ve çok sigmadır."
    
    if any(word in q for word in ["İlayda Hoca kimdir", "İlayda Hoca", "Who is İlayda", "ilayda teacher", "İlaydaa teacher"]):
        return "İlayda Hoca, Kırdar Bilgiören Koleji'nde çalışan bir öğretmendir.Ve çok sigmadır."
    
    if any(word in q for word in ["Zeynep Hoca kimdir", "Zeynep Hoca", "Who is Zeynep", "zeynep teacher", "Zeynep teacher", "zeynep hoca kimdir","zeynep hoca"]):
        return "Zeynep Hoca, Kırdar Bilgiören Koleji'nde çalışan bir öğretmendir.Ve çok zekidir."
    
    if any(word in q for word in ["knk", "kanka", "kardeşim", "bro", "dostum"]):
        return "Efendim knk!"
    
    if any(word in q for word in ["nbr", "naber knk", "selam aga"]):
        return "Merhaba knk!"
    
    if any(word in q for word in ["sen nesin", "adın ne", "ismin ne", "ismin ne",  "sen kimsin"]):
        return "Merhaba! Ben bir yapay zeka asistanıyım,adım Kırdar AI ve sorularını cevaplamak için buradayım! 😊"
    
    if any(word in q for word in ["seni kim tasarladı", "seni kim yaptı", "seni kim geliştirdi", "seni kim üretti","seni kim oluşturdu"]):
        return "Ben Emre, Efe, Selo ve danışman Dr. Zeynep Hoca tarafından geliştirildim! 😊"
    
    if any(word in q for word in ["merhaba", "selam", "hey"]):
        return "Merhaba! 😊 Nasıl yardımcı olabilirim?"

    if any(word in q for word in ["nasılsın", "naber", "iyi misin"]):
        return "İyiyim, teşekkür ederim! 😊 Sana nasıl yardımcı olabilirim?"

    if any(word in q for word in ["ne yapıyorsun", "napıyorsun"]):
        return "Senin sorularını cevaplamak için buradayım 😄 Nasıl yardımcı olabilirim?"

    return None

# Metni Türkçeye çevir
def translate_to_tr(text):
    try:
        return translator.translate(text, dest="tr").text
    except:
        return text

# İnternetten arama
def search_internet(query):
    try:
        results = ddgs.text(query + " Türkçe", max_results=2)
        text = ""
        for r in results:
            body = r.get("body", "").strip()
            if body:
                text += body + "\n"
        return text if text else None
    except:
        return None

# Soruyu cevapla
def answer_question(question):
    # 0) Küçük sohbet
    chat = small_talk(question)
    if chat:
        return chat

    # 1) Matematik sorusu
    math_ans = solve_math(question)
    if math_ans is not None:
        return f"Matematik sonucu: {math_ans}"

    # 2) Wikipedia dene
    try:
        summary = wikipedia.summary(question, sentences=2)
        if summary:
            return f"Wikipedia: {summary}"
    except:
        pass

    # 3) DuckDuckGo arama
    ddg_ans = search_internet(question)
    if ddg_ans:
        return f"Internet Arama Sonuçları:\n{translate_to_tr(ddg_ans)}"

    # 4) Fallback
    return "Üzgünüm, cevap bulamadım 😅"

# API route
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    answer = answer_question(question)
    return jsonify({"answer": answer})

# HTML route
@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)