import os

from flask import request
from flask import Flask, make_response
import datetime
import time
import sys
import hashlib
import rsa
from base64 import b64encode, b64decode
import urllib2
from BeautifulSoup import BeautifulSoup
import json
import requests
from decimal import *
import pickle

keysize = 2048
peers = []


class Blockchain(object):
    def __init__(self):
        self.chain = []

    def set_chain(self, file):

        with open(file, 'rb') as handle:
            self.chain = pickle.load(handle)

    def add_block(self, transaction):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': transaction
        }
        self.chain.append(block)

    def previous_block(self, address):
        for i in self.chain[::-1]:
            if i["transactions"]["type"] == "send":
                if i["transactions"]["sender"] == address:
                    return str(i["transactions"])
        return str(self.chain[0]["transactions"])

    def is_new(self, url):
        for i in block.chain:
            if i["transactions"]["type"] == "mine":
                if i["transactions"]["url"] == url:
                    return False
        return True

    def block_length(self):
        return len(self.chain)

app = Flask(__name__)


def load_block(address):
    file_data = urllib2.urlopen(address + '/getblock')
    data_to_write = file_data.read()


    with open('block.json', 'wb') as handle:
        handle.write(data_to_write)
        #pickle.dump(data_to_write, handle, protocol=pickle.HIGHEST_PROTOCOL)

    block.set_chain('block.json')


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/getblock')
def get_block():
    file = pickle.dumps(block.chain)
    response = make_response(file)
    cd = 'attachment; filename=block.json'
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'application/json'
    return response


def save_block():
    block_file = block.chain

    with open('block.json', 'wb') as handle:
        pickle.dump(block_file, handle, protocol=pickle.HIGHEST_PROTOCOL)

@app.route('/addPeer')
def add_peer():
    peers.append('http://' + request.remote_addr + ':' + request.args.get('port'))
    return "Added"


@app.route('/getPeers')
def get_peers():
    return str(peers)


@app.route('/send')
def get_send():
    transaction = {
        'type': "send",
        'signature': str(request.args.get('signature')),
        'sender': request.args.get('sender'),
        'receiver': request.args.get('receiver'),
        'amount': request.args.get('amount'),
        'public_key': str(request.args.get('public_key'))
    }
    key_temp = rsa.importKey(transaction["public_key"])
    temp_address = hashlib.sha256(key_temp.exportKey('PEM').split("-----")[2]).hexdigest()
    h = hashlib.new('ripemd160')
    h.update(temp_address)
    temp_address = h.hexdigest()
    d = rsa.importKey(transaction['public_key'])
    block_hash = str(hashlib.md5(str(block.previous_block(transaction['sender']))).hexdigest())

    if (temp_address == transaction["sender"] and Decimal(balance(transaction["sender"])) >= Decimal(
            transaction["amount"]) and Decimal(transaction["amount"]) > 0 and rsa.verify(block_hash, b64decode(
            transaction['signature']), d)):
        block.add_block(transaction)
        if request.args.get('fromNode') != '1':
            for peer in peers:
                r = requests.get(peer + '/send?sender=' + request.args.get('sender') + '&receiver=' + request.args.get(
                    'receiver') + '&amount=' + request.args.get('amount') + '&public_key=' + request.args.get(
                    'public_key') + '&signature=' + request.args.get('signature') + '&fromNode=1')
        save_block()
        return "Sent"
    else:
        return "Not sent"


@app.route('/mine')
def get_mine():
    transaction = {
        'type': "mine",
        'who': request.args.get('who'),
        'url': request.args.get('url')}

    page = urllib2.urlopen('https://www.instagram.com/p/' + transaction['url']).read()
    soup = BeautifulSoup(page)
    soup.prettify()
    data = soup.findAll('script', type='text/javascript')
    data = json.loads(data[2].text.replace("window._sharedData = ", "")[:-1])
    rec1 = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"][
        "edge_media_to_caption"]["edges"][0]["node"]["text"].encode("utf-8")
    rec2 = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["caption_is_edited"]

    if transaction['who'] in rec1 and rec2 == False and block.is_new(transaction['url']) == True:
        block.add_block(transaction)
        if request.args.get('fromNode') != '1':
            for peer in peers:
                r = requests.get(
                    peer + '/mine?who=' + transaction['who'] + '&url=' + transaction['url'] + '&fromNode=1')
        save_block()
        return "Mined"
    else:
        return "Not mined"

@app.route('/previous')
def get_previous():
    address=request.args.get('address')
    return block.previous_block(address)

@app.route('/balance')
def get_balance():
    addr = request.args.get('address')
    return str(balance(addr))


def balance(address):
    balance_temp = Decimal(0.0)
    for i in block.chain:
        if i["transactions"]["type"] == "send":
            if i["transactions"]["receiver"] == address:
                balance_temp += Decimal(i["transactions"]["amount"])
            if i["transactions"]["sender"] == address:
                balance_temp -= Decimal(i["transactions"]["amount"])
        if i["transactions"]["type"] == "mine":
            if i["transactions"]["who"] == address:
                balance_temp += (Decimal(1) / Decimal(i["index"]))
    return balance_temp


if __name__ == '__main__':

    global block
    block = Blockchain()
    if len(sys.argv) > 1:
        load_block(sys.argv[1])
        peers.append(sys.argv[1])
        requests.get(sys.argv[1] + '/addPeer?port=' + sys.argv[2])
        app.run(debug=False, port=int(sys.argv[2]))

    else:
        if os.path.isfile("block.json"):
            block.set_chain("block.json")
        if block.block_length()==0:
            transaction = {
                'type': "root"
            }
            block.add_block(transaction)
        app.run(debug=False)
