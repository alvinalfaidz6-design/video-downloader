import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)

# Folder tempat menyimpan hasil download sementara
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Tampilan HTML Website
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All-in-One Video Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #0f172a;
            color: #ffffff;
            text-align: center;
            padding: 20px;
            margin: 0;
        }
        .container {
            max-width: 500px;
            margin: 50px auto;
            background: #1e293b;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        h2 { margin-bottom: 10px; color: #38bdf8; }
        p { color: #94a3b8; font-size: 14px; margin-bottom: 25px; }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #475569;
            background: #0f172a;
            color: #fff;
            font-size: 16px;
            box-sizing: border-box;
            margin-bottom: 15px;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #0284c7;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: #0369a1; }
        .result {
            margin-top: 20px;
            font-size: 14px;
        }
        a.download-link {
            display: inline-block;
            margin-top: 10px;
            padding: 10px 20px;
            background: #22c55e;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
        }
        .error { color: #f87171; }
    </style>
</head>
<body>

    <div class="container">
        <h2>Video Downloader</h2>
        <p>Download video TikTok, YouTube, IG, & FB otomatis!</p>
        
        <form method="POST">
            <input type="text" name="url" placeholder="Tempel link video di sini..." required>
            <button type="submit">Proses Download</button>
        </form>

        {% if download_url %}
        <div class="result">
            <p style="color: #4ade80;">Video berhasil diproses!</p>
            <a class="download-link" href="{{ download_url }}">Klik Disini Untuk Simpan Video</a>
        </div>
        {% endif %}

        {% if error %}
        <div class="result">
            <p class="error">Gagal: {{ error }}</p>
        </div>
        {% endif %}

        <div style="margin-top: 25px; font-size: 12px; color: #64748b;">
            Support: YouTube • TikTok • Instagram • Facebook
        </div>
    </div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    download_url = None
    error = None
    if request.method == 'POST':
        video_url = request.form.get('url')
        try:
            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
                'format': 'best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                # Ambil nama file saja untuk didownload user
                basename = os.path.basename(filename)
                download_url = f"/download/{basename}"
        except Exception as e:
            error = str(e)

    return render_template_string(HTML_TEMPLATE, download_url=download_url, error=error)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
