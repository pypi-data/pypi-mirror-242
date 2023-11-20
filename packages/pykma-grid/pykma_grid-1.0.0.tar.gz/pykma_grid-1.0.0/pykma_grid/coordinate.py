import math

class Coordinate:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.map = {
            "Re": 6371.00877, 
            "grid": 5.0, 
            "slat1": 30.0, 
            "slat2": 60.0, 
            "olon": 126.0, 
            "olat": 38.0, 
            "xo": 210 / 5.0, 
            "yo": 675 / 5.0, 
            "first": 0
        }

    def lamcproj(self, lat, lon):
        PI = math.asin(1.0) * 2.0
        DEGRAD = PI / 180.0
        
        if self.map["first"] == 0:
            re = self.map["Re"] / self.map["grid"]
            slat1 = self.map["slat1"] * DEGRAD
            slat2 = self.map["slat2"] * DEGRAD
            olon = self.map["olon"] * DEGRAD
            olat = self.map["olat"] * DEGRAD

            sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
            sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
            sf = math.tan(PI * 0.25 + slat1 * 0.5)
            sf = pow(sf, sn) * math.cos(slat1) / sn
            ro = math.tan(PI * 0.25 + olat * 0.5)
            ro = re * sf / pow(ro, sn)
            self.map["first"] = 1
        else:
            re = self.map["Re"] / self.map["grid"]
            slat1 = self.map["slat1"] * DEGRAD
            slat2 = self.map["slat2"] * DEGRAD
            olon = self.map["olon"] * DEGRAD
            olat = self.map["olat"] * DEGRAD
            sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
            sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
            sf = math.tan(PI * 0.25 + slat1 * 0.5)
            sf = pow(sf, sn) * math.cos(slat1) / sn
            ro = math.tan(PI * 0.25 + olat * 0.5)
            ro = re * sf / pow(ro, sn)

        ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
        ra = re * sf / pow(ra, sn)
        theta = lon * DEGRAD - olon
        if theta > PI:
            theta -= 2.0 * PI
        if theta < -PI:
            theta += 2.0 * PI
        theta *= sn

        x = ra * math.sin(theta) + self.map["xo"]
        y = ro - ra * math.cos(theta) + self.map["yo"]

        if x < 0 or y < 0:
            return {"error": "Invalid coordinate conversion."}

        return {"x": x, "y": y}

    @property
    def gridX(self):
        return self.lamcproj(self.latitude, self.longitude)["x"]

    @property
    def gridY(self):
        return self.lamcproj(self.latitude, self.longitude)["y"]
