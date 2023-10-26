from well_section_counter.main_counter import main


# обработчик получаемого с фронта в бек
def handler_front(data):
    result_data = {}
    # заполнение данных скважины
    columns = {}
    well = data.get("well", {})
    construction = well.get("construction", [])
    i = 1
    if construction.get("columns", []):
        columns_data = construction.get("columns", [])
        for elem in columns_data:
            columns[i] = {
                "id": i,
                "D": int(elem["d"]),
                "from": float(elem["from"]),
                "till": float(elem["to"]),
                "type": "обсадная",
            }
            i += 1
    # добавление фильтровой колонны
    if construction.get("filter_columns", []):
        filter_columns = construction.get("filter_columns", [])
        for elem in filter_columns:
            columns[i] = {
                "id": i,
                "D": int(elem["d"]),
                "from": float(elem["from"]),
                "till": float(elem["to"]),
            }
            # выбор типа фильтровой колонны
            # нумерация колонн сквозная
            if elem["type"] == "Фильтровая колонна":
                columns[i]["type"] = "фильтровая"
                if elem["filters"]:
                    columns[i]["filter"] = {}
                    for j in range(len(elem["filters"])):
                        interval = {
                            "id": j + 1,
                            "from": float(elem["filters"][j]["from"]),
                            "till": float(elem["filters"][j]["to"]),
                        }
                        columns[i]["filter"][j + 1] = interval
            else:
                columns[i]["type"] = "О.С."
            i += 1
    # добавление оснастки
    result_data["well_data"] = {
        "columns": columns,
        "pump_type": str(data["well"]["data"]["pump_type"]) if data["well"]["data"]["pump_type"] else None,
        "pump_depth": float(data["well"]["data"]["pump_depth"]) if data["well"]["data"]["pump_depth"] else None,
        "static_lvl": float(data["well"]["data"]["static_lvl"]) if data["well"]["data"]["static_lvl"] else None,
        "dynamic_lvl": float(data["well"]["data"]["dynamic_lvl"]) if data["well"]["data"]["dynamic_lvl"] else None,
        "well_depth": float(data["well"]["depth"]) if data["well"]["depth"] else None,
    }
    # заполнение геологических слоев
    layers = {}
    i = 1
    if well.get("layers", []):
        layers_data = well.get("layers", [])
        for elem in layers_data["layer"]:
            layers[i] = {
                "id": i,
                "name": elem["name"],
                "thick": float(elem["to"])
                - float(elem["from"]),
                "sediments": tuple(elem["sediments"]),
                "interlayers": tuple(elem["interlayers"]),
                "inclusions": tuple(elem["inclusions"]),
            }
            i += 1
    result_data["layers"] = layers
    # добавление названия проекта
    if data["well"]["name"]:
        result_data["project_name"] = data["well"]["name"]
    return result_data
