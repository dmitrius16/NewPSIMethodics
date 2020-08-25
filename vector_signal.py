'''
test_point_signal - module containes classes for description test point
'''
import names_parameters as names_par
import numpy as np
class VectorValues:
    def __init__(self):
        self.storage = dict()
        self.storage.fromkeys(names_par.get_names_vector(), (0, 0))
    
    def set(self, name, ampl, phase_grad):
        '''
        name: string with name param. Valid names: Ua, Ub, Uc, Ia, Ib, Ic
        ampl: signal amplitude
        phase_grad: signal phase
        '''
        if name in names_par.get_names_vector():
            self.storage[name] = (ampl, phase_grad)
    
    def get(self, name):
        '''
        get - return pair (amplitude, phase) of given name
        '''
        return self.storage[name]
    def get_ampl(self, name):
        '''
        get_ampl - return rms value signal
        '''
        return self.storage[name][0]
    def get_phase(self, name):
        '''
        get_phase - return phase signal
        '''
        return self.storage[name][1]
    

class Signal:
    '''
    Signal represents point in generator.
    '''
    def __init__(self, freq):
        self.frequency = freq
        self.set_harmonics = dict()
        self.set_interharmonics = dict()
        self.meas_result = dict.fromkeys(names_par.names_measured_params, 0)
    def add(self, vector_values):
        '''
        add main frequency vector values
        vector_values - type VectorValues from test_point_signal.py
        '''
        self.set_harmonics[0] = vector_values

    def add_harm(self, num_harm, vector_values):
        '''
        add harmonics to signal
        vvector_values - type VectorValues from test_point_signal.py
        '''
        self.set_harmonics[num_harm] = vector_values
    def add_interharm(self, num_interharm, vector_values):
        '''
        add interharmonics to signal
        vvector_values - type VectorValues from test_point_signal.py
        '''
        self.set_interharmonics[num_interharm] = vector_values

    def add_MTE_counter_harm_results(self, *args):
        '''
        Create signal from mte counter results. MTE add every phases separately
        MTE has only harmonics! no interharmonics
        args - set ziped values for each phase args[0] -> Ua, args[1] -> Ub... , args[5] ->Ic, where Ua ->((val, phase),(val_1, phase_1)....)
        '''
        Ua, Ub, Uc, Ia, Ib, Ic = args
        names = names_par.get_names_vector()
        for num_harm in range(0, 32):
            harm_val = VectorValues()
            for ind in range(len(args)):
                harm_val.set(names[ind], args[ind][0], args[ind][1])  # args[ind][0] - amplitude, args[ind][1] - phase


    def __calc_rms_value(self, name="vltg"):
        '''
        __calc_rms_value - calculate rms value voltage or current depending on the name  U = sqrt(U2^2 + U3^2 + ...) or I = sqrt ...

        valid value for name 'vltg' or 'current'
        '''
        res = []
        phase_names = names_par.get_phase_voltage_names() if name == 'vltg' else names_par.get_phase_current_names() 
        for name in phase_names:
            value = 0
            for vec_val in self.set_harmonics.values():
                value += vec_val.get_ampl(name) ** 2
            res.append(value ** 0.5)
        self.meas_result.update({nm_phase: value for nm_phase, value in zip(phase_names, res)})


    def __calc_phase_voltage(self):
        '''
        calc_phase_voltage - calc rms voltage U = sqrt(U2^2 + U3^2 + ...)
        '''
        self.__calc_rms_value(name="vltg") 


    def __calc_voltage_angles(self):
        '''
        calc angles between phases.
        '''
        nm_angles = names_par.get_measured_vltg_angle_names()
        phiB = self.set_harmonics[0].get_phase("Ub")
        phiC = self.set_harmonics[0].get_phase("Uc")
        sign = 0
        if phiB - phiC > 0:
            sign = 1
        elif phiB - phiC < 0:
            sign = -1

        angle_Uab = 0 - phiB
        angle_Ubc = phiB - phiC if np.abs(phiB - phiC) < 180 else phiB - phiC - 360 * sign
        angle_Uca = phiC

        self.meas_result.update({angle: val for angle, val in zip(nm_angles, (angle_Uab, angle_Ubc, angle_Uca))})

    
    def __calc_phase_current(self):
        '''
        calc_phase_current - calc rms current I = sqrt(I2^2 + I3^2 + ...)
        '''
        self.__calc_rms_value(name="current")
    
    def __calc_cosPhi(self):
        '''
        calc_cos_phi - calc cos phi *(between U and I)
        '''
        nm_angles = names_par.get_measured_current_angle_names()
        phase_angles = [self.set_harmonics[0].get_phase(name) for name in names_par.get_phase_current_names()]  # phase_angles - phiA, phiB, phiC        
        self.meas_result.update({angle : val * 180/np.pi for angle, val in zip(nm_angles, phase_angles)})

    def __convert_to_complex_num(self, vec_val):
        '''
        convert_to_complex_num - convers VectorValue to complex number representation
        '''
        names = names_par.get_phase_voltage_names()
        res = np.zeros((3,1), dtype=complex)  # create vector zeros dimention 3x1
        for ind, nm in enumerate(names):
            ampl, phase = vec_val.get(nm)
            res[ind] = np.complex(ampl * np.cos(np.deg2rad(phase), ampl * np.sin(np.deg2rad(phase))))
        return res
        

    def __calc_symmetrical_sequences_vltg(self):
        '''
        calc_symmetrical_sequences_vltg - calculates U1, U2, U0
        '''
        alpha = np.complex(np.cos(2 * np.pi/3), np.sin(2 * np.pi/3))
        tranform_matrix = np.array([[1, alpha, alpha ** 2], [1, alpha ** 2, alpha], [1, 1, 1]])        
        complex_val = self.__convert_to_complex_num(self.set_harmonics[0])
        result = tranform_matrix.dot(complex_val)



    def calc_linear_voltage(self, name="Uab"):
        '''
        calc_linear_voltage calcs voltage between two phases. ! Now calc only on main frequency
        name - string name between two phases. Valid names Uab, Ubc, Uca
        '''
        if name in names_par.get_linear_vltg_names():
            pass
            
        return 0

    def calc_measured_param(self):
        '''
        calc all measurement parameters from signal
        '''
        self.meas_result["f"] = self.frequency
        self.__calc_phase_voltage()
        self.__calc_voltage_angles()
        self.__calc_phase_current()
        self.__calc_cosPhi()
        self.__calc_symmetrical_sequences_vltg()

    


def make_signal_from_csv_source(txt_par_dict, num_pnt):
    '''

    '''
    par = txt_par_dict[num_pnt]
    freq = float(par["F"])
    signal = Signal(freq)
    main_freq_signal = VectorValues()

    nominals = (float(par["Ua"]), float(par["Ub"]), float(par["Uc"]), float(par["Ia"]), float(par["Ib"]), float(par["Ic"]))

    main_freq_signal.set("Ua", nominals[0], 0)
    main_freq_signal.set("Ub", nominals[1], float(par["Phi_Uab"]))   # ??? phase correct ???
    main_freq_signal.set("Uc", nominals[2], float(par["Phi_Uac"]))
    main_freq_signal.set("Ia", nominals[3], float(par["Phi_A"]))
    main_freq_signal.set("Ib", nominals[4], float(par["Phi_B"]))
    main_freq_signal.set("Ic", nominals[5], float(par["Phi_C"]))
    signal.add(main_freq_signal)

     

    # put harmonics into signal    
    for harm in names_par.get_voltage_harmonic_names():
        uh_name, ih_name, phi_name_uh, phi_name_ih = harm
        harm = VectorValues()
        percent_uh, phi_uh = float(par[uh_name]), float(par[phi_name_uh])  # 3 phases have identical values
        for ind, name in enumerate(names_par.get_phase_voltage_names()):
            harm.set(name, nominals[ind] * percent_uh / 100, phi_uh)

        percent_ih, phi_ih = float(par[ih_name]), float(par[phi_name_ih])
        for ind, name in enumerate(names_par.get_phase_current_names()):
            harm.set(name, nominals[3 + ind] * percent_ih / 100, phi_ih)
            
        signal.add_harm(names_par.get_num_harm(uh_name), harm)
    
    # put interharmonics into signal. Notice!!! current csv scenary don't have phase shift on interharmonics!!!
    for inter_harm in names_par.get_voltage_interharmonic_names():
        ui_name, ii_name = inter_harm
        harm = VectorValues()
        percent_ui = float(par[ui_name])
        for ind, name in enumerate(names_par.get_phase_voltage_names()):
            harm.set(name, nominals[ind] * percent_ui / 100, 0)
        percent_ii = float(par[ii_name])
        for ind, name in enumerate(names_par.get_phase_current_names()):
            harm.set(name, nominals[3 + ind] * percent_ii / 100, 0)
        signal.add_interharm(names_par.get_num_harm(ui_name), harm)
    return signal
 


if __name__ == "__main__":
    pass