from pyVenus import Resources, Connection


Resources.read_submethods(r"C:\Program Files (x86)\HAMILTON\Library\Hamilton pH Module")

con = Connection()

from venus_resources import Hamilton_ph_module_controller

ph = Hamilton_ph_module_controller(con)

ph.Measure()
