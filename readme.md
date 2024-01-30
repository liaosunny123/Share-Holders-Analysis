# Demo For Getting Share Holder Relation

# API

## Get for entity information

- Address: {{host}}/entity/{{entity_id}}

- Method: GET
- Response

```json
{
    "id": 1,
    "name": "E01",
    "type": "E01",
    "status_code": 0,
    "status_msg": "ok"
}
```

```json
{
    "status_code": 400,
    "status_msg": "Bad request"
}
```

## Get for share holders relations

- Address: {{host}}/entity/{{entity_id}}
- Method: GET
- Response

```json
{
    "status_code": 0,
    "status_msg": "ok",
    "up_result": {
        "points": [
            {
                "source": 0,
                "target": 0,
                "share": 0.0
            }
        ],
        "edges": [
            {
                "id": 0,
                "name": "null",
                "type": "null"
            }
        ]
    },
    "down_result": {
        "points": [
            {
                "source": 0,
                "target": 0,
                "share": 0.0
            }
        ],
        "edges": [
            {
                "id": 0,
                "name": "null",
                "type": "null"
            }
        ]
    }
}
```

```json
{
    "status_code": 400,
    "status_msg": "Bad request",
}
```

