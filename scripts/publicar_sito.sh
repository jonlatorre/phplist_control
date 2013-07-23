#!/bin/bash
#url="http://localhost:8000/api/v1/sitio/"
url="http://phplist.kernet.es/api/v1/sitio/"
curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"nombre": "test desde shell", "dominio": "farsa.kernet.es"}' $url
