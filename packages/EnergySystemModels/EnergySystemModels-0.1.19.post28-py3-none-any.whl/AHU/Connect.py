from AHU.AirPort.AirPort import AirPort
def Air_connect( entree=AirPort(),sortie=AirPort()): # a : port d'entrée d'un composant, b sortie composant 
    Inlet.w=Outlet.w #humidité absolue en g/kgas"
    entree.P=sortie.P
    entree.h=sortie.h #kJ/kgas
    Inlet.F=Outlet.F
    return "connectés"