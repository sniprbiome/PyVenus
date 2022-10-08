from pyVenus import Connection, Variable, Array, Sequence, Device


class Channels1mL_8:
    def __init__(self, con: Connection):
        self.__con = con
        self.__con.execute(definitions=r'#include "C:\Program Files (x86)\HAMILTON\pyVenus_test\pyVenus\smt\channels1mL_8.hs_"')

    def tip_pickup(self, ML_STAR: Device, io_seqTips: Sequence, i_blnIncrementSequence=1, i_strChannelPattern="11111111", i_intSequenceUse=1):
        """
        Python function generated from submethod 'tip_pickup' in 'channels1mL_8.smt'
        Pickup tips using 1000 uL channels (8 channel system)
            :param ML_STAR: Device (in_out) - ML_STAR
            :param io_seqTips: Sequence (in_out) - Sequence over tips
            :param i_blnIncrementSequence: Variable (in) - Increment sequence after tip pickup?
            :param i_strChannelPattern: Variable (in) - Channel pattern to use
            :param i_intSequenceUse: Variable (in) - 1 = "All sequence positions", 2 = "Keep channel pattern"
        """

        # push all variables that are passed into the submethod
        
        io_seqTips.push()
        
        
        
        

        # generate the parameter string for the HSL function call
        parameter_string = ""
        
        parameter_string += ML_STAR.name
        
        
        parameter_string += ", " + io_seqTips.name
        
        if isinstance(i_blnIncrementSequence, Variable):
            value = i_blnIncrementSequence.value
        else:
            value = i_blnIncrementSequence
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_strChannelPattern, Variable):
            value = i_strChannelPattern.value
        else:
            value = i_strChannelPattern
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_intSequenceUse, Variable):
            value = i_intSequenceUse.value
        else:
            value = i_intSequenceUse
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        # call the HSL function
        self.__con.execute("CHANNELS1ML_8::tip_pickup(" + parameter_string + ");")

        # pull all variables there were returned by the submethod
        io_seqTips.pull()
        
    def tip_eject(self, ML_STAR: Device, io_seqEjectPosition: Sequence, i_blnDefaultWaste=1, i_blnIncrementSequence=0, i_strChannelPattern="11111111", i_intSequenceUse=1):
        """
        Python function generated from submethod 'tip_eject' in 'channels1mL_8.smt'
        Eject tips using 1000 uL channels  (8 channel system)
            :param ML_STAR: Device (in_out) - 
            :param io_seqEjectPosition: Sequence (in_out) - Sequence with eject positions
            :param i_blnDefaultWaste: Variable (in) - Eject to default waste?
            :param i_blnIncrementSequence: Variable (in) - Increment eject position sequence?
            :param i_strChannelPattern: Variable (in) - Channel pattern to use
            :param i_intSequenceUse: Variable (in) - 1 = "All sequence positions", 2 = "Keep channel pattern"
        """

        # push all variables that are passed into the submethod
        
        io_seqEjectPosition.push()
        
        
        
        
        

        # generate the parameter string for the HSL function call
        parameter_string = ""
        
        parameter_string += ML_STAR.name
        
        
        parameter_string += ", " + io_seqEjectPosition.name
        
        if isinstance(i_blnDefaultWaste, Variable):
            value = i_blnDefaultWaste.value
        else:
            value = i_blnDefaultWaste
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_blnIncrementSequence, Variable):
            value = i_blnIncrementSequence.value
        else:
            value = i_blnIncrementSequence
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_strChannelPattern, Variable):
            value = i_strChannelPattern.value
        else:
            value = i_strChannelPattern
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_intSequenceUse, Variable):
            value = i_intSequenceUse.value
        else:
            value = i_intSequenceUse
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        # call the HSL function
        self.__con.execute("CHANNELS1ML_8::tip_eject(" + parameter_string + ");")

        # pull all variables there were returned by the submethod
        io_seqEjectPosition.pull()
        
    def aspirate(self, ML_STAR: Device, io_seqAspirate: Sequence, i_fltVolume, i_strLiquidClass, i_blnIncrementSequence=1, i_blnLiquidFollowing=1, i_strChannelPattern="11111111", i_intSequenceUse=1, i_intcLLDSensitivity=1, i_fltSubmergeDepth=2, i_fltFixedHeight=0, i_fltRetractDistance=0, i_blnTouchOff=0, i_fltTouchOffHeight=0, i_intpLLDSensitivity=0, i_fltMaxHeightDifference=0, i_intAspirationMode=1, i_intMixCycles=0, i_fltMixPosition=0, i_fltMixVolume=0):
        """
        Python function generated from submethod 'aspirate' in 'channels1mL_8.smt'
        Aspirate using the 1000 uL channels (8 channel system)
            :param ML_STAR: Device (in_out) - 
            :param io_seqAspirate: Sequence (in_out) - Sequence with positions for aspiration
            :param i_fltVolume: Variable (in) - Volume to aspirate (uL)
            :param i_strLiquidClass: Variable (in) - Liquid class to use for aspiration
            :param i_blnIncrementSequence: Variable (in) - Increment sequence after aspiration?
            :param i_blnLiquidFollowing: Variable (in) - Follow liquid level during aspiration?
            :param i_strChannelPattern: Variable (in) - Channel pattern to use
            :param i_intSequenceUse: Variable (in) - 1 = "All sequence positions", 2 = "Keep channel pattern"
            :param i_intcLLDSensitivity: Variable (in) - Conductive LLD, 0 = off, 1 - 4 = high - low, 5 = "Get from labware definition"
            :param i_fltSubmergeDepth: Variable (in) - Submerge depth after LLD (mm)
            :param i_fltFixedHeight: Variable (in) - Fixed height from bottom, if LLD disabled (mm)
            :param i_fltRetractDistance: Variable (in) - Retract distance before air aspiration, if LLD disabled (mm)
            :param i_blnTouchOff: Variable (in) - Find container bottom with physical touch off?
            :param i_fltTouchOffHeight: Variable (in) - Aspiration height above touch off point (mm)
            :param i_intpLLDSensitivity: Variable (in) - Pressure LLD, 0 = off, 1 - 4 = high - low, 5 = "Get from liquid class"
            :param i_fltMaxHeightDifference: Variable (in) - Maximum height difference between cLLD and pLLD (mm)
            :param i_intAspirationMode: Variable (in) - 1 = Normal aspiration, 2 = consecutive aspiration, 3 = aspirate all
            :param i_intMixCycles: Variable (in) - Number of mixing cycles
            :param i_fltMixPosition: Variable (in) - Position offset for mixing, if LLD enabled (mm)
            :param i_fltMixVolume: Variable (in) - Volume used for mixing (uL)
        """

        # push all variables that are passed into the submethod
        
        io_seqAspirate.push()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        # generate the parameter string for the HSL function call
        parameter_string = ""
        
        parameter_string += ML_STAR.name
        
        
        parameter_string += ", " + io_seqAspirate.name
        
        if isinstance(i_fltVolume, Variable):
            value = i_fltVolume.value
        else:
            value = i_fltVolume
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_strLiquidClass, Variable):
            value = i_strLiquidClass.value
        else:
            value = i_strLiquidClass
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_blnIncrementSequence, Variable):
            value = i_blnIncrementSequence.value
        else:
            value = i_blnIncrementSequence
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_blnLiquidFollowing, Variable):
            value = i_blnLiquidFollowing.value
        else:
            value = i_blnLiquidFollowing
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_strChannelPattern, Variable):
            value = i_strChannelPattern.value
        else:
            value = i_strChannelPattern
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_intSequenceUse, Variable):
            value = i_intSequenceUse.value
        else:
            value = i_intSequenceUse
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_intcLLDSensitivity, Variable):
            value = i_intcLLDSensitivity.value
        else:
            value = i_intcLLDSensitivity
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltSubmergeDepth, Variable):
            value = i_fltSubmergeDepth.value
        else:
            value = i_fltSubmergeDepth
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltFixedHeight, Variable):
            value = i_fltFixedHeight.value
        else:
            value = i_fltFixedHeight
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltRetractDistance, Variable):
            value = i_fltRetractDistance.value
        else:
            value = i_fltRetractDistance
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_blnTouchOff, Variable):
            value = i_blnTouchOff.value
        else:
            value = i_blnTouchOff
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltTouchOffHeight, Variable):
            value = i_fltTouchOffHeight.value
        else:
            value = i_fltTouchOffHeight
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_intpLLDSensitivity, Variable):
            value = i_intpLLDSensitivity.value
        else:
            value = i_intpLLDSensitivity
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltMaxHeightDifference, Variable):
            value = i_fltMaxHeightDifference.value
        else:
            value = i_fltMaxHeightDifference
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_intAspirationMode, Variable):
            value = i_intAspirationMode.value
        else:
            value = i_intAspirationMode
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_intMixCycles, Variable):
            value = i_intMixCycles.value
        else:
            value = i_intMixCycles
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltMixPosition, Variable):
            value = i_fltMixPosition.value
        else:
            value = i_fltMixPosition
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltMixVolume, Variable):
            value = i_fltMixVolume.value
        else:
            value = i_fltMixVolume
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        # call the HSL function
        self.__con.execute("CHANNELS1ML_8::aspirate(" + parameter_string + ");")

        # pull all variables there were returned by the submethod
        io_seqAspirate.pull()
        
    def dispense(self, ML_STAR: Device, io_seqDispense: Sequence, i_fltVolume=0, i_blnDispenseRemaining=0, i_blnIncrementSequence=1, i_blnLiquidFollowing=1, i_strChannelPattern="11111111", i_intSequenceUse=1, i_intcLLDSensitivity=1, i_fltSubmergeDepth=2, i_fltFixedHeight=0, i_fltRetractDistance=0, i_blnTouchOff=0, i_fltTouchOffHeight=0, i_blnSideTouch=0, i_blnMinimizeZHeight=0, i_intMixCycles=0, i_fltMixPosition=0, i_fltMixVolume=0):
        """
        Python function generated from submethod 'dispense' in 'channels1mL_8.smt'
        Dispense using 1000 uL channels (8 channel system)
            :param ML_STAR: Device (in_out) - 
            :param io_seqDispense: Sequence (in_out) - Sequence with dispense positions
            :param i_fltVolume: Variable (in) - Volume to dispense, ignored if DispenseRemaining enabled (uL)
            :param i_blnDispenseRemaining: Variable (in) - Dispense all remaining volume in tip
            :param i_blnIncrementSequence: Variable (in) - Increment sequence after dispense
            :param i_blnLiquidFollowing: Variable (in) - Follow liquid level during dispense?
            :param i_strChannelPattern: Variable (in) - Channel pattern to use
            :param i_intSequenceUse: Variable (in) - 1 = "All sequence positions", 2 = "Keep channel pattern"
            :param i_intcLLDSensitivity: Variable (in) - Conductive LLD, 0 = off, 1 - 4 = height - low, 5 = "Get from labware definition"
            :param i_fltSubmergeDepth: Variable (in) - Submerge depth below LLD (mm)
            :param i_fltFixedHeight: Variable (in) - Fixed height from bottom, iff LLD disabled (mm)
            :param i_fltRetractDistance: Variable (in) - Retract distance before air aspiration, if LLD disabled (mm)
            :param i_blnTouchOff: Variable (in) - Find container bottom with physical touch off?
            :param i_fltTouchOffHeight: Variable (in) - Dispense height above touch off point (mm)
            :param i_blnSideTouch: Variable (in) - Perform side touch?
            :param i_blnMinimizeZHeight: Variable (in) - Minimize Z height after aspiration? (DANGER OF COLLISION!)
            :param i_intMixCycles: Variable (in) - Number of mixing cycles
            :param i_fltMixPosition: Variable (in) - Position offset for mixing, if LLD enabled (mm)
            :param i_fltMixVolume: Variable (in) - Volume for mixing (uL)
        """

        # push all variables that are passed into the submethod
        
        io_seqDispense.push()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        # generate the parameter string for the HSL function call
        parameter_string = ""
        
        parameter_string += ML_STAR.name
        
        
        parameter_string += ", " + io_seqDispense.name
        
        if isinstance(i_fltVolume, Variable):
            value = i_fltVolume.value
        else:
            value = i_fltVolume
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_blnDispenseRemaining, Variable):
            value = i_blnDispenseRemaining.value
        else:
            value = i_blnDispenseRemaining
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_blnIncrementSequence, Variable):
            value = i_blnIncrementSequence.value
        else:
            value = i_blnIncrementSequence
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_blnLiquidFollowing, Variable):
            value = i_blnLiquidFollowing.value
        else:
            value = i_blnLiquidFollowing
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_strChannelPattern, Variable):
            value = i_strChannelPattern.value
        else:
            value = i_strChannelPattern
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_intSequenceUse, Variable):
            value = i_intSequenceUse.value
        else:
            value = i_intSequenceUse
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_intcLLDSensitivity, Variable):
            value = i_intcLLDSensitivity.value
        else:
            value = i_intcLLDSensitivity
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltSubmergeDepth, Variable):
            value = i_fltSubmergeDepth.value
        else:
            value = i_fltSubmergeDepth
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltFixedHeight, Variable):
            value = i_fltFixedHeight.value
        else:
            value = i_fltFixedHeight
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltRetractDistance, Variable):
            value = i_fltRetractDistance.value
        else:
            value = i_fltRetractDistance
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_blnTouchOff, Variable):
            value = i_blnTouchOff.value
        else:
            value = i_blnTouchOff
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltTouchOffHeight, Variable):
            value = i_fltTouchOffHeight.value
        else:
            value = i_fltTouchOffHeight
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_blnSideTouch, Variable):
            value = i_blnSideTouch.value
        else:
            value = i_blnSideTouch
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_blnMinimizeZHeight, Variable):
            value = i_blnMinimizeZHeight.value
        else:
            value = i_blnMinimizeZHeight
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_intMixCycles, Variable):
            value = i_intMixCycles.value
        else:
            value = i_intMixCycles
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltMixPosition, Variable):
            value = i_fltMixPosition.value
        else:
            value = i_fltMixPosition
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        
        if isinstance(i_fltMixVolume, Variable):
            value = i_fltMixVolume.value
        else:
            value = i_fltMixVolume
        parameter_string += ", " + (f'"{value}"' if isinstance(value, str) else str(value))
        # call the HSL function
        self.__con.execute("CHANNELS1ML_8::dispense(" + parameter_string + ");")

        # pull all variables there were returned by the submethod
        io_seqDispense.pull()
        
    