# NonCoin

What is NonCoin?
NonCoin is a new cryptocurrency for nobody. 
I don't know reason of creation NonCoin.
Because I don't like programming without invention I invented new way of mining: If you want mine o NonCoin, upload a photo with 
your address in description to Instagram and inform Blockchain about this fact.

How to start
If you want use a NonCoin you can use my NonCoin client.
git clone https://github.com/pantrombka/NonCoin.git

cd NonCoin

On the beggining you must set a node. If you don't create a node, client will use a default node.
python client.py setnode <url>

If you want to generate wallet:
```
python client.py generate
```
It will create three files:
address.txt
private.txt
public.txt

if you want to check balance
```
python client.py balance
```
if you want to send NonCoin to other user
```
python client.py send <address> <amount>
```

if you want to mine  NonCoin you must add photo to instagram, add your address to caption of this photo. Next run command
```
python client.py mine <url>
```
where <url> is a fragment of url after 'https://www.instagram.com/p/'
Example: https://www.instagram.com/p/BdyJBpSAWLI
```
python client.py mine BdyJBpSAWLI
```

Version -1=-5-0.5+0.5+1-0.5+0.5+1-0.5+0.5+1+1-2+2+1-1
--------------------------------------------------
-5: this is small projects. I thought I can create in two days. Because I have enought free time to my hobby projects I estimate project size to 5 days. So it was 5 days to finish

-0.5: learning about blockchain;
+0.5: learning about blockchain;
+1: definition of Block;
-0.5: thinking about method of minining;
+0.5: thinking about method of minining;
+1: Instagram and mining;
-0.5: learning about peers in blockchain;
+0.5: learning about peers in blockchain;
+1: Adding Peers;
+1: Sending method;
-2: problems with cryptography;
+2: problems with cryptography fixed;
+1: Creation of wallet tests;
-1: I must polish add peer method;

This is first use of this way of versioning so it isn't perfect. I must little change it, but main idea is good. 

