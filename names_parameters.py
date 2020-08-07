'''
All names measurement parameters and generator's parameters
'''
def get_csv_parameters_names():
    parameter_names = ["Npoint", "time", "F", "Ua", "Ub", "Uc", "Phi_Uab", "Phi_Uac",
                    "Uab", "Ubc", "Uca", "U1", "U2", "U0", "Ia", "Ib", "Ic", "Phi_A",
                    "Phi_B", "Phi_C", "I1", "I2", "I0", "Dip_Swell_flag", "Dip_Swell duration",
                    "Dip_Swell period", "Dip_or_Swell(0-dip, 1-Swell)", "K dip/swell", "Count dip/swells" ,"dip_swell_phase"]
    u_harm = "Uh"
    parameter_names.extend([u_harm + str(num) for num in range(2, 51)])
    i_harm = "Ih"
    parameter_names.extend([i_harm + str(num) for num in range(2, 51)])
    phi_u_harm = "Phi_U_"
    parameter_names.extend([phi_u_harm + str(num) for num in range(2, 51)])
    phi_i_harm = "Phi"
    parameter_names.extend([phi_i_harm + str(num) for num in range(2,51)])
    u_interharm = "Ui"
    parameter_names.extend([u_interharm + str(num) for num in range(1, 50)])
    i_interharm = "Ii"
    parameter_names.extend([i_interharm + str(num) for num in range(1, 50)])
    tmp = "DumpParam"
    parameter_names.append(tmp)
    return parameter_names

def get_harmonic_names_prefixes():
    return ("Uh", "Ih", "Phi_U_", "Phi")

def get_interharmonic_names_prefixes():
    return ("Ui", "Ii")

def get_voltage_harmonic_names():
    '''
    return names harmonics as (Uh2, Ih2, Phi_U_2,  Phi_2), (Uh3, Ih3, Phi_U_3,  Phi_3), ...
    '''
    u_harm = get_harmonic_names_prefixes()
    res = []
    for num in map(lambda x: str(x), range(2, 51)):
        sub_res = []
        for ind in range(0, len(u_harm)):
            sub_res.append(u_harm[ind] + num)
        res.append(sub_res)
    return tuple(res)

def get_num_harm(name):
    '''
    get num harmonic or interharmonic for given name!
    '''
    pattern = get_harmonic_names_prefixes() + get_interharmonic_names_prefixes()
    for pat_name in pattern:
        ind = name.find(pat_name)
        if ind != -1:
            return int(name[len(pat_name):])
            
    return 0

    
def get_voltage_interharmonic_names():
    '''
    return names interharmonic as (Ui1, Ii1),(Ui2, Ii2),... (Ui3, Ii3)
    '''
    u_iharm = "Ui", "Ii"
    res = []
    for num in map(lambda x: str(x), range(1, 50)):
        sub_res = []
        for ind in range(0, len(u_iharm)):
            sub_res.append(u_iharm[ind] + num)
        res.append(sub_res)
    return tuple(res)


def get_names_vector():
    return ("Ua", "Ub", "Uc", "Ia", "Ib", "Ic")

def get_phase_voltage_names():
    return ("Ua", "Ub", "Uc")

def get_phase_current_names():
    return ("Ia", "Ib", "Ic")

def get_linear_vltg_names():
    return ("Uab", "Ubc", "Uca")


def get_signal_names():
    pass

if __name__ == "__main__":
    pass
