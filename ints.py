import main.py as m
from flask import Flask, request
import requests

app = Flask(__name__)

blockchain = m.BlockChain()

@app.route("/newTra")
