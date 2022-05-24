# Data pipeline

Necesario inicializar MySql con Xampp

##Diagrama
[Diagrama](https://drive.google.com/file/d/1Phv39urILgDo_CGEHA3CRMPIrOIzBMmg/view)

## Carpeta ETL
Ejecutar el script pipeline.py para realizar la extracción, transformación y carga de los metrobuses. El proceso de carga creará la base de datos si fuera necesario.

En el proceso de transformación se calcula la distancia entre las coordenadas de metrobuses y las alcaldías con la fórmula de Haversine, esto para encontrar el mínimo y definir a que alcaldía pertenece.

```bash
python3 pipeline.py
```

## Carpeta Server
Api con GraphQl, para inicializar en local ejecutar:
```bash
python3 app.py
```
Ingresar a http://localhost:8000/graphql para realizar las consultas:

Para recuperar las unidades 
```
query{
  listUnidades{
    success
    errors
    metrobuses{
      id
      date_updated
      vehicle_id
      vehicle_label
      vehicle_current_status
      position_latitude
      position_longitude
      geographic_point
      position_speed
      position_odometer
      trip_schedule_relationship
      trip_id
      trip_start_date
      trip_route_id
      alc
    }
  }
}
```
Para recuperar la unidad por ID
```
query{
  getMetroBus(id: 1){
    success
    metrobus{
      id
      position_latitude
      position_longitude
    }
  }
}
```

Para recuperar unidades por alcaldías
```
query{
  getMetroBusByAlc(alc: "Tlalpan"){
    success
    errors
    metrobuses{
      id
      date_updated
      vehicle_id
      vehicle_label
      position_latitude
      position_longitude
      geographic_point
      alc
    }
  }
}

```
