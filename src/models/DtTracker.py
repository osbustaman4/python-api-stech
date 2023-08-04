class DtTracker():
    def __init__(self, dt_tracker ,lat, lng, altitude, speed, angle, params):
        self.dt_tracker = dt_tracker
        self.lat = lat
        self.lng = lng
        self.altitude = altitude
        self.speed = speed
        self.angle = angle
        self.params = params

    def to_json(self):
        return {
            'dt_tracker': self.dt_tracker,
            'lat': self.lat,
            'lng': self.lng,
            'altitude': self.altitude,
            'speed': self.speed,
            'angle': self.angle,
            'params': self.params
        }