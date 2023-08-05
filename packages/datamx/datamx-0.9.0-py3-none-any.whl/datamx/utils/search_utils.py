from datamx.models.values import Groups


def find_first(groups: Groups, model_name: str, value_id: str):
    for group in groups.groups:
        value = next((v for v in group.values if v.id == value_id), None)
        if value is not None:
            break
    return value.value if value is not None else None
