import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
import numpy as np

class Object:
    def __init__(self, fluid):
        self.fluid = fluid
        self.T_min = CP.PropsSI(fluid, 'Ttriple')-273.15  # Triple point temperature in Kelvin
        self.T_max = CP.PropsSI(fluid, 'Tcrit')-273.15    # Critical temperature in Kelvin
        self.S_min = None
        self.S_max = None
        self.custom_points = []  # List to store custom points

    def set_temperature_range(self, T_min=None, T_max=None):
        if T_min is not None:
            self.T_min = T_min  # Convert to Kelvin
        if T_max is not None:
            self.T_max = T_max  # Convert to Kelvin

    def set_entropy_range(self, S_min=None, S_max=None):
        self.S_min = S_min
        self.S_max = S_max

    def add_points(self, points):
        for point in points:
            self.custom_points.append({'T': point['T'], 'S': point['S']})  # Temperature in Kelvin

    def show(self, draw_arrows=False):
        T_range = np.linspace(self.T_min, self.T_max, 100)
        plt.figure(figsize=(10, 6))

        # Plot saturation curves
        S_liquid = [CP.PropsSI('S', 'T', T+273.15, 'Q', 0, self.fluid) / 1000 for T in T_range]  # Convert S to kJ/kg-K
        S_vapor = [CP.PropsSI('S', 'T', T+273.15, 'Q', 1, self.fluid) / 1000 for T in T_range]  # Convert S to kJ/kg-K
        plt.plot(S_liquid, T_range, 'b')  # T in °C
        plt.plot(S_vapor, T_range, 'r')  # T in °C

        # Adjust S range if specified
        if self.S_min is not None or self.S_max is not None:
            plt.xlim(self.S_min, self.S_max)

        # Plot lines of constant pressure
        pressures = np.logspace(np.log10(CP.PropsSI(self.fluid, 'ptriple')), np.log10(CP.PropsSI(self.fluid, 'pcrit')), 10)
        for p in pressures:
            S = []
            for T in T_range:
                try:
                    T_K = T + 273.15  # Convert to Kelvin
                    entropy = CP.PropsSI('S', 'P', p, 'T', T_K, self.fluid) / 1000  # Convert S to kJ/kg-K
                    S.append(entropy)
                except ValueError:
                    # Skip points where properties cannot be calculated
                    continue
            if S:  # Check if the list is not empty
                plt.plot(S, T_range[:len(S)], 'k--', linewidth=0.5)  # T in °C
            

        # Plot custom points and optionally arrows
        for i in range(len(self.custom_points) - 1):
            point = self.custom_points[i]
            next_point = self.custom_points[i + 1]
            plt.scatter(point['S'], point['T'], color='red')  # T in °C
            if draw_arrows:
                plt.arrow(point['S'], point['T'], next_point['S'] - point['S'], next_point['T'] - point['T'],
                          head_width=0.05, head_length=0.1, fc='black', ec='black', linewidth=0.5)  # Arrow in black

        if self.custom_points:
            # Plot the last point
            last_point = self.custom_points[-1]
            plt.scatter(last_point['S'], last_point['T'], color='red')  # T in °C

        # Label the axes
        plt.xlabel('Entropy (kJ/kg-K)')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature-Entropy Diagram for ' + self.fluid)
        plt.grid(True)

        # Show the plot
        plt.show()


from ThermodynamicCycles import Temperature_Entropy_Chart

# Create an instance of the Temperature_Entropy_Chart class for Ammonia
Chart = Temperature_Entropy_Chart.Object('R407C')

# Show the Temperature-Entropy diagram
Chart.show()
