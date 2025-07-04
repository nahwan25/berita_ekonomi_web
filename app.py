from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
from scrapper import scrape
from summarizer import summarize
from classifier import classify
import threading, uuid
import csv
from io import StringIO

app = Flask(__name__)
TASKS: dict[str, dict] = {}  # task_id ➜ {"total":N, "done":0, "rows":[], "finished":bool}

# ──────────────── Background worker ────────────────
def worker(task_id: str, keyword: str, max_articles: int):
    art_list = scrape(keyword, max_articles)
    TASKS[task_id]["total"] = len(art_list)

    for art in art_list:
        isi = art.get("content", "").strip()
        if len(isi) < 30:
            art["summary"] = "Teks kosong"
            art["kategori"] = "R"
        else:
            art["summary"] = summarize(isi)
            art["kategori"] = classify(art["summary"])

        TASKS[task_id]["rows"].append(art)
        TASKS[task_id]["done"] += 1

    TASKS[task_id]["finished"] = True

# ──────────────── Routes ────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        max_raw = request.form.get("max_articles", "20").strip()
        max_art = int(max_raw) if max_raw.isdigit() else 20

        task_id = uuid.uuid4().hex[:8]
        TASKS[task_id] = {"total": 0, "done": 0, "rows": [], "finished": False}

        t = threading.Thread(target=worker, args=(task_id, keyword, max_art), daemon=True)
        t.start()

        return redirect(url_for("progress", task_id=task_id))

    return render_template("index.html")

@app.route("/progress/<task_id>")
def progress(task_id):
    if task_id not in TASKS:
        return "Task not found", 404
    return render_template("progress.html", task_id=task_id)

@app.route("/status/<task_id>")
def status(task_id):
    data = TASKS.get(task_id)
    if not data:
        return jsonify({"error": "task not found"}), 404
    return jsonify({
        "total": data["total"],
        "done": data["done"],
        "rows": data["rows"],
        "finished": data["finished"]
    })

@app.route("/download/<task_id>")
def download(task_id):
    data = TASKS.get(task_id)
    if not data or not data.get("finished"):
        return "Data belum siap atau task tidak ditemukan.", 404

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["site", "tanggal", "title", "summary", "kategori", "link"])

    for item in data["rows"]:
        writer.writerow([
            item.get("site", ""),
            item.get("tanggal", ""),
            item.get("title", ""),
            item.get("summary", ""),
            item.get("kategori", ""),
            item.get("link", "")
        ])

    output.seek(0)
    return Response(output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment;filename=berita_{task_id}.csv"})

if __name__ == "__main__":
    app.run(debug=True)
