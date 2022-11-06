from pyVenus import Resources, Connection, Device, Variable

Resources.read_submethods(r"C:\Program Files (x86)\HAMILTON\Library\Hamilton pH Module")

from venus_resources import Example_layout as lay
from venus_resources import Hamilton_ph_module_controller

con = Connection()
star_device = Device(con, lay.layout_file)
ph_module = Hamilton_ph_module_controller(con)

default_temperature = Variable(con)
ph_module_id = Variable(con)

ph_module.Initialize(star_device, 1, default_temperature, ph_module_id)

print(default_temperature)
print(ph_module_id)

con.close()
