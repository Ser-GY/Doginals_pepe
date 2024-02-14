# Doginals

A minter and protocol for inscriptions on Dogecoin. 

## ⚠️⚠️⚠️ Important ⚠️⚠️⚠️

Use this wallet for inscribing only! Always inscribe from this wallet to a different address, e.g. one you created with DogeLabs or Doggy Market. This wallet is not meant for storing funds or inscriptions.

## Prerequisites

This guide requires a bit of coding knowledge and running Ubuntu on your local machine or a rented one. To use this, you'll need to use your terminal to setup a Dogecoin node, clone this repo and install Node.js on your computer.

### Setup Dogceoin node

Follow the instructions here to setup and sync your Dogecoin node: (https://dogecoin.com/dogepedia/how-tos/operating-a-node/#linux-instructions)

From root directory:

Download the latest Linux build from the Dogecoin Github repository:
```
wget https://github.com/dogecoin/dogecoin/releases/download/v1.14.6/dogecoin-1.14.6-x86_64-linux-gnu.tar.gz
``` 

Untar and unzip the package you just downloaded
```
tar -xvzf dogecoin-1.14.6-x86_64-linux-gnu.tar.gz
```

Enter into the bin directory inside the directory where Dogecoin Core has been untarred:
```
cd dogecoin-1.14.6/bin
```

Start the headless Dogecoin Daemon process:
```
./dogecoind -daemon
```

The Dogecoin Daemon is now starting.

You can now use the dogecoin-cli tool to interact with Dogecoin Core’s JSON-RPC interface. Use the help command for a list of all available commands.
```
dogecoin-cli help
```

To get help on a specific command:
```
dogecoin-cli help getblock 
```

You can follow the synching process by reading the contents of the debug.log file contained in the data directory. Go into the data directory of .dogecoin in root, and type the following command:
```
tail -f debug.log
```

In most setups, you can stop “listening” to the output of the debug.log file by pressing CTRL+C

For more information on using Dogecoin CLI refer to the Dogecoin CLI section. Additional configuration settings can be found in the Advanced Configuration section. For example, if you are not using Dogecoin Core as a wallet, it might be a good idea to disable the wallet functionality altogether.


### Install NodeJS

Please head over to (https://github.com/nodesource/distributions#using-ubuntu) and follow the installation instructions.

## Setup Minter

### git clone and install

Install by git clone (requires git and node on your computer) 

#### Clone the repo
```
git clone https://github.com/Ser-GY/Doginals_pepe.git
```
#### Instell dependencies

```
cd Doginals_pepe
npm install
``` 

After all dependencies are solved, you can configure the environment:

### Configure environment

Create a `.env` file in the Doginals_pepe directory with your node information. Set your own username/password. Keep the rest as is.

```
NODE_RPC_URL=http://127.0.0.1:22555/
NODE_RPC_USER=ape
NODE_RPC_PASS=zord
TESTNET=false
FEE_PER_KB=500000000
```
You can get the current fee per kb from [here](https://blockchair.com/).

Create a `dogecoin.conf` at `/root/.dogecoin` folder. Set your own username/password the same as the .env file. Keep the rest as is.

```
rpcuser=ape
rpcpassword=zord
rpcport=22555
server=1
listen=1
txidex=1
```
## Server Start/Stop

Be in dogecoin-1.14.6/bin 
```
cd dogecoin-1.14.6/bin
```
To stop doge server:
```
./dogecoin-cli stop
```
To start doge server: 
```
./dogecoind -daemon
```

## Funding
Be in the the Doginals_pepe directory for the following commands:
```
cd Doginals_pepe
```
Generate a new `.wallet.json` file:

```
node . wallet new
```

Then send DOGE to the address displayed. Once sent, sync your wallet:

```
node . wallet sync
```

If you are minting a lot, you can split up your UTXOs:

```
node . wallet split <count>
```

When you are done minting, send the funds back:

```
node . wallet send <address> <optional amount>
```

## Minting

From file:

```
node . mint <address> <path>
```

From data:

```
node . mint <address> <content type> <hex data>
```

Examples:

```
node . mint DSV12KPb8m5b6YtfmqY89K6YqvdVwMYDPn dog.jpeg
```

```
node . mint DSV12KPb8m5b6YtfmqY89K6YqvdVwMYDPn "text/plain;charset=utf-8" 576f6f6621 
```

**Note**: Please use a fresh wallet to mint to with nothing else in it until proper wallet for doginals support comes. You can get a paper wallet [here](https://www.fujicoin.org/wallet_generator?currency=Dogecoin).

## DRC-20

```
node . drc-20 mint <address> <ticker> <amount>
```

Examples: 

```
node . drc-20 mint DSV12KPb8m5b6YtfmqY89K6YqvdVwMYDPn dogi 1000
```

## Viewing

Start the server:

```
node . server
```

And open your browser to:

```
http://localhost:3000/tx/15f3b73df7e5c072becb1d84191843ba080734805addfccb650929719080f62e
```

## Protocol

The doginals protocol allows any size data to be inscribed onto subwoofers.

An inscription is defined as a series of push datas:

```
"ord"
OP_1
"text/plain;charset=utf-8"
OP_0
"Woof!"
```

For doginals, we introduce a couple extensions. First, content may spread across multiple parts:

```
"ord"
OP_2
"text/plain;charset=utf-8"
OP_1
"Woof and "
OP_0
"woof woof!"
```

This content here would be concatenated as "Woof and woof woof!". This allows up to ~1500 bytes of data per transaction.

Second, P2SH is used to encode inscriptions.

There are no restrictions on what P2SH scripts may do as long as the redeem scripts start with inscription push datas.

And third, inscriptions are allowed to chain across transactions:

Transaction 1:

```
"ord"
OP_2
"text/plain;charset=utf-8"
OP_1
"Woof and "
```

Transaction 2

```
OP_0
"woof woof!"
```

With the restriction that each inscription part after the first must start with a number separator, and number separators must count down to 0.

This allows indexers to know how much data remains.

## FAQ

### I'm getting ECONNREFUSED errors when minting

There's a problem with the node connection. Your `dogecoin.conf` file should look something like:

```
rpcuser=ape
rpcpassword=zord
rpcport=22555
server=1
```

Make sure `port` is not set to the same number as `rpcport`. Also make sure `rpcauth` is not set.

Your `.env file` should look like:

```
NODE_RPC_URL=http://127.0.0.1:22555
NODE_RPC_USER=ape
NODE_RPC_PASS=zord
TESTNET=false
```

### I'm getting "insufficient priority" errors when minting

The miner fee is too low. You can increase it up by putting FEE_PER_KB=300000000 in your .env file or just wait it out. The default is 100000000 but spikes up when demand is high.

——Changing-Wallets———

Inside of /root/.dogecoin
cp wallet.dat /root/saved_wallets/wallet02
cp wallet.dat /root/.dogecoin

Inside of /root/Doginals_pepe
cd /root/Doginals_pepe
cp .wallet.json /root/saved_wallets/wallet02
cp .wallet.json /root/Doginals_pepe

Inside of /root/saved_wallets

mkdir wallet03
nano wallet03.txt

Enter the address and save

Inside of /root/.dogecoin
rm wallet.dat

Inside of /root/Doginals_pepe
rm .wallet.json

Make new wallet:
Be inside /root/Doginals_pepe
cd Doginals_pepe

node . wallet new


———End———

—name—
node . mint DFh6dtqDwqtz7xwfp4Js4hycMfP9oYG8HW "text/plain;charset=utf-8" 646269742e646f6765
——

./dogecoin-cli getreceivedbyaddress DFh6dtqDwqtz7xwfp4Js4hycMfP9oYG8HW

———art mint———
node . mint DFh6dtqDwqtz7xwfp4Js4hycMfP9oYG8HW /root/node_runners/100.png
————end———-

node . drc-20 mint DFh6dtqDwqtz7xwfp4Js4hycMfP9oYG8HW shit 10


———bulk mints———
./bulk-mint1.sh 20 DFh6dtqDwqtz7xwfp4Js4hycMfP9oYG8HW shit 10

./bulk-mint.sh 25 DFh6dtqDwqtz7xwfp4Js4hycMfP9oYG8HW shit 10
————end————


cp .wallet.json /root/saved_wallets/wallet01

