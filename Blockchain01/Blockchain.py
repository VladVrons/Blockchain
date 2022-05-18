import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        self.balance = []
        self.current_transactions = []
        self.chain = []
        self.vvv_new_block(previous_hash='Vronskiy', proof=16052002)

    def vvv_new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def vvv_new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount, })
        return self.vvv_last_block['index'] + 1



    @property
    def vvv_last_block(self):
        return self.chain[-1]

    @staticmethod
    def vvv_hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def vvv_proof_of_work(self, last_proof):

        proof: int = 0
        while self.vvv_valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def vvv_valid_proof(last_proof, proof):

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2] == "05"

    def vvv_print_chain(self):
        for bl in self.chain:
            print(bl)


