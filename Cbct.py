from Log_element import Log_element


class Cbct(Log_element):
    """
    CBCT object to hold extracted data
    """
    def __init__(self, **kwargs):
        Log_element.__init__(self, **kwargs)
        self.type = "image"
        self.type_type = "CBCT"
