# import PyVenus
from pyvenus import Resources, Connection, Device, Variable

# generate python class from pH module submethod library
Resources.read_submethods(r"C:\Program Files (x86)\HAMILTON\Library\Hamilton pH Module")

# import generated classes
from venus_resources import Example_layout as lay
from venus_resources import Hamilton_ph_module_controller

# init
con = Connection()
star_device = Device(con, lay.layout_file)
ph_module = Hamilton_ph_module_controller(con)

# initialize variable objects for output parameters
default_temperature = Variable(con)
ph_module_id = Variable(con)

# call init function of pH module
ph_module.Initialize(star_device, 1, default_temperature, ph_module_id)

# print values returned from init function
print(default_temperature)
print(ph_module_id)

# close run environment
con.close()
