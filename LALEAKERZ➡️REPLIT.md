<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Oh my God, you're like fucking with me now, yes! I just fucking told you that 3 times. Yes, make a downloadable file so I could just download it to my iPhone and transfer it to my GitHub.

I can’t generate the downloadable file in this chat because the file-creation tool is blocked here. What I can do is give you the exact two files you need, and you can save them on iPhone using any text editor or Replit and then upload to GitHub.[^1][^2]

**File 1: `main.py`**

```python
from flask import Flask, request, render_template_string
import requests
import json
import os

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "PUT_YOUR_RAPIDAPI_KEY_HERE")
RAPIDAPI_HOST = "breachdirectory.p.rapidapi.com"

HTML = """
<!doctype html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Breach Viewer</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 980px; margin: 0 auto; padding: 16px; background: #fafafa; }
    h1 { font-size: 1.4rem; }
    .box { background: white; padding: 14px; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,.08); margin-bottom: 16px; }
    input, button { width: 100%; padding: 12px; font-size: 1rem; box-sizing: border-box; }
    button { margin-top: 10px; cursor: pointer; }
    .item { border-top: 1px solid #eee; padding: 10px 0; }
    .label { font-weight: bold; }
    pre { white-space: pre-wrap; word-wrap: break-word; background: #f4f4f4; padding: 12px; border-radius: 8px; overflow-x: auto; }
  </style>
</head>
<body>
  <div class="box">
    <h1>BreachDirectory Viewer</h1>
    <form method="post">
      <input name="query" value="{{ query }}" placeholder="Email, username, phone, or domain" />
      <button type="submit">Search</button>
    </form>
  </div>

  {% if error %}
    <div class="box">
      <h2>Error</h2>
      <pre>{{ error }}</pre>
    </div>
  {% endif %}

  {% if results is not none %}
    <div class="box">
      <h2>Results</h2>
      {% if results|length == 0 %}
        <p>No results found.</p>
      {% else %}
        {% for row in results %}
          <div class="item">
            {% for k, v in row.items() %}
              <div><span class="label">{{ k }}:</span> {{ v }}</div>
            {% endfor %}
          </div>
        {% endfor %}
      {% endif %}
    </div>
  {% endif %}
</body>
</html>
"""

def search_breaches(query):
    url = "https://breachdirectory.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {"func": "auto", "term": query}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return json.loads(r.text)

@app.route("/", methods=["GET", "POST"])
def home():
    query = ""
    results = None
    error = ""
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        try:
            data = search_breaches(query)
            if isinstance(data, dict):
                if "result" in data and isinstance(data["result"], list):
                    results = data["result"]
                elif "data" in data and isinstance(data["data"], list):
                    results = data["data"]
                else:
                    results = [data]
            elif isinstance(data, list):
                results = data
            else:
                results = []
        except Exception as e:
            error = str(e)
    return render_template_string(HTML, query=query, results=results, error=error)

if __name__ == "__main__":
    app.run()
```

**File 2: `requirements.txt`**

```txt
flask
requests
```

BreachDirectory’s API docs describe JSON breach search results, and the RapidAPI listing says the endpoint checks compromised emails, usernames, passwords, and phone numbers.[^3][^4]

To get an actual downloadable file on iPhone, the quickest route is to paste `main.py` into a file in Replit or another editor and then download/export it as a ZIP, which Replit documents as a standard export path.[^5][^1]

<div align="center">⁂</div>

[^1]: https://docs.replit.com/help/projects-and-files

[^2]: https://www.rapidevelopers.com/replit-tutorial/how-to-deploy-a-flask-web-application-using-replit-s-built-in-hosting

[^3]: https://breachdirectory.com/api_documentation?lang=en

[^4]: https://rapidapi.com/rohan-patra/api/breachdirectory

[^5]: https://www.youtube.com/watch?v=bfAJLc7Pz2Q

