import hashlib
import requests
import json
from time import time
from urllib.parse import urlparse


class Blockchain(object):
    def __init__(self):
        self.balance = []
        self.current_transactions = []
        self.chain = []
        self.vvv_new_block(previous_hash='Vronskiy', proof=16052002)
        self.nodes = set()

    def vvv_register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

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

    def vvv_valid_chain(self, chain):

        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
        print(f'{last_block}')
        print(f'{block}')
        print("\n-----------\n")

        if block['previous_hash'] != self.hash(last_block):
            return False

        if not self.valid_proof(last_block['proof'], block['proof']):
            return False

        last_block = block

        current_index += 1
        return True

    def resolve_conflicts(self):

        neighbours = self.nodes
        new_chain = None

        # Шукаємо тільки ланцюги, довші за наші
        max_length = len(self.chain)

        # Захоплюємо і перевіряємо всі ланцюги з усіх вузлів мережі
        for node in neighbours:
            print(node)
            response = requests.get(f'http://{node}/vvv_chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
            if length > max_length and self.vvv_valid_chain(chain):
                max_length = length
                new_chain = chain

        # Замінюємо ланцюг, якщо знайдемо інший валідний і довший
        if new_chain:
            self.chain = new_chain
            return True

        return False
