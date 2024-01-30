from databases import Database

from fastapi import FastAPI

app = FastAPI()

app = FastAPI()
database = Database("mysql://root:123456@localhost:3306/huaqibei")


# 连接和断开数据库
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def advanced_convert_to_tuple(input_string):
    input_string = input_string.strip("[]")

    def parse_element(element):
        try:
            return int(element)
        except ValueError:
            pass

        try:
            return float(element)
        except ValueError:
            pass

        if element.startswith('"') and element.endswith('"'):
            return element[1:-1]
        if (element.startswith('[') and element.endswith(']')) or \
                (element.startswith('(') and element.endswith(')')):
            return parse_sequence(element[1:-1])

        return element

    def parse_sequence(seq):
        elements = []
        nested = 0
        current = ''
        for char in seq:
            if char in '([':
                nested += 1
                current += char
            elif char in ')]':
                nested -= 1
                current += char
            elif char == ',' and nested == 0:
                elements.append(parse_element(current.strip()))
                current = ''
            else:
                current += char
        if current:
            elements.append(parse_element(current.strip()))
        return tuple(elements) if '(' in seq else elements

    return parse_sequence(input_string)


@app.get("/entity/{entity_id}")
async def get_entity(entity_id: int):
    query = "SELECT * FROM `data` WHERE id = :id"
    result = await database.fetch_one(query, values={"id": entity_id})
    if result:
        return {"id": result[0], "name": result[2], "type": result[2], "status_code": 0, "status_msg": "ok"}
    return {"status_code": 400, "status_msg": "No found record"}


def get_edges_and_points(string):
    if string is None:
        return [], []
    shareholders_info = advanced_convert_to_tuple(string)
    points = []
    edges = []
    for shareholder in shareholders_info:
        point = {"id": shareholder[0], "name": shareholder[1], "type": shareholder[2]}
        if point not in points:
            points.append(point)
        for idx, edge in enumerate(shareholder[5]):
            if idx == 0:
                edge_tmp = {"source": edge[0], "target": shareholder[0], "share": edge[1]}
                if edge_tmp not in edges:
                    edges.append(edge_tmp)
                continue
            edge_tmp = {"source": edge[0], "target": shareholder[5][idx - 1][0], "share": edge[1]}
            if edge_tmp not in edges:
                edges.append(edge_tmp)
    return edges, points


@app.get("/shareholders/{entity_id}")
async def get_shareholders(entity_id: int):
    query = "SELECT * FROM `data` WHERE id = :id"
    result = await database.fetch_one(query, values={"id": entity_id})
    if result:
        up_points, up_edges = get_edges_and_points(result[3])
        down_points, down_edges = get_edges_and_points(result[4])
        return {"status_code": 0, "status_msg": "ok",
                "up_result": {"points": up_points, "edges": up_edges},
                "down_result": {"points": down_points, "edges": down_edges}
                }
    return {"status_code": 400, "status_msg": "No found record"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
