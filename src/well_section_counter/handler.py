from well_section_counter.main_counter import main


# обработчик получаемого с фронта в бек
def handler_front(data):
    result_data = {}
    # заполнение данных скважины
    casing_data = data.get("casingString", [])
    columns = {}
    if casing_data:
        for i, casing in enumerate(casing_data):
            columns[i + 1] = {
                "id": i + 1,
                "D": int(casing["diameter"]),
                "from": float(casing["depth"]["from"]),
                "till": float(casing["depth"]["to"]),
                "type": "обсадная",
            }
    # добавление фильтровой колонны
    if data.get("filterColumn"):
        i = len(casing_data)
        columns[i + 1] = {
            "id": i + 1,
            "D": int(data["filterColumn"]["diameter"]),
            "from": float(data["filterColumn"]["depth"]["from"]),
            "till": float(data["filterColumn"]["depth"]["to"]),
        }
        if data["filterColumn"]["type"] == "Фильтровая колонна":
            columns[i + 1]["type"] = "фильтровая"
            if data["filterColumn"]["intervals"]:
                columns[i + 1]["filter"] = {}
                for j in range(len(data["filterColumn"]["intervals"])):
                    interval = {
                        "id": j + 1,
                        "from": float(data["filterColumn"]["intervals"][j]["from"]),
                        "till": float(data["filterColumn"]["intervals"][j]["to"]),
                    }
                    columns[i + 1]["filter"][j + 1] = interval
        else:
            columns[i + 1]["type"] = "О.С."
    # добавление оснастки
    result_data["well_data"] = {
        "columns": columns,
        "pump_type": data["rigging"]["pumpName"],
        "pump_depth": float(data["rigging"]["pumpDepth"]),
        "static_lvl": float(data["rigging"]["staticLvl"]),
        "dynamic_lvl": float(data["rigging"]["dynamicLvl"]),
        "well_depth": float(data["well"]["depth"]),
    }
    # заполнение геологических слоев
    horizons_data = data.get("horizons", [])
    layers = {}
    if horizons_data:
        for i, horizon in enumerate(horizons_data):
            layers[i + 1] = {
                "id": i + 1,
                "name": horizon["name"],
                "thick": float(horizon["depth"]["to"])
                - float(horizon["depth"]["from"]),
                "sediments": tuple(horizon["depositType"]),
                "interlayers": tuple(horizon["interlayers"]),
                "inclusions": tuple(horizon["inclusions"]),
            }
        result_data["layers"] = layers
        if data["well"]["project_name"]:
            result_data["project_name"] = data["well"]["project_name"]
        return result_data
