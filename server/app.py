import pathlib
from flask import request, jsonify
from api import app
from ariadne import load_schema_from_path, make_executable_schema,graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from api.queries import listUnidades_resolver,getUnidad_resolver,getUnidadByAlc_resolver

query = ObjectType("Query")
query.set_field("listUnidades", listUnidades_resolver)
query.set_field("getMetroBus", getUnidad_resolver)
query.set_field("getMetroBusByAlc", getUnidadByAlc_resolver)

type_defs = load_schema_from_path(f'{pathlib.Path(__file__).parent.absolute()}/schema.graphql')
schema = make_executable_schema(
    type_defs,query, snake_case_fallback_resolvers
)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == '__main__':
   app.run(host='127.0.0.1',port=8000,debug=True)