import argparse
from rdflib.plugins.sparql import prepareQuery
import rdflib
import json
import sys


NON_REC_PROPERTY = rdflib.URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty")
REC_PROPERTY = rdflib.URIRef("http://www.w3.org/2002/07/owl#ObjectProperty")

TYPE_MAPPING = {
    rdflib.URIRef("http://www.w3.org/2001/XMLSchema#string"): "string",
    rdflib.URIRef("http://www.w3.org/2001/XMLSchema#integer"): "integer",
    rdflib.URIRef("http://www.w3.org/2001/XMLSchema#double"): "number",
    rdflib.URIRef("http://www.w3.org/2001/XMLSchema#boolean"): "boolean",
    rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#Datatype"): "object",
    rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#Literal") : "string"
}

q0 = prepareQuery("""
SELECT ?subject
WHERE {
    ?subject rdf:type owl:Class
}""",
                  initNs={
                      "owl": rdflib.OWL,
                      "rdf": rdflib.RDF
                  })

q1 = prepareQuery("""
select distinct ?property ?value ?type where {
        {
            ?a ?property ?value .
            bind(?property as ?type) .
            filter(?property != rdfs:subClassOf)
        }
        union
        {
            ?property rdf:type ?prop_type.
            ?property rdfs:domain ?a .
            ?property rdfs:range ?value .
            bind(?prop_type as ?type) .
        }
}""",
                  initNs={
                      "rdf": rdflib.RDF,
                      "rdfs": rdflib.RDFS
                  })




def get_prop_name(prop_iri, skip_ontology_name=False):
    if not skip_ontology_name:
        return str(prop_iri)
    elif '#' in str(prop_iri):
        return str(prop_iri).split('#')[1]
    else:
        return str(prop_iri).split('/')[-1]

def make_schema(_cls, g, q1, visited, skip_ontology_name=False):
    schema = {
        "$id": str(_cls),
        "type": "object",
        "properties": {}
    }

    if str(_cls) in visited:
        return schema
    else:
        visited.append(str(_cls))

    props = g.query(q1, initBindings={'a': _cls})

    for prop in props:
        prop_iri, prop_val, prop_type = prop
        if prop_type == NON_REC_PROPERTY:
            try:
                _type = TYPE_MAPPING[prop_val]
                schema["properties"][get_prop_name(prop_iri, skip_ontology_name=skip_ontology_name)] = {
                    "$id": str(prop_iri),
                    "type": _type
                }
            except:
                print(f"Invalid property type: {prop_val}")
        elif prop_type == REC_PROPERTY:
            schema["properties"][get_prop_name(prop_iri, skip_ontology_name=skip_ontology_name)] = make_schema(
                prop_val, g, q1, visited)
    visited.pop()
    return schema


def parse_graph(g, skip_ontology_name=False):
    classes = g.query(q0)
    classes = [c[0] for c in classes]

    schemas = {}

    for _cls in classes:
        schemas[get_prop_name(_cls, skip_ontology_name=skip_ontology_name)] = make_schema(
            _cls, g, q1, [], skip_ontology_name=skip_ontology_name)

    return schemas # json.dumps(, indent='\t')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url',
                        type=str,
                        required=True,
                        help="Address of ontology to parse (i.e http://localhost:3030/test or ~/Downloads/test.ttl)")
    parser.add_argument('-f', '--format', type=str, default='turtle',
                        help="RDFlib-supported ontology format")
    parser.add_argument('-s', '--skip-ontology-name', action='store_true',
                        default=False, help="Do we need to skip the ontology URI in parameter names?")

    args = parser.parse_args()

    g = rdflib.Graph()
    g.parse(args.url, format=args.format)

    print(json.dumps(parse_graph(g, args.skip_ontology_name), indent='\t'))
    
