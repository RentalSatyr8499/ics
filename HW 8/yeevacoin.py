import sys, rsa, hashlib
from datetime import datetime

# the time zone is hardcoded to avoid unecessary dependcencies

COIN_NAME = "yeevacoin"
GENESIS_BLOCK = "The virtues are natural adjuncts of the pleasant life and the pleasant life is inseparable from them."
NUM_KEY_BITS = 1024
TAG_LENGTH = 16

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

def get_wallet_tag(fileName):
    publicKey = read_key_from_file(fileName, 'PUBLIC')
    tag = hashlib.sha256(publicKey.save_pkcs1()).hexdigest()[:TAG_LENGTH]
    return tag

def fund(receiverTag, amount, statementFile):
    date = str(datetime.now().strftime("%a %b %d %H:%M:%S EDT %Y"))
    statement = f"From: my_heart\nTo: {receiverTag}\nAmount: {amount}\nDate: {date}\n"
    with open(statementFile, 'a') as file:
        file.write(statement)

    print(f"Funded wallet {receiverTag} with {amount} yeevacoin on {date}")

def transfer(senderWalletFile, receiverTag, amount, statementFile):
    date = str(datetime.now().strftime("%a %b %d %H:%M:%S EDT %Y"))
    statement = f"From: {get_wallet_tag(senderWalletFile)}\nTo: {receiverTag}\nAmount: {amount}\nDate: {date}\n"
    senderPrivateKey = read_key_from_file(senderWalletFile, 'PRIVATE')
    signature = rsa.sign(statement.encode('utf-8'), senderPrivateKey, 'SHA-256')

    senderTag = get_wallet_tag(senderWalletFile)
    with open(statementFile, 'a') as file:
        file.write(statement + "\n" + signature.hex())

    print(f"Transferred {amount} yeevacoin from {senderWalletFile} to {receiverTag} and the statement to {statementFile} on {date}")

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
        case _:
            pass