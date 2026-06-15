from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import os

API_KEY = "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"

class MiServidor(BaseHTTPRequestHandler):

    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        pregunta = params.get("q", [""])[0]

        respuesta = ""

        if pregunta:
            try:
                r = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [
                            {"role": "user", "content": pregunta}
                        ]
                    }
                )

                data = r.json()

                if "choices" in data:
                    respuesta = data["choices"][0]["message"]["content"]
                else:
                    respuesta = str(data)

            except Exception as e:
                respuesta = f"Error: {e}"

        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>JurisAI</title>
            <style>
                body {{
                    font-family: Arial;
                    background: #0f172a;
                    color: white;
                    text-align: center;
                    margin-top: 50px;
                }}

                input {{
                    padding: 12px;
                    width: 320px;
                    border-radius: 10px;
                    border: none;
                }}

                button {{
                    padding: 12px 20px;
                    border-radius: 10px;
                    background: #3b82f6;
                    color: white;
                    border: none;
                    cursor: pointer;
                }}

                .box {{
                    margin-top: 30px;
                    padding: 20px;
                    background: #1e293b;
                    border-radius: 15px;
                    display: inline-block;
                    max-width: 650px;
                    text-align: left;
                }}
            </style>
        </head>

        <body>
            <h1>⚖️ JurisAI</h1>

            <form method="GET">
                <input name="q" placeholder="Pregunta jurídica...">
                <button>Enviar</button>
            </form>

            <div class="box">
                <h3>Respuesta:</h3>
                <p>{respuesta}</p>
            </div>

        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(html.encode("utf-8"))


PORT = int(os.environ.get("PORT", 8000))
servidor = HTTPServer(("0.0.0.0", PORT), MiServidor)

print("JurisAI listo")
servidor.serve_forever()