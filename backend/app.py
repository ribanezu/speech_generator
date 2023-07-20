from flask import Flask, request, jsonify
from flask_cors import CORS

from process import process_files, query_collection, query_collection_knowledge, process_files_knowledge

app = Flask(__name__)
CORS(app)


@app.route('/process', methods=['POST'])
def process():
    documents = request.files.getlist('documents')
    process_files(documents)
    response = {'success': True}
    return jsonify(response)

@app.route('/process_knowledge', methods=['POST'])
def process_knowledge():
    documents = request.files.getlist('knowledge')
    process_files_knowledge(documents)
    response = {'success': True}
    return jsonify(response)


@app.route('/query', methods=['GET'])
def query():
    query = request.args.get('text')
    results = query_collection(query)
    return jsonify(results)

@app.route('/query_knowledge', methods=['GET'])
def query_knowledge():
    query = request.args.get('text')
    results = query_collection_knowledge(query)
    return jsonify(results)


if __name__ == '__main__':
    app.run()
