from api import db

class MetroBus(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    date_updated = db.Column(db.DateTime)
    vehicle_id = db.Column(db.Integer)
    vehicle_label = db.Column(db.Integer)
    vehicle_current_status= db.Column(db.Integer)
    position_latitude= db.Column(db.Float)
    position_longitude= db.Column(db.Float)
    geographic_point = db.Column(db.String(255))
    position_speed= db.Column(db.Integer)
    position_odometer= db.Column(db.Integer)
    trip_schedule_relationship= db.Column(db.Integer)
    trip_id= db.Column(db.Integer)
    trip_start_date= db.Column(db.Integer)
    trip_route_id= db.Column(db.Integer)
    alc= db.Column(db.String(255))
    def to_dict(self):
        return {
            "id": self.id,
            "date_updated": str(self.date_updated.strftime("%Y-%m-%d %H:%M:%S")),
            "vehicle_id": self.vehicle_id,
            "vehicle_label": self.vehicle_label,
            "vehicle_current_status": self.vehicle_current_status,
            "position_latitude": self.position_latitude,
            "position_longitude": self.position_longitude,
            "geographic_point": self.geographic_point,
            "position_speed": self.position_speed,
            "position_odometer": self.position_odometer,
            "trip_schedule_relationship": self.trip_schedule_relationship,
            "trip_id": self.trip_id,
            "trip_start_date": self.trip_start_date,
            "trip_route_id": self.trip_route_id,
            "alc": self.alc
        }