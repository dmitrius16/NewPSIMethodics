""" 
MakeCmdFromCSV this module reads PSI scenariy.csv file and convert it to MTE comands
"""
import sys
import csv
import collections
import MTE_parameters
import names_parameters
from test_point_signal import Signal
import serial

def make_signal_from_csv_source(txt_par_dict, num_pnt):
    '''

    '''
    freq = float(txt_par_dict["F"])
    signal = Signal(freq)
    
    

    pass
    
def create_dict_test_points(csv_file_name):
    """
    Read csv line by line and create dict of points
    """
    res_dict = collections.OrderedDict()
    with(open(csv_file_name, 'r')) as csv_file:
        reader = csv.DictReader(csv_file, fieldnames = names_parameters.get_csv_parameters_names(), delimiter=";")
        for num_pnt, pnt_param in enumerate(reader):
            res_dict[num_pnt + 1] = pnt_param
    return res_dict


def MenuItems():
    print("1 - Choose num point")
    print("2 - Reset MTE")
    print("3 - Exit")

def HandleMenu(pnts_for_generator):
    with open(r".\out.txt", "w") as outfile,\
    serial.Serial('COM5', 19200, timeout=1, parity=serial.PARITY_NONE, rtscts=1) as ser:
        while(True):
            try:
                menu_item = int(input())
                if menu_item == 3:
                    return
                elif menu_item == 1:
                    num_pnt = int(input("Enter point number "))
                    pnt_param = pnts_for_generator.get(num_pnt)
                    if pnt_param:
                        # res = MTE_parameters.generate_commands(pnt_param)
                        res = MTE_parameters.generate_commands_with_harm(pnt_param)
                        ser.write(res.encode(encoding="utf-8"))
                        rd_ser = ser.read(300)
                        outfile.write(res)
                        print(rd_ser)
                    else:
                        print("No such point try again. Point starts from 1!")
                elif menu_item == 2:
                    outfile.write("R\r")
            except ValueError:
                print("Something go wrong! input num menu item.")


def main():
    if len(sys.argv) < 3:
        print("Need more cmd arguments! 1 - name csv, 2 - number of point")
        return     
    # generator_points_dict = collections.OrderedDict()
    set_pnts_for_PSI = create_dict_test_points(sys.argv[1])
    
    MenuItems()
    HandleMenu(set_pnts_for_PSI)

if __name__ == "__main__":
    main()