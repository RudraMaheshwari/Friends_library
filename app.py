import os
import subprocess
from flask import Flask

# Import your Streamlit main function
from src.run_streamlit import main

app = Flask(__name__)
streamlit_started = False


@app.route("/")
def start_streamlit():
    """
    This route is called by Vercel.
    It starts Streamlit only once and returns a simple response.
    """
    global streamlit_started

    if not streamlit_started:
        port = os.environ.get("PORT", "8080")

        # Launch streamlit as a subprocess
        subprocess.Popen([
            "streamlit", "run", "run_streamlit.py",
            "--server.port", port,
            "--server.headless", "true"
        ])

        streamlit_started = True

    return "Streamlit app starting..."


if __name__ == "__main__":
    app.run()
