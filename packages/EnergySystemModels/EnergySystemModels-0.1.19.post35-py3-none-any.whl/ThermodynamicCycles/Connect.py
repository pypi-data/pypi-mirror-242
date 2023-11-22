from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
def Fluid_connect( a=FluidPort(),b=FluidPort()):
    a.fluid=b.fluid
    a.P=b.P
    a.h=b.h
    a.F=b.F
    return "connectés"