"""
MTE_parameters classes for generator parameters
"""

# Диапазоны СЧЕТЧИКА
U_CNT_max_ranges_dict = {   1   : 0.4, 
                            2   : 5.0,
                            3   : 65.0,
                            4   : 130.0,
                            5   : 260.0,
                            6   : 520.0,    }

I_CNT_max_ranges_dict = {   1   : 0.004, 
                            2   : 0.012,
                            3   : 0.04,
                            4   : 0.12,
                            5   : 0.4,
                            6   : 1.2,
                            7   : 4.0,
                            8   : 12.0    }

# Диапазоны ГЕНЕРАТОРА
U_GEN_max_ranges_dict = {   2   : 75,
                            3   : 150     }
                            
U_GEN_TRUE_dict = {         2   : 3,
                            3   : 2     }                            
                            

I_GEN_max_ranges_dict = {   1   : 0.012,
                            2   : 0.12,
                            3   : 1.2,
                            4   : 12.0    }   
                            
I_GEN_TRUE_dict = {         1   : 4,
                            2   : 3,
                            3   : 2,
                            4   : 1    }                            


def generate_commands_base_params(vec_par,main_freq):
    '''
    generate_base_signal_commands for MTE generator: set FREQ, U, I, phase U, phase between U and I
    '''
    #cmds = vec_par.get("Ua")

    ########################################################################
    ########################################################################
    ########################################################################
    # найти максимальный элемент U и I -> выбрать нужный верхний диапазон -> установить команду на счетчик МТЕ
    Ua = vec_par.get_ampl("Ua")
    Ub = vec_par.get_ampl("Ub")
    Uc = vec_par.get_ampl("Uc")

    Ia = vec_par.get_ampl("Ia")
    Ib = vec_par.get_ampl("Ib")
    Ic = vec_par.get_ampl("Ic")

    global range_Ua_CNT
    global range_Ub_CNT
    global range_Uc_CNT

    global range_Ia_CNT
    global range_Ib_CNT
    global range_Ic_CNT

    range_Ua_CNT,range_Ub_CNT,range_Uc_CNT = find_ranges(Ua,Ub,Uc,U_CNT_max_ranges_dict)
    range_Ia_CNT,range_Ib_CNT,range_Ic_CNT = find_ranges(Ia,Ib,Ic,I_CNT_max_ranges_dict)

    global range_Ua_GEN
    global range_Ub_GEN
    global range_Uc_GEN

    global range_Ia_GEN
    global range_Ib_GEN
    global range_Ic_GEN

    list_ranges_U = []
    list_ranges_I = []

    list_ranges_U = find_ranges_GEN(Ua,Ub,Uc,U_GEN_max_ranges_dict,U_GEN_TRUE_dict)
    list_ranges_I = find_ranges_GEN(Ia,Ib,Ic,I_GEN_max_ranges_dict,I_GEN_TRUE_dict)

    range_Ua_GEN = list_ranges_U[0]
    range_Ub_GEN = list_ranges_U[1]
    range_Uc_GEN = list_ranges_U[2]

    range_Ia_GEN = list_ranges_I[0]
    range_Ib_GEN = list_ranges_I[1]
    range_Ic_GEN = list_ranges_I[2]
    '''
    range_Ua_GEN,range_Ub_GEN,range_Uc_GEN = find_ranges_GEN(Ua,Ub,Uc,U_GEN_max_ranges_dict,U_GEN_TRUE_dict)
    range_Ia_GEN,range_Ib_GEN,range_Ic_GEN = find_ranges_GEN(Ia,Ib,Ic,I_GEN_max_ranges_dict,I_GEN_TRUE_dict)
    '''

    ########################################################################
    ########################################################################
    ########################################################################

    str_cmd = "FRQ,"+str(main_freq)+";"

    ph_U_a = vec_par.get_phase("Ua")
    ph_U_b = vec_par.get_phase("Ub")
    ph_U_c = vec_par.get_phase("Uc")

    ph_I_a = vec_par.get_phase("Ia") - ph_U_a# + 0
    ph_I_b = vec_par.get_phase("Ib") - ph_U_b# -120
    ph_I_c = vec_par.get_phase("Ic") - ph_U_c


    str_cmd +=  "U1,"+ str(vec_par.get_ampl("Ua"))+";"+ "U2,"+ str(vec_par.get_ampl("Ub"))+";"+ "U3,"+ str(vec_par.get_ampl("Uc"))+";"+\
               "PH1,"+str(ph_U_a)+";"+"PH2,"+str(ph_U_b)+";"+"PH3,"+str(ph_U_c)+";"

    str_cmd +=  "I1,"+ str(vec_par.get_ampl("Ia"))+";"+ "I2,"+ str(vec_par.get_ampl("Ib"))+";"+ "I3,"+ str(vec_par.get_ampl("Ic"))+";"+\
                "W1,"+str(ph_I_a)+";"+ "W2,"+str(ph_I_b)+";"+ "W3,"+str(ph_I_c)          #+";"

    return str_cmd


    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
def generate_harm_cmd(h_signal):

    vol_harm_zero = True
    cur_harm_zero = True
    t_U_ampl = 0.0
    t_I_ampl = 0.0

    keys_vect_dict = ["Ua", "Ub", "Uc", "Ia", "Ib", "Ic"]

    cmd_harm_prefix = ["OWU","OWI"]
    cmd_phase_prefix = ["1","2","3"]

    cmd_voltage = ""
    cmd_current = ""

    main_harm_ampl = []
    main_harm = h_signal.get_main_freq_vector()

    for idx_phase in keys_vect_dict:
        main_harm_ampl.append(main_harm.get_ampl(idx_phase))

    
    for idx_harm_num in range(2, 32):   # цикл по всем гармоникам

        cur_harm_signal = h_signal.get_vector_harm(idx_harm_num)    # текущий объект Vector_values с параметрами idx_harm_num гармоники

        for idx_phase in range(3):              # цикл по фазам

            t_U_ampl = round(100.0*cur_harm_signal.get(keys_vect_dict[idx_phase])[0] / main_harm_ampl[idx_phase],3)
            t_I_ampl = round(100.0*cur_harm_signal.get(keys_vect_dict[idx_phase+3])[0] / main_harm_ampl[idx_phase+3],3)

            if t_U_ampl != 0.0: 
                vol_harm_zero = False
            if t_I_ampl != 0.0: 
                cur_harm_zero = False

            cmd_voltage += cmd_harm_prefix[0] + cmd_phase_prefix[idx_phase] + "," \
                                                        + str(idx_harm_num) + "," \
                                                        + str(t_U_ampl) + "," \
                                                        + str(cur_harm_signal.get(keys_vect_dict[idx_phase])[1]) + ";"

            cmd_current += cmd_harm_prefix[1] + cmd_phase_prefix[idx_phase] + "," \
                                                        + str(idx_harm_num) + "," \
                                                        + str(t_I_ampl) + "," \
                                                        + str(cur_harm_signal.get(keys_vect_dict[idx_phase+3])[1]) + ";"


    if vol_harm_zero == True: 
        cmd_voltage = ""
    if cur_harm_zero == True: 
        cmd_current = ""


    return cmd_voltage, cmd_current


def get_ranges_CNT():
    #range_Ua_CNT,range_Ub_CNT,range_Uc_CNT,range_Ia_CNT,range_Ib_CNT,range_Ic_CNT = MTE_parameters.get_ranges_CNT()
    ranges_CNT = "U"+str(range_Ua_CNT)+","+str(range_Ub_CNT)+","+str(range_Uc_CNT)+";" 
    ranges_CNT = ranges_CNT + "I"+str(range_Ia_CNT)+","+str(range_Ib_CNT)+","+str(range_Ic_CNT)+"\r"  

    return ranges_CNT


def get_ranges_GEN():
    #range_Ua_GEN,range_Ub_GEN,range_Uc_GEN,range_Ia_GEN,range_Ib_GEN,range_Ic_GEN = MTE_parameters.get_ranges_GEN()
    ranges_GEN = "BU1,"+str(range_Ua_GEN)+";BU2,"+str(range_Ub_GEN)+";BU3,"+str(range_Uc_GEN)+";" 
    ranges_GEN = ranges_GEN + "BI1,"+str(range_Ia_GEN)+";BI2,"+str(range_Ib_GEN)+";BI3,"+str(range_Ic_GEN)+"\r" 

    return ranges_GEN

def find_ranges(val_a,val_b,val_c,max_ranges_dict):

    for key_dict in max_ranges_dict:
        #print("val_a "+str(val_a) + " "+str(key_dict) + " ")
        if val_a < max_ranges_dict[key_dict]:
            range_val_a = key_dict
            #print("val_a " + str(val_a)+" key_dict find max range: " + str(range_val_a)+"  max_ranges_dict[key_dict]  " + str(max_ranges_dict[key_dict]))
            break

    for key_dict in max_ranges_dict:
        if val_b < max_ranges_dict[key_dict]:
            range_val_b = key_dict
            #print("val_b " + str(val_b)+" key_dict find max range: " + str(range_val_b)+"  max_ranges_dict[key_dict]  " + str(max_ranges_dict[key_dict]))
            break

    for key_dict in max_ranges_dict:
        if val_c < max_ranges_dict[key_dict]:
            range_val_c = key_dict
            #print("val_c " + str(val_c)+" key_dict find max range: " + str(range_val_c)+"  max_ranges_dict[key_dict]  " + str(max_ranges_dict[key_dict]))
            break

    return range_val_a, range_val_b, range_val_c
    
def find_ranges_GEN(val_a,val_b,val_c,max_ranges_dict,GEN_TRUE_dict):

    list_vals = [val_a,val_b,val_c]
    list_ranges = []
    for key_list_vals in list_vals:
        for key_dict in max_ranges_dict:
            if key_list_vals < max_ranges_dict[key_dict]:
                list_ranges.append(GEN_TRUE_dict[key_dict])
                #print("val " + str(key_list_vals)+" key_dict find max range: "\
                #     + str(GEN_TRUE_dict[key_dict])+"  max_ranges_dict[key_dict]  " + str(max_ranges_dict[key_dict]))
                break

    '''
    for key_dict in max_ranges_dict:
        #print("val_a "+str(val_a) + " "+str(key_dict) + " ")
        if val_a < max_ranges_dict[key_dict]:
            range_val_a = GEN_TRUE_dict[key_dict]
            print("val_a " + str(val_a)+" key_dict find max range: " + str(range_val_a)+"  max_ranges_dict[key_dict]  " + str(max_ranges_dict[key_dict]))
            break

    for key_dict in max_ranges_dict:
        if val_b < max_ranges_dict[key_dict]:
            range_val_b = GEN_TRUE_dict[key_dict]
            print("val_b " + str(val_b)+" key_dict find max range: " + str(range_val_b)+"  max_ranges_dict[key_dict]  " + str(max_ranges_dict[key_dict]))
            break

    for key_dict in max_ranges_dict:
        if val_c < max_ranges_dict[key_dict]:
            range_val_c = GEN_TRUE_dict[key_dict]
            print("val_c " + str(val_c)+" key_dict find max range: " + str(range_val_c)+"  max_ranges_dict[key_dict]  " + str(max_ranges_dict[key_dict]))
            break
    '''

    return list_ranges


 

if __name__ == "__main__":
    pass



        