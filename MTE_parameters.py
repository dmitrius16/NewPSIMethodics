"""
MTE_parameters classes for generator parameters
"""

class Voltage:
    def __init__(self ,ampl, phi_grad):
        self.__ampl_val = ampl
        self.__phi_grad = phi_grad
    
    def set_param(self, *args):
        self.__ampl_val = args[0]
        self.__ampl_val = args[1]
    
    def get_param(self):
        return (self.__ampl_val, self.__phi_grad)


class Current:
    def __init__(self, vltg_obj ,ampl, phi_grad):
        self.__vltg_obj = vltg_obj
        self.__ampl_val = ampl
        self.__phi_grad = phi_grad

  


def generate_commands(vec_par):
    '''
    Generate sequence command for MTE generator. 
    !!! In the future place in class!!! 
    '''
    str_cmd = "\r".join((__generate_base_signal_command(vec_par), "SET\r"))
    return str_cmd

def generate_commands_with_harm(vec_par):
    '''
    Generate sequence command for MTE generator with Harmonics
    '''
    str_cmd = []
    str_cmd.append(__generate_base_signal_command(vec_par))
    str_cmd.append(__generate_harm_cmd(vec_par, "OWU", "Uh", "Phi_U_"))
    str_cmd.append(__generate_harm_cmd(vec_par, "OWI", "Ih", "Phi"))
    str_cmd.append("SET\r")
    return "\r".join(str_cmd)
    
    


def __generate_base_signal_command(vec_par):
    '''
    generate_base_signal_commands for MTE generator: set FREQ, U, I, phase U, phase between U and I
    '''
    cmds = (("FRQ", vec_par["F"]), 
            ("U1,", vec_par["Ua"]), ("PH1,", '0'),  
            ("U2,", vec_par["Ub"]), ("PH2,", vec_par["Phi_Uab"]),
            ("U3,", vec_par["Uc"]), ("PH3,", vec_par["Phi_Uac"]),
            ("I1,", vec_par["Ia"]), ("W1,", vec_par["Phi_A"]),
            ("I2,", vec_par["Ib"]), ("W2,", vec_par["Phi_B"]),
            ("I3,", vec_par["Ic"]), ("W3,", vec_par["Phi_C"]))
    #  str_cmd = ';'.join((''.join((el[0], el[1].replace(",", "."))) for el in cmds))
    str_cmd = ';'.join((''.join((el[0], el[1])) for el in cmds))
    return str_cmd

def __generate_harm_cmd(vec_par, cmd_name, prefix_harm, prefix_harm_phi):
    '''
    generate_harm_cmd - create command for generate harmonics
    cmd_name - name cmd for MTE: "OWU" or "OWI"
    prefix_harm - "Uh" or "Ih"
    prefix_harm_phi - "Phi_U_" or "Phi"
    '''
    res_cmd  = []
    for num_harm in range(2, 32):
        name_harm = prefix_harm + str(num_harm) 
        phi_harm = prefix_harm_phi + str(num_harm)
        harm_val = vec_par[name_harm].replace(",", ".")
        phi_val = vec_par[phi_harm]
        if harm_val != "0":
            for num_phase in range(1, 4):  # phase 1 - 3
                res_cmd.append(",".join((cmd_name + str(num_phase), str(num_harm), harm_val, phi_val)))
    return "\r".join(res_cmd)
    
    
if __name__ == "__main__":
    pass



        