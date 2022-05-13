from opentrons import labware, instruments

# Custom protocol for Opentrons OT-2 liquid handling robot
# Enables index primer addition to a single 96-well PCR plate from forward and reverse index primer plates 
# Increases possible index combinations from 96 to 13824 and enables simultaneous sequencing of 144 96-well plates
# Updated 13May2022

metadata = {
    'protocolName': 'Plate Copying',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }

#identify slot on stage where multichannel pipette tips and 96-well plates are clipped in

fwd_slot = '6'

rev_slot = '8'

dest_slot = '9'

tip_slots = ['3', '5']

tip_racks = [labware.load('tiprack-10ul', slot) for slot in tip_slots]

#identify robot head loading slot where pipette is clipped in

p10multi = instruments.P10_Multi(
    mount='right',
    tip_racks=tip_racks)

container_choices = [
    '96-flat', '96-PCR-tall', '96-deep-well', '384-plate']

#head speed tuned to minimize splatter and runtime

max_speed_per_axis = {
            'x': (600), 'y': (600), 'z': (130), 'a': (130), 'b': (40),
            'c': (40)}
        robot.head_speed(
            combined_speed=max(max_speed_per_axis.values()),
            **max_speed_per_axis)

def run_custom_protocol(
        transfer_volume: float=2,
        primer_container: 'StringSelection...'='96-flat',
        destination_container: 'StringSelection...'='96-flat',
        starting_col_fwd: float=1,
        starting_col_rev: float=1):
    
    # Converts plain english notation for starting column to python (base 0)
    
    py_starting_col_fwd = starting_col_fwd - 1
    py_starting_col_rev = starting_col_rev - 1

    # Load labware dimensions from 'labware'

    fwd_plate = labware.load(primer_container, fwd_slot)
    rev_plate = labware.load(primer_container, rev_slot)
    dest_plate = labware.load(destination_container, dest_slot)

    # Store total number of columns in sample plate
    
    col_count = len(dest_plate.cols())

    # Make vector for forward index column order
    
    if py_starting_col_fwd != 0:
        custom_fwd_cols = list(range(py_starting_col_fwd,len(fwd_plate.cols()))) + list(range(0,py_starting_col_fwd))
    else:
        custom_fwd_cols = range(len(fwd_plate.cols()))

    # Make vector for reverse index column order

    if py_starting_col_rev != 0:
        custom_rev_cols = list(range(py_starting_col_rev,len(rev_plate.cols()))) + list(range(0,py_starting_col_rev))
    else:
        custom_rev_cols = range(len(rev_plate.cols()))

    air_vol = 1

    # distribute forward primers
    for col_index, cust_index in enumerate(custom_fwd_cols):
        dest_wells = dest_plate.cols(col_index)
        fwd_wells = fwd_plate.cols(cust_index)

        p10multi.distribute(
            transfer_volume, fwd_wells, dest_wells, air_gap=air_vol, blow_out=True, disposal_vol=0)
        mix_after=(3, 10)

    # distribute reverse primers
    for col_index, cust_index in enumerate(custom_rev_cols):
        dest_wells = dest_plate.cols(col_index)
        rev_wells = rev_plate.cols(cust_index)

        p10multi.distribute(
            transfer_volume, rev_wells, dest_wells, air_gap=air_vol, blow_out=True, disposal_vol=0)
        mix_after=(3, 10)

#ATTN: EDIT HERE
#Assign starting columns here!
#Use plain English column numbers. 
#Do NOT use python zero base index logic to assign starting column number.
#This script will convert your column number for you

run_custom_protocol(**{'transfer_volume': 1.0, 'primer_container': '96-flat', 'destination_container': '96-PCR-tall', 'starting_col_fwd': 4, 'starting_col_rev': 1 })



