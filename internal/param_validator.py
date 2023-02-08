def validate (param: dict, param_name: str, type: type, positive = True):
    if type == str:
        return param_name in param and isinstance(param[param_name], type)
    if type == int and positive == True:
        return param_name in param and isinstance(param[param_name], type) and param[param_name] >= 0 and param[param_name] <= 10000
    return param_name in param and isinstance(param[param_name], type)