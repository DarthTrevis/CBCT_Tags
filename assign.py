"""
License GNU GPL 3
Author: Florian Charlier
"""


import csv
import Cbct
from typing import List
from colorama import init as colorama_init


# todo: convert cbcts to log_elements in is_why

def is_why(cbct, reason_to_test, next_cbcts_to_preview=None):
    # type: (Cbct, str, List[Cbct])-> (bool, str)
    """
    Returns the user or automatic assessment based on rules on whether the
    reason suggested is why the CBCT was rejected, if applicable, or allows to
    raise SystemExit.

    :param cbct: Cbct object to evaluate
    :param reason_to_test: Possible explanation evaluated
    :param next_cbcts_to_preview: List of following CBCTs performed to get more
            information
    :return: Probably true or false explanation
    """
    print("-------------------------------------------------------------------")
    print(reason_to_test, "? ", cbct.get_look_str())
    matches = 0
    comment = cbct.comment and 1 or 0

    if next_cbcts_to_preview:
        for num_next_cbct in range(len(next_cbcts_to_preview)):
            nxt_cbct = next_cbcts_to_preview[num_next_cbct]
            time_diff = str(nxt_cbct.get_time() - cbct.get_time())[:-3]
            if cbct.same_date(nxt_cbct) and cbct.same_treatment(nxt_cbct):
                print("\033[01;34m%s CBCT later\033[00;37m: SAME treatment at "
                      "\033[01;34m%s\033[01;35m(+%s)\033[00;37m with comment: "
                      "\"%s\"" % (str(num_next_cbct+1),
                                  nxt_cbct.time, time_diff,
                                  nxt_cbct.comment and "\033[00;33m" +
                                  nxt_cbct.comment +
                                  "\033[00;37m" or
                                  "\033[00;31mNot commented\033[00;37m"))
                matches += 1
                if nxt_cbct.comment:
                    comment = 1
    if not comment:
        print("False[Auto] - No comment available for all imaging performed "
              "this day for this treatment")
        return False, "rule2"

    if not matches:
        print("False [auto] - No second CBCT on same patient in the next "
              "%i CBCTs" % len(next_cbcts_to_preview))
        return False, "rule1"

    if reason_to_test == "bladder":
        try:
            while 1:
                choice = input("\n\n\nPlease enter\n"
                               "- 1 if '%s' is (probably) the reason the CBCT "
                               "was rejected,\n"
                               "- 0 if '%s' is (probably) NOT the reason or if "
                               "the CBCT was (probably) NOT rejected.\n"
                               "- 2 or q to leave.\n" % (reason_to_test,
                                                         reason_to_test))
                if choice == "1":
                    print(True)
                    return True, "manual"
                elif choice == "0":
                    print(False)
                    return False, "manual"
                elif choice == "2" or choice == "q":
                    print("Exiting")
                    raise ValueError("exit")
        except ValueError:
            raise SystemExit
    else:
        raise NotImplemented


in_file = "./ok_cols.csv"
reason = "bladder"
out_file = "./" + reason + "_out.csv"
nb_next_cbcts = 5

colorama_init()

# Fetch columns
with open(in_file, 'r') as in_csv:
    in_reader = csv.DictReader(in_csv)
    columns = in_reader.fieldnames

columns.append(reason)
columns.append("labeling_method")

while 1:
    with open(in_file, 'r') as in_csv:
        in_reader = csv.DictReader(in_csv)
        read_lines = []
        next_cbcts = []
        try:
            in_line1 = next(in_reader)
            cbct1 = Cbct.Cbct(**in_line1)
            for _num in range(nb_next_cbcts):
                next_cbct = next(in_reader)
                next_cbcts.append(Cbct.Cbct(**next_cbct))
            is_reason, labeling_method = is_why(cbct1, reason, next_cbcts)
        except SystemExit:
            exit(0)
        else:
            in_line1[reason] = is_reason
            in_line1["labeling_method"] = labeling_method
            out_lines = []
            # Add line in processed file
            try:
                with open(out_file, "r") as out_csv:
                    out_reader = csv.DictReader(out_csv)
                    for out_line in out_reader:
                        out_lines.append(out_line)
            except FileNotFoundError:
                pass

            with open(out_file, "w+") as out_csv:
                writer = csv.DictWriter(out_csv, fieldnames=columns,
                                        quoting=csv.QUOTE_ALL)
                writer.writeheader()
                if out_lines:
                    writer.writerows(out_lines)
                writer.writerow(in_line1)

    # Remove line in inputs
    with open(in_file, 'r') as in_csv:
        lines = in_csv.readlines()
        lines = [lines[0]] + lines[2:]

    with open(in_file, 'w') as in_csv:
        in_csv.writelines(lines)
