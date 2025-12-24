import os
import warnings
from huggingface_hub import login
from pyngrok import conf

warnings.filterwarnings("ignore", category=UserWarning)

HF_TOKEN = os.getenv("HF_TOKEN")
NGROK_TOKEN = os.getenv("NGROK_TOKEN")

if HF_TOKEN:
    os.environ["HF_TOKEN"] = HF_TOKEN
    login(token=HF_TOKEN)

if NGROK_TOKEN:
    conf.get_default().auth_token = NGROK_TOKEN
