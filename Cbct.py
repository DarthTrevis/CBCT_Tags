from LogElement import LogElement


class Cbct(LogElement):
    """
    CBCT object to hold extracted data
    """
    def __init__(self, **kwargs):
        LogElement.__init__(self, **kwargs)
        self.type = "image"
        self.type_type = "CBCT"
