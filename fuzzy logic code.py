import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define the fuzzy variables
soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_moisture')
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
water_amount = ctrl.Consequent(np.arange(0, 101, 1), 'water_amount')

# Define the fuzzy sets for soil moisture
soil_moisture['dry'] = fuzz.trimf(soil_moisture.universe, [0, 0, 50])
soil_moisture['optimal'] = fuzz.trimf(soil_moisture.universe, [30, 50, 70])
soil_moisture['wet'] = fuzz.trimf(soil_moisture.universe, [50, 100, 100])

# Define the fuzzy sets for temperature
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 15])
temperature['moderate'] = fuzz.trimf(temperature.universe, [10, 20, 30])
temperature['hot'] = fuzz.trimf(temperature.universe, [25, 40, 40])

# Define the fuzzy sets for humidity
humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 50])
humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['high'] = fuzz.trimf(humidity.universe, [50, 100, 100])

# Define the fuzzy sets for water amount
water_amount['low'] = fuzz.trimf(water_amount.universe, [0, 0, 50])
water_amount['medium'] = fuzz.trimf(water_amount.universe, [30, 50, 70])
water_amount['high'] = fuzz.trimf(water_amount.universe, [50, 100, 100])

# Define the fuzzy rules
rule1 = ctrl.Rule(soil_moisture['dry'] & temperature['hot'] & humidity['low'], water_amount['high'])
rule2 = ctrl.Rule(soil_moisture['dry'] & temperature['moderate'] & humidity['medium'], water_amount['medium'])
rule3 = ctrl.Rule(soil_moisture['optimal'] & temperature['moderate'] & humidity['medium'], water_amount['low'])
rule4 = ctrl.Rule(soil_moisture['wet'] | temperature['cold'], water_amount['low'])

# Create a control system and simulation
irrigation_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
irrigation_simulation = ctrl.ControlSystemSimulation(irrigation_control)

# Test the system with specific inputs
input_soil_moisture = 40  # Example input: 40% soil moisture
input_temperature = 25    # Example input: 25°C temperature
input_humidity = 60       # Example input: 60% humidity

irrigation_simulation.input['soil_moisture'] = input_soil_moisture
irrigation_simulation.input['temperature'] = input_temperature
irrigation_simulation.input['humidity'] = input_humidity

# Compute the output water amount
irrigation_simulation.compute()
output_water_amount = irrigation_simulation.output['water_amount']

print(f"Input Soil Moisture: {input_soil_moisture}%")
print(f"Input Temperature: {input_temperature}°C")
print(f"Input Humidity: {input_humidity}%")
print(f"Output Water Amount: {output_water_amount:.2f}%")
