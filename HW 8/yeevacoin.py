import sys, rsa, hashlib
from datetime import datetime

# the time zone is hardcoded to avoid unecessary dependcencies
# how to verify that statements aren't added to mempool multiple times?

COIN_NAME = "yeevacoin"
GENESIS_BLOCK = "The virtues are natural adjuncts of the pleasant life and the pleasant life is inseparable from them."
NUM_KEY_BITS = 1024
TAG_LENGTH = 16

# generate functionality
def read_key_from_file(fileName, keyType):
    with open(fileName, 'r') as file:
        key_data = ''
        begin_marker = f'-----BEGIN RSA {keyType} KEY-----'
        end_marker = f'-----END RSA {keyType} KEY-----'
        for line in file:
            if begin_marker in line:
                key_data += line
                while True:
                    next_line = file.readline()
                    key_data += next_line
                    if end_marker in next_line:
                        break
                break
    if keyType == 'PUBLIC':
        return rsa.PublicKey.load_pkcs1(key_data.encode('utf-8'))
    else:
        return rsa.PrivateKey.load_pkcs1(key_data.encode('utf-8'))  

def create_wallet(fileName):
    (public_key, private_key) = rsa.newkeys(NUM_KEY_BITS)
    with open(fileName, 'w') as file:
        file.write(public_key.save_pkcs1().decode('utf-8') + '\n')
        file.write(private_key.save_pkcs1().decode('utf-8') + '\n')

    tag = hashlib.sha256(public_key.save_pkcs1()).hexdigest()[:TAG_LENGTH]
    print(f"New wallet generated in '{fileName}' with tag {tag}")

# address functionality
def get_wallet_tag(fileName):
    publicKey = read_key_from_file(fileName, 'PUBLIC')
    tag = hashlib.sha256(publicKey.save_pkcs1()).hexdigest()[:TAG_LENGTH]
    return tag

# fund functionality; transactions automatically verified
def fund(receiverTag, amount, statementFile):
    date = str(datetime.now().strftime("%a %b %d %H:%M:%S EDT %Y"))
    statement = f"From: my_heart\nTo: {receiverTag}\nAmount: {amount}\nDate: {date}\n"
    with open(statementFile, 'a') as file:
        file.write(statement)
    
    with open("mempool.txt", 'a') as mempool:
        mempool.write(f"my_heart transferred {amount} to {receiverTag} on {date}\n")

    print(f"Funded wallet {receiverTag} with {amount} yeevacoin on {date}")

# transfer functionality
def transfer(senderWalletFile, receiverTag, amount, statementFile):
    date = str(datetime.now().strftime("%a %b %d %H:%M:%S EDT %Y"))
    statement = f"From: {get_wallet_tag(senderWalletFile)}\nTo: {receiverTag}\nAmount: {amount}\nDate: {date}\n"
    senderPrivateKey = read_key_from_file(senderWalletFile, 'PRIVATE')
    signature = rsa.sign(statement.encode('utf-8'), senderPrivateKey, 'SHA-256')

    with open(statementFile, 'a') as file:
        file.write(statement + "\n" + signature.hex())

    print(f"Transferred {amount} yeevacoin from {senderWalletFile} to {receiverTag} and the statement to {statementFile} on {date}")

# balance functionality
def parse_transaction_line(line, walletTag):
    parts = line.split()
    sender = parts[0]
    amount = int(parts[2])
    receiver = parts[4]

    if sender == walletTag:
        return -1 * amount
    elif receiver == walletTag:
        return amount
    return 0

def scan_block(walletTag, block):
    balance = 0
    with open(block, 'r') as currBlockFile:
        for line in currBlockFile:
            if 'transferred' in line:
                balance += parse_transaction_line(line, walletTag)
    return balance

def balance(walletTag):
    balance = 0
    currBlockNum = 0
    while True:
        try:
            balance += scan_block(walletTag, f'block_{currBlockNum}.txt')
        except FileNotFoundError:
            break
        currBlockNum += 1
    
    try:
        balance += scan_block(walletTag, 'mempool.txt')
    except FileNotFoundError:
        pass

    return balance

# verify functionality
def verify(senderWalletFile, statementFile):
    with open(statementFile, 'r') as file:
        lines = file.readlines()
        statement = ''.join(lines[:-2]) # account for newline before signature
        signature = bytes.fromhex(lines[-1].strip())

    senderPublicKey = read_key_from_file(senderWalletFile, 'PUBLIC')
    try:
        rsa.verify(statement.encode('utf-8'), signature, senderPublicKey)

        
    except rsa.VerificationError:
        print(f"The transaction in file {statementFile} with wallet {senderWalletFile} is not valid.")
        return False
    
    with open("mempool.txt", 'a') as mempool:
        mempool.write(f"{lines[0][6:].strip()} transferred {lines[2][8:].strip()} to {lines[1][4:].strip()} on {lines[3][6:].strip()}\n")
    
    print(f"The transaction in file {statementFile} with wallet {senderWalletFile} is valid, and was written to the mempool")

if sys.argv:
    match sys.argv[1]:
        case "name": print(COIN_NAME)
        case "genesis": 
            with open('block_0.txt', 'w') as file:
                file.write(GENESIS_BLOCK)
            print(f"Genesis block written to block_0.txt")
        case "generate": create_wallet(sys.argv[2])
        case "address": print(get_wallet_tag(sys.argv[2]))
        case "fund": fund(sys.argv[2], sys.argv[3], sys.argv[4])
        case "transfer": transfer(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        case "balance": print(balance(sys.argv[2]))
        case "verify": verify(sys.argv[2], sys.argv[3])
        case _:
            pass