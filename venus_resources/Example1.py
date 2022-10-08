class DeckLayout:
    class __Sequences:
        def __init__(self):
            self.trough2 = "ML_STAR.trough2"
            self.tubes = "ML_STAR.tubes"
            self.input_plates = "ML_STAR.input_plates"
            self.MlStar300ulStandardVolumeTipWithFilter = "ML_STAR.MlStar300ulStandardVolumeTipWithFilter"
            self.trough3 = "ML_STAR.trough3"
            self.trough1 = "ML_STAR.trough1"
            self.output_plate = "ML_STAR.output_plate"
            self.trough4 = "ML_STAR.trough4"
            self.trough5 = "ML_STAR.trough5"
            self.MlStar50ulTipWithFilter = "ML_STAR.MlStar50ulTipWithFilter"
            self.Waste = "ML_STAR.Waste"
            self.MlStar1000ulHighVolumeTipWithFilter = "ML_STAR.MlStar1000ulHighVolumeTipWithFilter"
            

    def __init__(self):
        self.layout_file = r"C:\Program Files (x86)\HAMILTON\pyVenus\Example1.lay"
        self.sequences = self.__Sequences()