import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Aplicação no Elastic Beanstalk funcionando!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="127.0.0.1", port=port)
