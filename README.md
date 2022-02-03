# Convert classes from OWL model to JSON schema (in a very specific case yet)

## Install
```shell
pip3 install rdflib
```

## Docker and flask service

### Build

```shell
docker build -t owl2jsonschema:latest .
```

### Run

```shell
docker run -p 5000:80 -e UPDATE_INTERVAL=60 -e OWL_DB=http://xmlns.com/foaf/spec/index.rdf -e OWL_DB_TYPE=xml owl2jsonschema:latest
```

### Usage

 - `GET /<class name>` - returns json schema by class name without ontology name
 - `POST /full` body: `iri=<full IRI>` - returns json schema by IRI

### Environment variables

 - `OWL_DB` -- ontology address
 - `OWL_DB_TYPE` -- ontology type (`xml`, `turtle`, etc)
 - `UPDATE_INTERVAL` -- ontology fetch interval in seconds

## Usage examples
 - Local turtle file:
 ```shell
python3 owl2jsonschema.py -s -u test.ttl
```
 - FOAF ontology:
```shell
python3 owl2jsonschema.py -s -f xml -u http://xmlns.com/foaf/spec/index.rdf 
```
outputs:
```json
{
	"Class": {
		"$id": "http://www.w3.org/2000/01/rdf-schema#Class",
		"type": "object",
		"properties": {}
	},
	"LabelProperty": {
		"$id": "http://xmlns.com/foaf/0.1/LabelProperty",
		"type": "object",
		"properties": {}
	},
    ...
    "Image": {
		"$id": "http://xmlns.com/foaf/0.1/Image",
		"type": "object",
		"properties": {
			"depicts": {
				"$id": "http://www.w3.org/2002/07/owl#Thing",
				"type": "object",
				"properties": {
					"name": {
						"$id": "http://xmlns.com/foaf/0.1/name",
						"type": "string"
					},
					...
					"maker": {
						"$id": "http://xmlns.com/foaf/0.1/Agent",
						"type": "object",
						"properties": {
							"mbox": {
								"$id": "http://www.w3.org/2002/07/owl#Thing",
								"type": "object",
								"properties": {}
							},
							...
							"account": {
								"$id": "http://xmlns.com/foaf/0.1/OnlineAccount",
								"type": "object",
								"properties": {
									"accountServiceHomepage": {
										"$id": "http://xmlns.com/foaf/0.1/Document",
										"type": "object",
										"properties": {
											"topic": {
												"$id": "http://www.w3.org/2002/07/owl#Thing",
												"type": "object",
												"properties": {}
											},
											"primaryTopic": {
												"$id": "http://www.w3.org/2002/07/owl#Thing",
												"type": "object",
												"properties": {}
											}
										}
									},
									"accountName": {
										"$id": "http://xmlns.com/foaf/0.1/accountName",
										"type": "string"
									}
								}
							},
							...
						}
					},
					"depiction": {
						"$id": "http://xmlns.com/foaf/0.1/Image",
						"type": "object",
						"properties": {}
					},
					...
				}
			},
			"thumbnail": {
				"$id": "http://xmlns.com/foaf/0.1/Image",
				"type": "object",
				"properties": {}
			}
		}
	},
    ...
}
```

