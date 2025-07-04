from groq import Groq

# Inisialisasi client Groq
client = Groq(api_key="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")

def get_prompt(text):
    return (
        "Tentukan kategori utama dari teks berikut berdasarkan klasifikasi sektor ekonomi Indonesia.\n"
        "Pilih **satu** jawaban yang paling sesuai dari daftar kategori berikut (contoh jawaban: A. 1. a., C. 10., G. 2., dst):\n\n"
        "A. Pertanian, Kehutanan, dan Perikanan\n"
        "A. 1. Pertanian, Peternakan, Perburuan dan Jasa Pertanian\n"
        "A. 1. a. Tanaman Pangan\n"
        "A. 1. b. Tanaman Hortikultura Semusim\n"
        "A. 1. c. Perkebunan Semusim\n"
        "A. 1. d. Tanaman Hortikultura Tahunan dan Lainnya\n"
        "A. 1. e. Perkebunan Tahunan\n"
        "A. 1. f. Peternakan\n"
        "A. 1. g. Jasa Pertanian dan Perburuan\n"
        "A. 2. Kehutanan dan Penebangan Kayu\n"
        "A. 3. Perikanan\n"
        "B. Pertambangan dan Penggalian\n"
        "B. 1. Pertambangan Minyak, Gas dan Panas Bumi\n"
        "B. 2. Pertambangan Batubara dan Lignit\n"
        "B. 3. Pertambangan Bijih Logam\n"
        "B. 4. Pertambangan dan Penggalian Lainnya\n"
        "C. Industri Pengolahan\n"
        "C. 01. Industri Batubara dan Pengilangan Migas\n"
        "C. 01. a. Industri Batu Bara\n"
        "C. 01. b. Industri Pengilangan Migas\n"
        "C. 02. Industri Makanan dan Minuman\n"
        "C. 03. Pengolahan Tembakau\n"
        "C. 04. Industri Tekstil dan Pakaian Jadi\n"
        "C. 05. Industri Kulit, Barang dari Kulit dan Alas Kaki\n"
        "C. 06. Industri Kayu, Barang dari Kayu dan Gabus, Anyaman Bambu/Rotan\n"
        "C. 07. Industri Kertas, Percetakan, dan Reproduksi Media Rekaman\n"
        "C. 08. Industri Kimia, Farmasi dan Obat Tradisional\n"
        "C. 09. Industri Karet, Plastik\n"
        "C. 10. Industri Barang Galian bukan Logam\n"
        "C. 11. Industri Logam Dasar\n"
        "C. 12. Industri Barang Logam, Elektronik, Komputer, Optik\n"
        "C. 13. Industri Mesin dan Perlengkapan YTDL\n"
        "C. 14. Industri Alat Angkutan\n"
        "C. 15. Industri Furnitur\n"
        "C. 16. Industri Pengolahan Lainnya & Reparasi Mesin/Peralatan\n"
        "D. Pengadaan Listrik dan Gas\n"
        "D. 1. Ketenagalistrikan\n"
        "D. 2. Pengadaan Gas dan Produksi Es\n"
        "E. Pengadaan Air, Pengelolaan Sampah, Limbah, dan Daur Ulang\n"
        "F. Konstruksi\n"
        "G. Perdagangan Besar & Eceran; Reparasi Mobil & Sepeda Motor\n"
        "G. 1. Perdagangan Mobil, Sepeda Motor dan Reparasinya\n"
        "G. 2. Perdagangan Bukan Mobil/Sepeda Motor\n"
        "H. Transportasi dan Pergudangan\n"
        "H. 1. Angkutan Rel\n"
        "H. 2. Angkutan Darat\n"
        "H. 3. Angkutan Laut\n"
        "H. 4. Angkutan Sungai, Danau dan Penyeberangan\n"
        "H. 5. Angkutan Udara\n"
        "H. 6. Pergudangan, Pos dan Kurir\n"
        "I. Penyediaan Akomodasi dan Makan Minum\n"
        "I. 1. Akomodasi\n"
        "I. 2. Makan Minum\n"
        "J. Informasi dan Komunikasi\n"
        "K. Jasa Keuangan dan Asuransi\n"
        "K. 1. Perantara Keuangan\n"
        "K. 2. Asuransi dan Dana Pensiun\n"
        "K. 3. Jasa Keuangan Lainnya\n"
        "K. 4. Penunjang Keuangan\n"
        "L. Real Estate\n"
        "M,N. Jasa Perusahaan\n"
        "O. Administrasi Pemerintahan, Pertahanan, dan Jaminan Sosial Wajib\n"
        "P. Jasa Pendidikan\n"
        "Q. Kesehatan dan Kegiatan Sosial\n"
        "R,S,T,U. Jasa Lainnya\n\n"
        "Tentukan kategori utama dari teks berikut berdasarkan klasifikasi sektor ekonomi Indonesia.\n"
        "Jawab hanya dengan 1 huruf berikut tanpa penjelasan apapun: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, atau U.\n\n"
        f"Teks: \"{text}\"\n\nKategori:"
    )

# Fungsi utama untuk dipakai di app.py
def classify(summary_text):
    try:
        prompt = get_prompt(summary_text)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        label = response.choices[0].message.content.strip()
        return label
    except Exception as e:
        print(f"⚠️ Error saat klasifikasi: {e}")
        return "ERROR"
