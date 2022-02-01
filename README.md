# Convert classes from OWL model to JSON schema (in a very specific case yet)

## Install
```shell
pip3 install rdflib
```

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

