# обработчик получаемого с фронат в бек
data = {
    "filterColumn": {
        "type": "Фильтровая колонна",
        "diameter": "3",
        "depth": {"from": "3", "to": "3"},
        "intervals": [{"from": "4", "to": "4"}, {"from": "5", "to": "5"}],
    },
    "horizons": [
        {
            "depositType": ["пески"],
            "interlayers": ["пески средние"],
            "inclusions": ["глыбы"],
            "name": "6",
            "depth": {"from": "6", "to": "6"},
        },
        {
            "depositType": ["пески средние"],
            "interlayers": ["пески мелкие"],
            "inclusions": ["галька"],
            "name": "7",
            "depth": {"from": "7", "to": "7"},
        },
    ],
    "well": {"project_name": "Название", "depth": "Глубина"},
    "casingString": [
        {"diameter": "1", "depth": {"from": "1", "to": "1"}},
        {"diameter": "2", "depth": {"from": "2", "to": "2"}},
    ],
}


def handler_front(data):
    result_data = {}
    columns = {}
    casing_data = data.get("casingString", [])
    for i, casing in enumerate(casing_data):
        columns[i + 1] = {
            "id": i + 1,
            "D": int(casing["diameter"]),
            "from": float(casing["depth"]["from"]),
            "till": float(casing["depth"]["to"]),
            "type": "обсадная",
        }
    if data.get("filterColumn"):
        i = len(casing_data)
        columns[i + 1] = {
            "id": i + 1,
            "D": int(data["filterColumn"]["diameter"]),
            "from": float(data["filterColumn"]["depth"]["from"]),
            "till": float(data["filterColumn"]["depth"]["to"]),
        }
        # определяем тип фильтровой колонны
        if data["filterColumn"]["type"] == "Фильтровая колонна":
            columns[i + 1]["type"] = "фильтровая"
            if data["filterColumn"]["intervals"]:
                columns[i + 1]["filter"] = {}
                for j in range(len(data["filterColumn"]["intervals"])):
                    interval = {
                        "id": j + 1,
                        "from": data["filterColumn"]["intervals"][j]["from"],
                        "till": data["filterColumn"]["intervals"][j]["to"],
                    }
                    columns[i + 1]["filter"][j + 1] = interval
        else:
            columns[i + 1]["type"] = "О.С."
    result_data["well_data"] = {}
    result_data["well_data"]["columns"] = columns
    # result_data["well_data"]["pump_type"] = columns
    print(result_data)


handler_front(data)
