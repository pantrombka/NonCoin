import sys
import rsa
import hashlib
from base64 import b64encode, b64decode
import urllib
import requests
keysize = 2048


def set_node(node):
    node_file = open("node.txt", "w")
    node_file.write(node)
    node_file.close()


def generate():
    (public, private) = rsa.newkeys(keysize)
    address = hashlib.sha256(public.exportKey(
        'PEM').split("-----")[2]).hexdigest()
    h = hashlib.new('ripemd160')
    h.update(address)
    address = h.hexdigest()
    address_file=open("address.txt","w")
    address_file.write(address)
    address_file.close()
    public_file=open("public.txt","w")
    public_file.write( b64encode(public.exportKey()))
    public_file.close()
    private_file=open("private.txt","w")
    private_file.write(b64encode(private.exportKey()))
    private_file.close()


def send(target,amount):
    try:
        node_file = open("node.txt", "r")
        node=node_file.read()
        node_file.close()
    except:
        print "Problem with node file."
        node_file = open("node.txt", "w")
        node_file.write('http://pantrombka.pythonanywhere.com/')
        node='http://pantrombka.pythonanywhere.com/'
        node_file.close()
    try:
        address=open("address.txt","r").read()
    except: print "Problem with wallet files. Please repair your wallet file or generate new."
    try:
        key64=open("public.txt","r").read()
    except: print "Problem with wallet files. Please repair your wallet file or generate new."
    try:
        priv=open("private.txt","r").read()
    except: print "Problem with wallet files. Please repair your wallet file or generate new."

    msg = requests.get(node+'/previous?address='+address).text

    a = rsa.importKey(priv)
    z = str(hashlib.md5(msg).hexdigest())
    signature = b64encode(rsa.sign(z, a, "SHA-512"))
    print requests.get(
        node+'/send?sender='+address+'&receiver='+target+'&amount='+amount+'&public_key=' + urllib.quote_plus(
            key64) + '&signature=' + urllib.quote_plus(signature) + '&fromNode=0').text


def mine(url):
    try:
        node_file = open("node.txt", "r")
        node = node_file.read()
        node_file.close()
    except:
        print "Problem with node file."
        node_file = open("node.txt", "w")
        node_file.write('http://pantrombka.pythonanywhere.com/')
        node = 'http://pantrombka.pythonanywhere.com/'
        node_file.close()
    try:
        address=open("address.txt","r").read()
    except: print "Problem with wallet files. Please repair your wallet file or generate new."

    print requests.get(node + '/mine?who=' + address + '&url=' + url + '&fromNode=0').text


def balance(address=None):
    try:
        node_file = open("node.txt", "r")
        node=node_file.read()
        node_file.close()
    except:
        print "Problem with node file."
        node_file = open("node.txt", "w")
        node_file.write('http://pantrombka.pythonanywhere.com/')
        node='http://pantrombka.pythonanywhere.com/'
        node_file.close()
    if address is None:
        try:
            address=open("address.txt","r").read()
        except: print "Problem with wallet files. Please repair your wallet file or generate new"
    print requests.get(node+'/balance?address='+address).text
if __name__=="__main__":
    argument=sys.argv[1]
    if(len(sys.argv)) > 1:
        argument = sys.argv[1]
    if argument=="setnode":
        set_node(sys.argv[2])
    if argument=="generate":
        generate()
    if argument=="balance":
        if len(sys.argv)==3:
            balance(sys.argv[2])
        else:
            balance()
    if argument=="mine":
        mine(sys.argv[2])
    if argument=="send":
        send(sys.argv[2],sys.argv[3])
