import json
from internal.logger import logger

with open("/usr/src/app/config.json") as f:
    CONF = json.load(f)
PARAM_TYPES = CONF['PARAM_TYPES']

#params - словарь со всеми параметрами в запросе
#requirement - список строк с обязательными параметрами
def validate (params: dict, requirement: list = None) -> bool :
    if requirement:
        for param in requirement:
            if not param in params: 
                logger.error(f'No required param {param}')
                return False

    for key, value in params.items():
        if not key in PARAM_TYPES: 
            logger.error(f'No key "{key}" in PARAM_TYPES')
            return False
        
        if PARAM_TYPES[key]['type'] == 'str':
            if len(value) >= PARAM_TYPES[key]['min'] and len(value) <= PARAM_TYPES[key]['max'] and isinstance(key, str):
                continue
        elif PARAM_TYPES[key]['type'] == 'int':
            if value >= PARAM_TYPES[key]['min'] and value <= PARAM_TYPES[key]['max'] and isinstance(key, str):
                continue
        logger.error(f'No type for "{key}" in PARAM_TYPES or "{value}" out of bounds')
        return False
    return True
                

print (validate({"login": "adv", "add_pills": 1230}))
print (validate({"login": "adv"}))