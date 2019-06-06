from datetime import datetime


class Cbct:
    """
    CBCT object to hold extracted data
    """
    def __init__(self, **kwargs):
        self.date = kwargs["date"]
        self.time = datetime.strptime(kwargs["time"], "%H%M").strftime("%H:%M")
        self.comment = kwargs["comment"]
        self.treatment = kwargs["treatment"]

    def same_date(self, cbct):
        # type: (Cbct) -> bool

        """
        Checks whether another CBCT was performed on same (hashed) date

        :param cbct: CBCT to compare to
        :return: True or False
        """
        if self.date == cbct.date:
            return True
        return False

    def same_treatment(self, cbct):
        # type: (Cbct) -> bool

        """
        Checks whether another CBCT was performed fot the same (hashed)
        treatment

        :param cbct: CBCT to compare to
        :return: True or False
        """
        if self.treatment == cbct.treatment:
            return True
        return False

    def __repr__(self):
        return "For treatment #%s on date %s at %s with comment :\"%s\"" % (
            self.treatment, self.date, self.time, self.comment
        )

    def get_look_str(self):
        return "For treatment #%s on date %s at %s with comment :\n\n\t %s\n\n"\
               % (self.treatment, self.date, self.time, self.comment)
