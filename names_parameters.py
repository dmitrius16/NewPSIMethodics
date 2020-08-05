'''
All names measurement parameters and generator's parameters
'''
def get_csv_parameters_names():
    parameter_names = ["Npoint", "time", "F", "Ua", "Ub", "Uc", "Phi_Uab", "Phi_Uac",
                    "Uab", "Ubc", "Uca", "U1", "U2", "U0", "Ia", "Ib", "Ic", "Phi_A",
                    "Phi_B", "Phi_C", "I1", "I2", "I0", "Dip_Swell_flag", "Dip_Swell duration",
                    "Dip_Swell period", "Dip_or_Swell(0-dip, 1-Swell)", "K dip/swell", "dip_swell_phase"]
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
    tmp="DumpParam"
    parameter_names.append(tmp)
    return parameter_names

def get_names_harm_vector():
    return ("Ua", "Ub", "Uc", "Ia", "Ib", "Ic")

if __name__ == "__main__":
    pass
