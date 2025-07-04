from groq import Groq

client = Groq(api_key="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")  # Ganti dengan key kamu

def summarize(text):
    if not text or not isinstance(text, str) or len(text.strip()) < 30:
        return "Teks terlalu pendek atau kosong"

    try:
        prompt = f"""
        Ringkaskan atau summarizekan teks berikut menjadi 2–3 kalimat menggunakan Bahasa Indonesia yang jelas dan alami.
        Jangan sertakan pembuka seperti “Ringkasan:”, “Berikut ini adalah...”, atau sejenisnya.Langsung tuliskan isi ringkasan tanpa pengantar apa pun.
        {text.strip()}

        Ringkasan:
        """

        response = client.chat.completions.create(
            model="llama3-8b-8192",  # atau "mixtral-8x7b-32768" untuk ringkasan lebih panjang
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ Error saat ringkasan Groq: {e}")
        return "Ringkasan gagal"
