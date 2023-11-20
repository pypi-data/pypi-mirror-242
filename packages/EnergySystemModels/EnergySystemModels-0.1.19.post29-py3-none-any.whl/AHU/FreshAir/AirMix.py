from AHU.air_humide import air_humide
from AHU.air_humide import air_humide_NB
from AHU.AirPort.AirPort import AirPort



        

class Object:
    def __init__(self):
        
        self.Inlet1=AirPort() 
        self.Inlet2=AirPort() 
        self.Outlet=AirPort()
        self.id=1
        self.T=5
        self.HR_FreshAir = 60
        self.F = 10000
        self.Pvsat=0
        self.w=0
        self.T_hum=0
        self.h=0
        self.P=101325
        
        self.F_dry=0
        self.m_as1=0
        self.m_as2=0
        
        
    def calculate(self):
        
        # self.F = self.m_vol * air_humide.rho_ah(self.T, self.HR_FreshAir, self.P)/3600 #kg/s
        # self.F = self.F/3600 #m3/s
        #Connecteur Inlet
                        
        self.Pvsat=air_humide.func_Pv_sat(self.T)
       # print("Pvsat=",self.Pvsat)
        self.w=air_humide.HA(self.Pvsat,self.HR_FreshAir,self.P)
       # print("HA=",self.w)
        self.T_hum=air_humide.Tw(self.T,self.HR_FreshAir)
      #  print("self.T_hum=",self.T_hum)
        self.h=air_humide.Enthalpie(self.T, self.w)
      #  print("self.h=",self.h)
        
        self.m_as1=self.Inlet1.F_kgs/(1+self.Inlet1.HA)
        self.m_as2=self.Inlet2.F_kgs/(1+self.Inlet2.HA)

        #connecteur   
      
        #self.Inlet1.HA=self.w
        #self.Inlet.P=
        self.Outlet.w=(self.Inlet1.HA*self.m_as1+self.Inlet2.HA*self.m_as2)/(self.m_as1+self.m_as2)
        self.Outlet.P=min(self.Inlet1.P,self.Inlet2.P)
        self.Outlet.h=(self.Inlet1.h*self.m_as1+self.Inlet2.h*self.m_as2)/(self.m_as1+self.m_as2)
        self.Outlet.F=self.Inlet1.F_kgs+self.Inlet2.F_kgs 
        self.T_outlet=air_humide_NB.Air3_Tdb(self.Outlet.w/1000,self.Outlet.P,self.Outlet.h)
        self.F_dry=(self.Outlet.F)/(1+self.Outlet.w/1000)
    
    
    



