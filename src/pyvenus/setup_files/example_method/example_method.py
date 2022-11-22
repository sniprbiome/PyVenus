# import libraries
from pyvenus import Connection,Variable,Sequence,Device,Helpers
import pandas as pd

# import generated code
from venus_resources import Example_layout as lay
from venus_resources import LiquidClasses as lc
from venus_resources import Ml_star
from venus_resources import Channels1ml_8
from venus_resources import Pipetting

# start Hamilton run environment
con = Connection()

# init connection to STAR
star_device = Device(con, lay.layout_file)

# init submethod libraries
smt_star = Ml_star(con)
smt_ch = Channels1ml_8(con)
smt_pip = Pipetting(con)

# init deck sequences
tips_1000F = Sequence(con, lay.Sequences.MlStar1000ulHighVolumeTipWithFilter, deck_sequence=True)
tips_50F = Sequence(con, lay.Sequences.MlStar50ulTipWithFilter, deck_sequence=True)
buffer = Sequence(con, lay.Sequences.trough1, deck_sequence=True)
plate_input = Sequence(con, lay.Sequences.plate_input, deck_sequence=True)
plate_dilution = Sequence(con, lay.Sequences.plate_dilution, deck_sequence=True)
hitpicking_dispense = Sequence(con, name=lay.Sequences.plate_hitpicking, deck_sequence=True)
waste_ch = Sequence(con, lay.Sequences.Waste, deck_sequence=True)

# initialization routine for STAR
smt_star.initialize(star_device)

# transfer buffer to plate using individual commands
smt_ch.tip_pickup(star_device, tips_1000F)
while plate_dilution.current > 0:
    smt_ch.aspirate(star_device, buffer, 100, lc.lcHighVolumeFilter_Water_DispenseSurface_Empty, increment_sequence=0)
    smt_ch.dispense(star_device, plate_dilution, 100)
smt_ch.tip_eject(star_device, waste_ch)
plate_dilution.current = 1

# transfer buffer to plate using a pipetting submethod
smt_pip.add_buffer(star_device, buffer, plate_dilution, tips_1000F, 100)

# example of how to use output parameters
number_of_transfers = Variable(con)
smt_pip.input_to_dilution(star_device, plate_input, plate_dilution, tips_50F, 10, number_of_transfers)
print(f"Number of transfers: {number_of_transfers}")

# generate sequences on the fly from a labware ID
smt_pip.input_to_dilution(
    star_device, 
    Sequence(con).from_list([lay.Labware.mtp_plate], Helpers.get_well_map(96)), 
    Sequence(con).from_list([lay.Labware.dwp_plate], Helpers.get_well_map(96)), 
    tips_50F, 
    10, 
    number_of_transfers)

# hitpicking example from worklist file
hitpicking_aspirate = Sequence(con).from_dataframe(pd.read_excel("example_worklist.xlsx", "Sheet1"))
while hitpicking_aspirate.remaining > 0:
    smt_ch.tip_pickup(star_device, tips_50F)
    smt_ch.aspirate(
        star_device, 
        hitpicking_aspirate, 
        30, 
        lc.lcTip_50ulFilter_Water_DispenseJet_Empty)
    smt_ch.dispense(star_device, hitpicking_dispense, dispense_remaining=1, cLLD_sensitivity=0, fixed_height=10)
    smt_ch.tip_eject(star_device, waste_ch)
hitpicking_dispense.current = 1

# sort hitpicking worklist by x and y coordinates
hitpicking_aspirate = Sequence(con)
(hitpicking_aspirate
    .from_dataframe(pd.read_excel("example_worklist.xlsx", "Sheet1"))
    .get_dataframe(include_position_data=True)
    .sort_values(by=['x','y'], ascending=[True,False])
    .pipe(hitpicking_aspirate.from_dataframe)
) 

# pipette sorted hitpicking list
while hitpicking_aspirate.remaining > 0:
    smt_ch.tip_pickup(star_device, tips_50F)
    smt_ch.aspirate(star_device, hitpicking_aspirate, 30, lc.lcTip_50ulFilter_Water_DispenseJet_Empty)
    smt_ch.dispense(star_device, hitpicking_dispense, dispense_remaining=1, cLLD_sensitivity=0, fixed_height=10)
    smt_ch.tip_eject(star_device, waste_ch)

# close Hamilton run environment
con.close()


















