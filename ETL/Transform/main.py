import yaml
import pathlib
import pandas as pd
import json
import math
import csv
from datetime import datetime

def structure():
    with open(f'{pathlib.Path(__file__).parent.absolute()}/../campos.yaml', mode='r', encoding="utf8") as f:
        return yaml.Loader(f).get_data()

def jsonData():
    with open(f'{pathlib.Path(__file__).parent.absolute()}/data.json', mode='r', encoding="utf8") as f:
        return json.load(f)

def delete_list_position(listData,position):
    return listData[:position] + listData[position+1:]

def read_node(position,count,structureKeys,structureJSON):
    if (position+1) == count:
        if structureJSON[structureKeys[position]]['type'] == "JSON":
            read_node(0,
                len(delete_list_position(list(structureJSON[structureKeys[position]].keys()),list(structureJSON[structureKeys[position]].keys()).index("type"))),
                delete_list_position(list(structureJSON[structureKeys[position]].keys()),list(structureJSON[structureKeys[position]].keys()).index("type")),
                structureJSON[structureKeys[position]])
        elif structureJSON[structureKeys[position]]['type'] == "MAPS":
            readData=lambda sheet,keys,struct: read_data(pd.read_csv(f'{pathlib.Path(__file__).parent.absolute()}/../{sheet}.csv',usecols=keys, encoding="utf8"),sheet,keys,struct,jsonData())
            readData(structureKeys[position],delete_list_position(list(structureJSON[structureKeys[position]].keys()),list(structureJSON[structureKeys[position]].keys()).index("type")),structureJSON[structureKeys[position]])

def validate_field(value,typeV):
    #print(typeV)
    #print(value)
    #print(type(value))
    if typeV=="timestamp":
        return datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M:%S")
    return value

#radio promedio 6,371.0km
def set_alcaldia(position,count,latitud,longitud,jsonAlcaldia,response=[]):
    distance=lambda lat1, lon1, lat2, lon2: 12742*math.asin(math.sqrt(math.pow(math.sin((lat2-lat1)*math.pi/180/2),2)+math.cos(lat1*math.pi/180)*math.cos(lat2*math.pi/180)*math.pow(math.sin((lon2-lon1)*math.pi/180/2),2)))
    response.append({'alc':jsonAlcaldia['keys'][position],'distance':distance(latitud,longitud,jsonAlcaldia[jsonAlcaldia['keys'][position]]['latitud'],jsonAlcaldia[jsonAlcaldia['keys'][position]]['longitud'])})
    if (position+1)==count:
        return response
    else:
        return set_alcaldia(position+1,count,latitud,longitud,jsonAlcaldia,response)

def set_min_distance_alcaldia(data):
    return [x for x in data if x['distance']==min([x['distance'] for x in data])][0]['alc']

def read_fields(position,y,count,file,jsonAlcaldia,structureKeys,structureJSON,response={}):
    response[structureKeys[position]]=validate_field(file[structureKeys[position]][y],structureJSON[structureKeys[position]])
    if (position+1) == count:
        response['alc']=set_min_distance_alcaldia(set_alcaldia(0,len(jsonAlcaldia['keys']),response['position_latitude'],response['position_longitude'],jsonAlcaldia,[]))
        return response
    else:
        return read_fields(position+1,y,count,file,jsonAlcaldia,structureKeys,structureJSON,response)

def read_data_row(position,count,file,jsonAlcaldia,structureKeys,structureJSON,response=[]):
    response.append(read_fields(0,position,len(structureKeys),file,jsonAlcaldia,structureKeys,structureJSON,{}))
    if (position+1)==count:
        return response
    else:
        return read_data_row(position+1,count,file,jsonAlcaldia,structureKeys,structureJSON,response)


def csv_writter(writer,data,position,count):
    if position==0:
        writer.writeheader()
    if (position+1) <= count:
        writer.writerow(data[position])
        csv_writter(writer,data,position+1,count)

def save_data(sheet,header,data):
    header.append('alc')
    with open(f'{pathlib.Path(__file__).parent.absolute()}/../{sheet}.csv', mode='w',newline='', encoding="utf8") as csvfile:
        csv_writter(csv.DictWriter(csvfile,fieldnames=header),data,0,len(data))

def read_data(file,sheet,structureKeys,structureJSON,jsonAlcaldia):
    save_data(f'{sheet}Transform',[x for x in structureKeys],read_data_row(0,len(file),file,jsonAlcaldia,structureKeys,structureJSON))

def main(structureJSON):
    read_node(0,len(list(structureJSON.keys())),list(structureJSON.keys()),structureJSON)

if __name__ == '__main__':
    main(structure()['site']['struct'])