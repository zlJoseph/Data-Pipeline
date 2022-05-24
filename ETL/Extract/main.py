import yaml
import pathlib
import requests
import csv

def structure():
    """ Estructura del JSON recuperado de la API """
    with open(f'{pathlib.Path(__file__).parent.absolute()}/../campos.yaml', mode='r', encoding="utf8") as f:
        return yaml.Loader(f).get_data()

def get_data(url):
    """
        Recupera los datos de la API
        @param url: URL de la API
    """
    return requests.get(url).json()

def delete_list_position(listData,position):
    """
        Elimina una posición de una lista
        @param listData: Lista
        @param position: Posición a eliminar
    """
    return listData[:position] + listData[position+1:]

def read_maps_node_data_children(data,position,count,structureKeys,response={}):
    """
        Recuperar los datos del nodo hijo del JSON recuperado de la API
        @param data: Datos del nodo hijo
        @param position: Posición del nodo hijo
        @param count: Cantidad de nodos hijos
        @param structureKeys: Estructura de las llaves del JSON recuperado de la API
        @param response: Datos que se guardarán en un archivo CSV
    """
    response[structureKeys[position]]=data[structureKeys[position]]
    if (position+1) == count:
        return response
    else:
        return read_maps_node_data_children(data,position+1,count,structureKeys,response)

def read_maps_node_children(data,position,count,structureKeys,response=[]):
    """
        Lee los nodos hijos del JSON recuperado de la API, datos que se guardarán en un archivo CSV
        @param data: Datos recuperados de la API
        @param position: Posición del nodo hijo
        @param count: Cantidad de nodos hijos
        @param structureKeys: Estructura de las llaves del JSON recuperado de la API
        @param response: Datos que se guardarán en un archivo CSV
    """
    response.append(read_maps_node_data_children(data[position],0,len(delete_list_position(structureKeys,structureKeys.index("type"))),delete_list_position(structureKeys,structureKeys.index("type")),{}))
    if (position+1) == count:
        return response
    else:
        return read_maps_node_children(data,position+1,count,structureKeys,response)

def read_node(data,position,count,structureKeys,structureJSON):
    """
        Lee los nodos del JSON recuperado de la API
        @param data: Datos recuperados de la API
        @param position: Posición del nodo
        @param count: Cantidad de nodos
        @param structureKeys: Estructura de las llaves del JSON recuperado de la API
        @param structureJSON: Estructura del JSON recuperado de la API
    """
    if (position+1) == count:
        if structureJSON[structureKeys[position]]['type'] == "JSON":
            read_node(data[structureKeys[position]],0,
                len(delete_list_position(list(structureJSON[structureKeys[position]].keys()),list(structureJSON[structureKeys[position]].keys()).index("type"))),
                delete_list_position(list(structureJSON[structureKeys[position]].keys()),list(structureJSON[structureKeys[position]].keys()).index("type")),
                structureJSON[structureKeys[position]])
        elif structureJSON[structureKeys[position]]['type'] == "MAPS":
            save_data(structureKeys[position],list(structureJSON[structureKeys[position]].keys()),read_maps_node_children(data[structureKeys[position]],0,len(data[structureKeys[position]]),list(structureJSON[structureKeys[position]].keys()),[]))

def csv_writter(writer,data,position,count):
    """
        Escribe los datos en un archivo CSV
        @param writer: Objeto que escribe los datos en un archivo CSV
        @param data: Datos que se guardarán en un archivo CSV
        @param position: Posición del dato
        @param count: Cantidad de datos
    """
    if position==0:
        writer.writeheader()
    if (position+1) <= count:
        writer.writerow(data[position])
        csv_writter(writer,data,position+1,count)

def save_data(sheet,header,data):
    """
        Guarda los datos en un archivo CSV
        @param sheet: Hoja de Excel
        @param header: Cabecera del archivo CSV
        @param data: Datos que se guardarán en un archivo CSV
    """
    with open(f'{pathlib.Path(__file__).parent.absolute()}/../{sheet}.csv', mode='w',newline='', encoding="utf8") as csvfile:
        csv_writter(csv.DictWriter(csvfile,fieldnames=delete_list_position(header,header.index("type"))),data,0,len(data))

def process_data(data,structureKeys,structureJSON):
    """
        Procesa los datos recuperados de la API
        @param data: Datos recuperados de la API
        @param structureKeys: Estructura de las llaves del JSON recuperado de la API
        @param structureJSON: Estructura del JSON recuperado de la API
    """
    read_node(data,0,len(structureKeys),structureKeys,structureJSON)

def search_data(url,arg,structureJSON):
    """
        Busca los datos en la API
        @param url: URL de la API
        @param arg: Argumentos de la API
        @param structureJSON: Estructura del JSON recuperado de la API
    """
    process_data(get_data(f'{url}&offset={arg[0]}&limit={arg[1]}'),list(structureJSON.keys()),structureJSON)

if __name__ == '__main__':
    """Iniciar el proceso de extraccion"""
    search_data(structure()['site']['url'],['0',structure()['site']['limit']],structure()['site']['struct'])

