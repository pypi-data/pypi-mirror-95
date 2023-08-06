

def prepare_params(params: dict) -> dict:
    """
    Метод для фильтрации параметров

    Args:
        params (dict): 'сырые' параметры, не мутируются

    Returns:
        dict: отфильтрованные и приведённые к нужному формату параметры,
        мутированная копия входных
    """
    params = params.copy()  # NOTE: возможно создание копии не нужно?
    if "kwargs" in params:
        params.update(params.pop("kwargs"))
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, (tuple, list)):
            # NOTE: возможно вместо repr нужен str, я пока не уверен
            # объединение списков "[1, 2, 3]" к виду "1,2,3"
            params[k] = ",".join(repr(i) for i in v)
        elif isinstance(v, bool):
            params[k] = int(v)

    return {
        k if not k.endswith("_") else k[:-1]: v
        for k, v in params.items()
        if k != "self" and v is not None
    }
