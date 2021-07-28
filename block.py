import json
import os
import hashlib

BLOCKCHAIN_DIR = 'blockchain/'


def get_hash(prev_block,nonce):

    with open(BLOCKCHAIN_DIR + prev_block, 'rb') as f:
        content = f.read()
        content += str(nonce).encode('utf-8')
    return hashlib.sha256(content).hexdigest()

def check_integrity():
    files = sorted(os.listdir(BLOCKCHAIN_DIR), key=lambda x: int(x))
    
    results = []

    for file in files[1:]:
        with open(BLOCKCHAIN_DIR + file) as f:
            block =json.load(f)
        
        prev_hash = block.get('prev_block').get('hash')
        prev_filename= block.get('prev_block').get('filename')
        prev_nonce = block.get('prev_block').get('nonceblock')
        actual_hash = get_hash(prev_filename, prev_nonce)

        if prev_hash == actual_hash:
            res = 'Ok'
        else:
            res = 'was Changed'
        print(f'Block {prev_filename}: {res}')
        results.append({'block': prev_filename,'results': res})
        
    return results


def write_block(borrower, lender, amount):

    blocks_count = len(os.listdir(BLOCKCHAIN_DIR))
    prev_block = str(blocks_count)
    mine_result, nonce_value = mine(prev_block)
    data =  {
        "borrower": borrower,
        "lender": lender,
        "amount": amount,
        "prev_block": {
            "hash": mine_result,
            "nonceblock": nonce_value,
            "filename": prev_block
        }
    }
    
    current_block = BLOCKCHAIN_DIR + str(blocks_count + 1)

    with open(current_block, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write('\n')

def mine(prev_block):
    nonce=0
    diff= int(prev_block)
    maxNonce = 2**32
    target = 2 ** (256-diff)
    for n in range(maxNonce):
        x = get_hash(prev_block,nonce)
        print("Mining... please wait nonce: ", n)
        #print("Current hash: ", x)
        if int(x, 16) <= target:
            print("Mining successful")

            return x, nonce
        else:
            nonce += 1

