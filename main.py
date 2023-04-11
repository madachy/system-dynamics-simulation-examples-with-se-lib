"""
System Dynamics Simulation Examples

This uses the following se-lib system dynamics modeling functions:

init_model()
    Instantiate a model for simulation

add_auxiliary(name, equation)
    Adds auxiliary equation or constant to the model

    Parameters:
    ----------
    name: str
      The name of the auxiliary 
    equation: str
      Equation for the auxiliary using other named model variables

add_stock(name, initial, inflows=[], outflows=[])
    Adds a stock to the model
    
    Parameters:
    ----------
    name: str
      The name of the stock 
    initial: float
      Initial value of stock at start of simulation
    inflows: list of float
      The names of the inflows to the stock
    outflows: list of float
      The names of the outflows to the stock

add_flow(name, equation)
    Adds a flow to the model

    Parameters
    ----------
    name: str
      The name of the flow 
    equation: str
      Equation for the flow using other named model variables
      
run_model()
    Executes the model
    
plot_graph(variables)
    displays matplotlib graph for each model variable

    Parameters
    ----------
    variables: variable name or list of variable names to plot on graph
    
    Returns:
    ----------
    matplotlib graph
    
save_graph(variables, filename)
    save graph to file

    Parameters:
    ----------
    variables: variable name or list of variable names to plot on graph
    filename: file name with format extension
"""

# import se-lib system dynamics modeling functions
from selib_sd import *

# exponential_growth
init_model(start=0, stop=10, dt=.5)
add_stock("level", 10, inflows=["rate"])
add_auxiliary("growth_fraction", .4)
add_flow("rate", "growth_fraction * level") 
run_model()
 
save_graph('level', filename="exponential_growth.png")

# negative feedback
init_model(start=0, stop=10, dt=.1)
add_stock("level", 50, inflows=["rate"])
add_auxiliary("time_constant", .5)
add_auxiliary("goal", 100)
add_flow("rate", "(goal - level) / time_constant") 
run_model()

save_graph(['level', 'rate'], filename="negative_feedback.png")

# Rayleigh Curve Staffing
init_model(start=0, stop=6, dt=.2)
add_stock("cumulative_effort", 0, inflows=["effort rate"])
add_flow("effort rate", "learning_function * (estimated_total_effort - cumulative_effort)")
add_auxiliary("learning_function", "manpower_buildup_parameter * time")
add_auxiliary("manpower_buildup_parameter", .5)
add_auxiliary("estimated_total_effort", 30)
run_model()

# on replit.com the generated graph window requires closing before further execution
#plot_graph('cumulative_effort', 'effort rate', "learning_function")
 
save_graph("effort rate", filename="rayleigh_curve_effort_rate.png")
save_graph(["effort rate", "cumulative_effort"], filename="rayleigh_curve_components.png")


# Battle Simulator using Lanchester's Law for Aimed Fire
import random
init_model(start=0, stop=1.5, dt=.2)
add_stock("blue", 1000, outflows=["blue_attrition"])
add_flow("blue_attrition", "red*red_lethality")
add_auxiliary("blue_lethality", .8)
add_stock("red", 800, outflows=["red_attrition"])
add_flow("red_attrition", "blue*blue_lethality")
add_auxiliary("red_lethality", .9)
run_model()

save_graph(["blue", "red"], filename="battle_simulator.png")


# test input functions
init_model(start=0, stop=10, dt=1)
add_stock("Level", 0, inflows=["Pulse", "Ramp"])
add_flow("Pulse", "pulse(100, 2)") # pulse of 100 at time 2
add_flow("Ramp", "ramp(3, 5) ") # ramp with slope 3 at time 5

run_model()

save_graph(['Level', 'Ramp', 'Pulse'], filename="test_inputs.png")
