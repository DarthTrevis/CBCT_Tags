from datetime import datetime, time


class Log_element:
    """
    Log element object to hold extracted data
    """
    def __init__(self, **kwargs):
        self.date = kwargs["date"]
        self.time = datetime.strptime(kwargs["time"], "%H%M").strftime("%H:%M")
        self.comment = kwargs["comment"]
        self.treatment = kwargs["treatment"]

    def same_date(self, l_elem):
        # type: (Log_element) -> bool

        """
        Checks whether another log_element was logged on same (hashed) date

        :param l_elem: Log element to compare to
        :return: True or False
        """
        if self.date == l_elem.date:
            return True
        return False

    def same_treatment(self, l_elem):
        # type: (Cbct) -> bool

        """
        Checks whether another log_element was logged for the same treatment
        :param l_elem: Log element to compare to
        :return: True or False
        """
        if self.treatment == l_elem.treatment:
            return True
        return False

    def __repr__(self):
        return "For treatment #%s on date %s at %s with comment :\"%s\"" % (
            self.treatment, self.date, self.time, self.comment)

    def get_look_str(self):
        if self.comment:
            comment = "\033[01;33m"+self.comment+"\033[00;37m"
        else:
            comment = "\033[00;31mNot commented\033[00;37m"
        return "For treatment #%s on date %s at \033[01;34m%s\033[00;37m " \
               "with comment :\n\n\t %s\n\n"\
               % (self.treatment, self.date, self.time, comment)

    def get_time(self):
        return datetime.strptime(self.time, "%H:%M")