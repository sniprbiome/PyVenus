from numpy import number
from pyVenus import Connection,Variable,Sequence,Array,Device,Helpers, helpers

from venus_resources import Example_layout as lay
from venus_resources import LiquidClasses as lc
from venus_resources import Ml_star
from venus_resources import Channels1ml_8
from venus_resources import Pipetting

con = Connection()

star_device = Device(con, lay.layout_file)

smt_star = Ml_star(con)
smt_ch = Channels1ml_8(con)
smt_pip = Pipetting(con)

tips_1000F = Sequence(con, lay.Sequences.MlStar1000ulHighVolumeTipWithFilter, deck_sequence=True)
tips_50F = Sequence(con, lay.Sequences.MlStar50ulTipWithFilter, deck_sequence=True)
buffer = Sequence(con, lay.Sequences.trough1, deck_sequence=True)
plate_input = Sequence(con, lay.Sequences.plate_input, deck_sequence=True)
plate_dilution = Sequence(con, lay.Sequences.plate_dilution, deck_sequence=True)
plate_output = Sequence(con, lay.Sequences.plate_output, deck_sequence=True)
waste_ch = Sequence(con, lay.Sequences.Waste, deck_sequence=True)

smt_star.initialize(star_device)
"""
smt_ch.tip_pickup(star_device, tips_1000F)
number_of_transfers = 0
while plate_dilution.current > 0:
    number_of_transfers = number_of_transfers + 1
    smt_ch.aspirate(star_device, buffer, 100, lc.lcHighVolumeFilter_Water_DispenseSurface_Empty, increment_sequence=0)
    smt_ch.dispense(star_device, plate_dilution, 100)
smt_ch.tip_eject(star_device, waste_ch)
print("Number of transfers: ")
print(number_of_transfers) """


tips_1000F.set


number_of_transfers = Variable(con)
smt_pip.add_buffer(
    star_device, 
    buffer, 
    Sequence(con).from_list([lay.Labware.dwp_plate], Helpers.get_well_map(96)), 
    tips_1000F, 
    100, 
    number_of_transfers)
print("Number of transfers: ")
print(number_of_transfers)



smt_pip.input_to_dilution(star_device, plate_input, plate_dilution, tips_50F, 10)



smt_pip.dilution_to_output(star_device, plate_dilution, plate_output, tips_50F, 5)


con.close()

