from flask import Flask, jsonify, request
from rdflib import Graph
from owl2jsonschema import parse_graph
import time
import os

OWL_DB = os.environ.get("OWL_DB", "http://localhost:3030/test")
OWL_DB_TYPE = os.environ.get("OWL_DB_TYPE", "turtle")

UPDATE_INTERVAL = int(os.environ.get("UPDATE_INTERVAL", "10"))

app = Flask(__name__)

last_upd = 0
schema = None
schema_full = None

@app.route('/')
def root():
    return "OK!"

@app.route('/<string:_cls>', methods=['GET'])
def parse_class(_cls):
    global last_upd, schema, schema_full
    now = time.time()
    if now - last_upd > UPDATE_INTERVAL:
        app.logger.warning("Updating schemas!")
        g = Graph()
        g.parse(OWL_DB, format=OWL_DB_TYPE)
        schema = parse_graph(g, skip_ontology_name=True, skip_class_name=True)
        schema_full = parse_graph(g, skip_ontology_name=True, skip_class_name=False)
        last_upd = time.time()
    if _cls in schema:
        return jsonify(schema[_cls])
    else:
        return jsonify({}), 404


@app.route('/full', methods=['POST'])
def parse_class_full():
    global last_upd, schema, schema_full
    _cls = request.form.get('iri', None)

    app.logger.warning(f"Fetch {_cls}")
    
    if not _cls:
        return jsonify({}), 401
    
    now = time.time()
    if now - last_upd > UPDATE_INTERVAL:
        app.logger.warning("Updating schemas!")
        g = Graph()
        g.parse(OWL_DB, format=OWL_DB_TYPE)
        schema = parse_graph(g, skip_ontology_name=True, skip_class_name=True)
        schema_full = parse_graph(
            g, skip_ontology_name=True, skip_class_name=False)
        last_upd = time.time()
    # app.logger.warning(f"IRI: {_cls}")
    if _cls in schema_full:
        return jsonify(schema_full[_cls])
    else:
        return jsonify({}), 404
