""" 
MakeCmdFromCSV this module reads PSI scenariy.csv file and convert it to MTE comands
"""

import serial

import MTE_Counter
import MTE_Generator

#import vector_signal
import collections
import csv
import names_parameters
import measurement

#-------------------------------

import make_psi

import svgrequest 
import time

#binom_data = svgrequest.RequestBinom()



def init_main():
    ##################################
    # Создание большого списка сигналов. Один экземпляр класса сигнал для одной точки ПСИ
    set_pnts_for_PSI = create_dict_test_points("PSI_Binom3_5_57.csv")
    ##################################

    ##################################
    #1.1 - inits serial ports
    ser_Counter   = serial.Serial("COM2", 19200, timeout=0.5, parity=serial.PARITY_NONE, rtscts=0)
    ser_Generator = serial.Serial("COM3", 19200, timeout=0.5, parity=serial.PARITY_NONE, rtscts=0)

    #1.2 - Create objects MTE device
    #1.2.1 - MTE Counter
    write_str = "MODE1;DB1;SU0;SP1,1;SP2,1;SP22,1;SP9,1;SP13,1;T0;MAN;YI0;SU0\r"   # mode of send/get command by COM4 'Counter' port # режим токовых входов 12 А (по умолчанию стоит 120 А)
    counter_MTE = MTE_Counter.C_MTE_Counter(ser_Counter, 0.5, write_str, 0, 0)
    #1.2.2 - MTE Generator
    write_str = "MODE1;T1\r"   # mode of send/get command by COM1 'Generator' port
    generator_MTE = MTE_Generator.C_MTE_Generator(ser_Generator, 0.5, write_str, 0, 0)
    ##################################


    
    ##################################
    make_psi.init()
    ##################################
    
    return set_pnts_for_PSI, ser_Counter, ser_Generator, counter_MTE, generator_MTE


def main():

    st_pnt = 14
    end_pnt = 15

    cur_pnt = st_pnt
    try:

        # Единая функция Init
        set_pnts_for_PSI, ser_Counter, ser_Generator, counter_MTE, generator_MTE = init_main()

        while cur_pnt <= end_pnt:
            
            #1.3 - Set PSI point on Generator
            sig = measurement.make_signal_from_csv_source(set_pnts_for_PSI, cur_pnt)    # 
            set_PSI_pnt_flag_Generator = generator_MTE.set_PSI_point(sig)

            if set_PSI_pnt_flag_Generator == True:      # проверка установки точки ПСИ по генератору пройдена  
                counter_MTE.ser_port.timeout = 1
                counter_MTE.set_ranges_for_CNT()    # Установка диапазонов для Счетчика

                # 1.3.2 - Check by Counter/ - soon will be added (11:41 31.08.2020)

                #4 Read data from MTE Counter
                counter_MTE.start_auto_measure()    # Включить режим автовыдачи результатов               
                readTime = 6
                MTE_measured_Time = 1
                counter_MTE.readByTimeT(readTime,MTE_measured_Time)
                counter_MTE.stop_auto_measure()#9 - выключить режим автовыдачи результатов после окончания интеравала записи Т

                # получить усредненные данные 'короткой посылки' от счетчика МТЕ
                short_MTE_data_block = counter_MTE.get_mean_values()
                ####for elem in short_MTE_data_block:
                ####    print("elem "+str(elem))
                measurement.measurement_storage.set_mte_measured_signal(cur_pnt,short_MTE_data_block)
        
            for _ in range(2):
                make_psi.binom_data.read_data(cur_pnt)
                # time.sleep(5)
            
            cur_pnt+=1

        print("Ask finished")
    except Exception as ex:
        print("Exception occur:", ex)
    finally:

        ser_Counter.close()
        ser_Generator.close()

        make_psi.deinit()


    #TopMenuItems()
    #HandleMenu(set_pnts_for_PSI)



def TopMenuItems():
    print("\r\nTop menu:")
    print("1 - 'MTE counter':    Configure params")
    print("2 - 'MTE counter':    Measured menu")
    print("3 - 'MTE counter':    Send Direct command")
    print("4 - 'MTE counter':    Reset Counter MTE")
    print("5 - 'MTE generator':  Measured menu")
    print("6 - 'MTE generator':  Choose PSI point (1 - 156)")
    print("7 - 'MTE generator':  Send Direct command")
    print("8 - 'MTE generator':  Reset Generator MTE")
    print("9 - shutdown program")
    print("10 - shutdown program and RESET devices")

def HandleMenu(set_pnts_for_PSI):
    """
    Main menu: control 'Generator MTE':PPS 400.3 and 'Counter MTE':PRS 440.3
    """

    ##with serial.Serial("COM4", 19200, timeout=0.3, parity=serial.PARITY_NONE, rtscts=0) as ser_Counter:        #Init COM-port to 'Counter MTE' (PRS 400.3)
    with serial.Serial("COM2", 19200, timeout=0.3, parity=serial.PARITY_NONE, rtscts=0) as ser_Counter:        #Init COM-port to 'Counter MTE' (PRS 400.3)
                      
        write_str = "MODE1;DB1\r"   # mode of send/get command by COM4 'Counter' port # режим токовых входов 12 А (по умолчанию стоит 120 А)
        #def init(self ,ser, ser_timeout, start_cmd,b_print_cmd,b_print_answ):
        counter_MTE = MTE_Counter.C_MTE_Counter(ser_Counter, 0.3, write_str, 1, 1)
        ######################################################
        write_str = "SU0;SP1,1;SP2,1;T0.25\r"   # установка элементов списка автовыдачи (I,U) и времени измерения (0.25 сек)
        counter_MTE.send_to_MTE(write_str)
        ######################################################
        # предустановка диавапазонов для точки 1
        #write_str = "MAN;YI0;I8,8,8;U3,3,3\r"   # mode of send/get command by COM4 'Counter' port # режим токовых входов 12 А (по умолчанию стоит 120 А)
        write_str = "MAN;YI0\r"        
        counter_MTE.send_to_MTE(write_str)
        ######################################################

        with serial.Serial('COM3', 19200, timeout=0.3, parity=serial.PARITY_NONE, rtscts=0) as ser_Generator:
        #with serial.Serial('COM1', 19200, timeout=0.3, parity=serial.PARITY_NONE, rtscts=0) as ser_Generator:
        #with serial.Serial('COM5', 19200, timeout=0.3, parity=serial.PARITY_NONE, rtscts=0) as ser_Generator:
            
            write_str = "MODE1;T1\r"   # mode of send/get command by COM1 'Generator' port
            #def init(self ,ser, ser_timeout, start_cmd,b_print_cmd,b_print_answ):
            generator_MTE = MTE_Generator.C_MTE_Generator(ser_Generator, 0.3, write_str, 1, 1)
            
            while(True):
                try:
                    top_menu_item = int(input())
                    #top_menu_item = 6
                    if top_menu_item == 9:
                        print("Pressed: 9 - shutdown programm")  
                        write_str = "SU0\r"     # закончить автоматическую передачу данных
                        counter_MTE.send_to_MTE(write_str)  #9 exit from this programm
                        return

                    elif top_menu_item == 10:
                        print("Pressed: 10 - shutdown program and RESET devices")  #10 exit with Reset devices
                        write_str = "R\r"
                        counter_MTE.send_to_MTE(write_str)
                        generator_MTE.send_to_MTE(write_str)
                        return

                    elif top_menu_item == 1:
                        print("\r\nChoose 'MTE counter' configure params:")     #1 set/get params from/to 'Counter MTE'
                        counter_MTE.SetMenuHandler()
                        
                    elif top_menu_item == 2:                              
                        print("\r\nChoose 'MTE counter' measured menu:")
                        counter_MTE.GetMenuHandler()
                            
                    elif top_menu_item == 3:
                        print("\r\n Input Direct command to 'MTE counter':")
                        directCommandToMTE = str(input())
                        print("Command to send: ", directCommandToMTE)
                        counter_MTE.send_to_MTE(directCommandToMTE + "\r")

                    elif top_menu_item == 4:
                        print("Reset Counter MTE")
                        counter_MTE.send_to_MTE("R\r")
                        counter_MTE.send_to_MTE("MODE1;DB1\r")

                    elif top_menu_item == 5:
                        print("\r\nChoose 'MTE generator' measured menu:")
                        
                        generator_MTE.GetMenuHandler()

                    elif top_menu_item == 6:
                        print("\r\n Enter PSI point (1 - 156) number: ")
                        num_pnt = int(input())
                        #num_pnt = 134
                        
                        if num_pnt > 0 and num_pnt < 157:

                            sig = measurement.make_signal_from_csv_source(set_pnts_for_PSI, num_pnt)    # 
                            set_PSI_pnt_flag_Generator = generator_MTE.set_PSI_point(sig)

                            if set_PSI_pnt_flag_Generator == True:      # проверка установки точки ПСИ по генератору пройдена  

                                counter_MTE.ser_port.timeout = 3
                                counter_MTE.set_ranges_for_CNT()    # Установка диапазонов для Счетчика

                                counter_MTE.ser_port.timeout = 0.5

                                ### Проверка по счетчику
                                '''
                                set_PSI_pnt_flag_Counter = counter_MTE.check_PSI_pnt(sig)

                                if set_PSI_pnt_flag_Generator == True:      # проверка установки точки ПСИ по генератору пройдена 
                                    counter_MTE.start_auto_measure()
                                    
                                    readTime = 3
                                    MTE_measured_Time = 0.25
                                    counter_MTE.readByTimeT(readTime,MTE_measured_Time)
                                    
                                    #9 - выключить режим автовыдачи результатов после окончания интеравала записи Т
                                    counter_MTE.stop_auto_measure()
                                '''
                                #counter_MTE.get_all_spectrum()

                            #10 передать в класс Signal усредненные значения измерений счетчика МТЕ
                            #def get_mean_values(self):    
                            #return self.list_I_mean, self.list_U_mean,self.list_phi_UI_mean, self.list_phi_UU_mean, self.freq_mean


                    elif top_menu_item == 7:
                        print("\r\n Input Direct command to 'MTE generator':")
                        directCommandToMTE = str(input())
                        print("Command to send: ", directCommandToMTE)
                        write_directCommandToMTE = directCommandToMTE + "\r"

                        generator_MTE.send_to_MTE(write_directCommandToMTE)

                    elif top_menu_item == 8:
                        print("Reset Generator MTE")
                        write_str = "R\r"
                        generator_MTE.send_to_MTE(write_str)
                        
                    TopMenuItems() 

                except ValueError:
                    print("\r\nSomething go wrong! main menu error exeption.")


def create_dict_test_points(csv_file_name):
    """
    Read csv line by line and create dict of points
    """
    res_dict = collections.OrderedDict()
    with(open(csv_file_name, 'r')) as csv_file:
        reader = csv.DictReader(csv_file, fieldnames = names_parameters.get_csv_parameters_names(), delimiter=";")
        for num_pnt, pnt_param in enumerate(reader):
            pnt_param = {k:v.replace(",", ".") if type(v) == str else v for k, v in pnt_param.items()}
            res_dict[num_pnt + 1] = pnt_param
    return res_dict


if __name__ == "__main__":
    main()