# app.py
import wikipedia
from ddgs import DDGS
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

ddgs = DDGS()
app = Flask(__name__)
CORS(app)

# Matematik çözme fonksiyonu
def solve_math(question):
    try:
        safe_question = re.sub(r'[^0-9+\-*/(). ]', '', question)
        if safe_question.strip() != '':
            return eval(safe_question)

        # Kesir soruları: "96 sayısının sekizde biri ile altıda birin toplamı"
        numbers = [int(s) for s in re.findall(r'\d+', question)]
        fractions = re.findall(r'(\d+)de biri', question)
        result = 0
        if numbers and fractions:
            for f in fractions:
                result += numbers[0] / int(f)
            return result

        return None
    except:
        return None

# DuckDuckGo arama
def search_ddg(query):
    try:
        results = ddgs.text(query, safesearch='Moderate', timelimit='y', max_results=1)
        for r in results:
            return r['body']
        return None
    except:
        return None

# Cevap fonksiyonu
def answer_question(question):
    q = question.lower().strip()

    # 1️⃣ Türkçe selamlaşmalar
    selamlar = ["selam", "merhaba", "naber", "iyi misin", "nasılsın"]
    if any(word in q for word in selamlar):
        return "İyiyim! Sana nasıl yardımcı olabilirim? 😊"

    # 2️⃣ Matematik çöz
    math_result = solve_math(question)
    if math_result is not None:
        return f"Matematik sonucu: {math_result}"

    # 3️⃣ Wikipedia dene
    try:
        summary = wikipedia.summary(question, auto_suggest=False, sentences=3)
        return f"Wikipedia: {summary}"
    except:
        pass

    # 4️⃣ DuckDuckGo dene
    ddg_result = search_ddg(question)
    if ddg_result:
        return f"DuckDuckGo: {ddg_result}"

    # 5️⃣ Genel fallback
    return "Üzgünüm, bunu bulamadım. Başka bir şey sormak ister misin?"

# Flask endpoint
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    answer = answer_question(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)