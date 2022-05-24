from ntpath import join
import yaml
import pathlib
import pandas as pd
import mysql.connector

def structure():
    with open(f'{pathlib.Path(__file__).parent.absolute()}/loadCampos.yaml', mode='r', encoding="utf8") as f:
        return yaml.Loader(f).get_data()

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
            readData=lambda sheet,keys,struct: read_data(pd.read_csv(f'{pathlib.Path(__file__).parent.absolute()}/../{sheet}Transform.csv',usecols=keys, encoding="utf8"),sheet,keys,struct)
            readData(structureKeys[position],delete_list_position(list(structureJSON[structureKeys[position]].keys()),list(structureJSON[structureKeys[position]].keys()).index("type")),structureJSON[structureKeys[position]])

def validate_field(value,typeV):
    #print(typeV)
    #print(value)
    #print(type(value))
    return value

def read_fields(position,y,count,file,structureKeys,structureJSON,response={}):
    response[structureKeys[position]]=validate_field(file[structureKeys[position]][y],structureJSON[structureKeys[position]])
    if (position+1) == count:
        return response
    else:
        return read_fields(position+1,y,count,file,structureKeys,structureJSON,response)

def read_data_row(position,count,file,structureKeys,structureJSON,response=[]):
    response.append(read_fields(0,position,len(structureKeys),file,structureKeys,structureJSON,{}))
    if (position+1)==count:
        return response
    else:
        return read_data_row(position+1,count,file,structureKeys,structureJSON,response)

def type_bd(typeString):
    if typeString == "text":
        return "VARCHAR(255)"
    if typeString == "int":
        return "INT"
    if typeString == "double":
        return "DOUBLE(17,14)"
    if typeString == "numeric":
        return "INT"#"FLOAT(4,2)"
    if typeString == "timestamp":
        return "TIMESTAMP"
    return "VARCHAR(255)"

def create_string_table(position,count,structureKeys,structureJSON,response=""):
    if (position+1) == count:
        if structureKeys[position]=="id":
            response=response+","+structureKeys[position]+" "+type_bd(structureJSON[structureKeys[position]])+" NOT NULL AUTO_INCREMENT"
        else:
            response=response+","+structureKeys[position]+" "+type_bd(structureJSON[structureKeys[position]])
        response=response+", PRIMARY KEY (`id`)) ENGINE = InnoDB;"
        return response
    elif position== 0:
        if structureKeys[position]=="id":
            response="("+structureKeys[position]+" "+type_bd(structureJSON[structureKeys[position]])+" NOT NULL AUTO_INCREMENT"
        else:
            response="("+structureKeys[position]+" "+type_bd(structureJSON[structureKeys[position]])
    else:
        if structureKeys[position]=="id":
            response=response+","+structureKeys[position]+" "+type_bd(structureJSON[structureKeys[position]])+" NOT NULL AUTO_INCREMENT"
        else:
            response=response+","+structureKeys[position]+" "+type_bd(structureJSON[structureKeys[position]])
    return create_string_table(position+1,count,structureKeys,structureJSON,response)

def mysql_create_database(mysql):
    mysql.cursor().execute("CREATE DATABASE IF NOT EXISTS prueba")

def mysql_table_database(mysql,nameTable,structureKeys,structureJSON):
    mysql.cursor().execute("DROP TABLE IF EXISTS "+nameTable)
    mysql.cursor().execute("CREATE TABLE IF NOT EXISTS "+nameTable+create_string_table(0,len(structureKeys),structureKeys,structureJSON,""))
    return mysql

def connect_mysql(create=True):
    if(create):
        mysql_create_database(connect_mysql(False))
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="prueba"
        )
    else:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )

def insert_row(sheet,position,count,data,structureKeys,response=""):
    #print(structureKeys)
    if position == 0:
        response=f"INSERT INTO {sheet} ({','.join(structureKeys)}) VALUES ('{data[structureKeys[position]]}'"
    elif (position+1) == count:
        return f"{response},'{data[structureKeys[position]]}')"
    else:
        response=f"{response},'{data[structureKeys[position]]}'"

    return insert_row(sheet,position+1,count,data,structureKeys,response)

def insert_data(sheet,position,count,data,structureKeys,mysql):
    mysql.cursor().execute(insert_row(sheet,0,len(structureKeys),data[position],structureKeys,""))
    mysql.commit()
    if (position+1) < count:
        insert_data(sheet,position+1,count,data,structureKeys,mysql)

def read_data(file,sheet,structureKeys,structureJSON):
    v=read_data_row(0,len(file),file,structureKeys,structureJSON)
    insert_data(sheet,0,len(v),v,delete_list_position(structureKeys,structureKeys.index("id")),mysql_table_database(connect_mysql(),sheet,structureKeys,structureJSON))

def main(structureJSON):
    read_node(0,len(list(structureJSON.keys())),list(structureJSON.keys()),structureJSON)

if __name__ == '__main__':
    main(structure()['site']['struct'])