import pysd
import matplotlib.pyplot as plot
import matplotlib as mpl

mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False


def init_model(start, stop, dt):
  global xmile_header, model, model_specs
  xmile_header = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <xmile version="1.0" xmlns="http://docs.oasis-open.org/xmile/ns/XMILE/v1.0">
        <header>
            <vendor>Ray Madachy</vendor>
            <name>Battle Simulator</name>
            <options>
                <uses_outputs/>
            </options>
            <product version="1.0">PyML .20 dev</product>
        </header>"""

  model_specs = f"""
        <sim_specs>
                <stop>{stop}</stop>
                <start>{start}</start>
                <dt>{dt}</dt>
        </sim_specs>"""
  model = ""
  build_model()


def add_stock(name, initial, inflows=[], outflows=[]):
  global model
  inflow_string, outflow_string = "", ""
  for flow in inflows:
    inflow_string += f"""<inflow>"{flow}"</inflow>"""
  for flow in outflows:
    outflow_string += f"""<outflow>"{flow}"</outflow>"""
  model += f"""
                <stock name="{name}">
                    <doc>{name}</doc>
                    {inflow_string}
                    {outflow_string}
                    <eqn>{initial}</eqn>
                </stock>"""
  build_model()


def add_flow(name, equation):
  global model
  model += f"""
                <flow name="{name}">
                    <doc>{name}</doc>
                    <eqn>{equation}</eqn>
                </flow>"""
  build_model()


def add_auxiliary(name, equation):
  global model
  model += f"""
                <aux name="{name}">
                    <doc>{name}</doc>
                    <eqn>{equation}</eqn>
                </aux>"""
  build_model()


def build_model():
  global xmile_string
  xmile_closing = """
    </xmile>
    """
  model_string = """
        <model>
            <variables>""" + f"{model}" + """
            </variables>
        </model>"""
  xmile_string = xmile_header + model_specs + model_string + xmile_closing
  with open('test.xmile', 'w') as f:
    f.write(xmile_string)


def run_model():
  import pysd
  global output
  model = pysd.read_xmile('./test.xmile')
  output = model.run(progress=False)
  return (output)


def plot_graph(*outputs):
  for var in outputs:
    fig, axis = plot.subplots(figsize=(3, 3))
    axis.set(xlabel='Time', ylabel=var)
    axis.plot(output.index, output[var].values, label=var)
    axis.legend(loc="best", )
    plot.show()


def save_graph(*outputs, filename="graph.png"):
  for var in outputs:
    #print(var)
    fig, axis = plot.subplots()
    axis.set(xlabel='Time', ylabel=var)
    axis.plot(output.index, output[var].values, label=var)
    axis.legend(loc="best", )
    #plot.show()
    plot.savefig(filename)


"""
def save_graph(*outputs, filename="graph.png"):
    print(outputs[0], len(outputs[0]))
    for i, var in enumerate(outputs[0]):
        fig, axis = plot.subplots(len(outputs[0]))
        print(i)
        axis[i].set(xlabel = 'Time', ylabel = var)
        axis[i].plot(output.index, output[var].values, label=var)
        axis[i].legend(loc="best", )
        #plot.show()
    plot.savefig(filename)
"""
