import sys, rsa, hashlib

COIN_NAME = "yeevacoin"
GENESIS_BLOCK = "The virtues are natural adjuncts of the pleasant life and the pleasant life is inseparable from them."
NUM_KEY_BITS = 1024
TAG_LENGTH = 16

def create_wallet(fileName):
    (public_key, private_key) = rsa.newkeys(NUM_KEY_BITS)
    with open(fileName, 'w') as file:
        file.write(public_key.save_pkcs1().decode('utf-8') + '\n')
        file.write(private_key.save_pkcs1().decode('utf-8') + '\n')

    tag = hashlib.sha256(public_key.save_pkcs1()).hexdigest()[:TAG_LENGTH]
    print(f"New wallet generated in '{fileName}' with tag {tag}")
   
if sys.argv:
    match sys.argv[1]:
        case "name": print(COIN_NAME)
        case "genesis": 
            with open('block_0.txt', 'w') as file:
                file.write(GENESIS_BLOCK)
            print(f"Genesis block written to block_0.txt")
        case "generate": create_wallet(sys.argv[2])
        case _:
            pass