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
    generate sequence command for MTE generator. 
    !!! In the future place in class!!! 
    '''

    cmds = (("FRQ", vec_par["F"]), 
            ("U1,", vec_par["Ua"]), ("PH1,", '0'),  
            ("U2,", vec_par["Ub"]), ("PH2,", vec_par["Phi_Uab"]),
            ("U3,", vec_par["Uc"]), ("PH3,", vec_par["Phi_Uac"]),
            ("I1,", vec_par["Ia"]), ("W1,", vec_par["Phi_A"]),
            ("I2,", vec_par["Ib"]), ("W2,", vec_par["Phi_B"]),
            ("I3,", vec_par["Ic"]), ("W3,", vec_par["Phi_C"]),
            ("SET\r",""))
    
    str_cmd = '\r'.join((''.join((el[0], el[1].replace(",","."))) for el in cmds))
    return str_cmd
    
if __name__ == "__main__":
    pass



        