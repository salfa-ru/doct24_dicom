from core.json import load_from_json


def model_fill(json_path, model, file: str):
    objects = load_from_json(json_path, file)
    for _object in objects:
        new = model(**_object)
        new.save()
