from .models import MetroBus
from ariadne import convert_kwargs_to_snake_case

def listUnidades_resolver(obj, info):
    try:
        metrobuses = [metrobus.to_dict() for metrobus in MetroBus.query.all()]
        return {
            "success": True,
            "metrobuses": metrobuses
        }
    except Exception as error:
        return {
            "success": False,
            "errors": [str(error)]
        }

@convert_kwargs_to_snake_case
def getUnidad_resolver(obj, info, id):
    try:
        metrobus = MetroBus.query.get(id)
        payload = {
            "success": True,
            "metrobus": metrobus.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["Post item matching {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def getUnidadByAlc_resolver(obj, info, alc):
    try:
        metrobuses = [metrobus.to_dict() for metrobus in MetroBus.query.filter(MetroBus.alc == alc).all()]
        return {
            "success": True,
            "metrobuses": metrobuses
        }
    except AttributeError:  # todo not found
        return {
            "success": False,
            "errors": ["Post item matching {id} not found"]
        }