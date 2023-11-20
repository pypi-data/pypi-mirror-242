from AHU.air_humide import air_humide



class AirPort:
    def __init__(self):
        self.F_kgs=0 # d'air d'air
        self.P = 101325 # pression
        self.h = 10000 # enthalpie spéc
        self.HA = 0 # Humidité absolue
        
    def propriete(self):
        self.result="HR,Pv_sat,T="
        self.T=air_humide.Temperature(self.h, self.HA)
        self.Pv_sat=air_humide.Pv_sat(self.T)
        self.HR=air_humide.HR(self.Pv_sat, self.HA, self.P)
        return self.result,self.HR,self.Pv_sat,self.T
    

