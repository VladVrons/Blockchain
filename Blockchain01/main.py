import Blockchain as ch
import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = ch.Blockchain()


@app.route('/vvv_mine', methods=['GET'])
def vvv_mine():
    # Запускаємо алгоритм підтвердження роботи, щоб отримати наступний пруф
    last_block = blockchain.vvv_last_block
    last_proof = last_block['proof']
    proof = blockchain.vvv_proof_of_work(last_proof)

    # Повинні отримати винагороду за знайдене підтвердження
    # Відправник "0" означає, що вузол заробив коін
    blockchain.vvv_new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=5,
    )

    # Створюємо новий блок, шляхом внесення його в ланцюг
    previous_hash = blockchain.vvv_hash(last_block)
    block = blockchain.vvv_new_block(proof, previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/vvv_chain', methods=['GET'])
def vvv_full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/transaction', methods=['POST'])
def vvv_new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.vvv_new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/vvv_balance', methods=['POST'])
def vvv_balance():

    values = request.get_json()
    required = ['recipient']
    total = 0
    if not all(k in values for k in required):
        return 'Missing values', 400

    for a in blockchain.chain:
        for tr in a['transactions']:
            if tr['recipient'] == values:
                total += int(tr['amount'])
    response = {'message': f'Total balance = {total}'}
    return jsonify(response), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
