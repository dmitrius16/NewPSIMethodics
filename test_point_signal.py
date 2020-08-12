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
        self.set_interharmonics[num_interharm]

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
                harm_val.set(names[ind], args[ind][0], args[ind][1])  # args[ind][0] - val, args[ind][1] - phase
            
    def calc_phase_voltage(self, name="Ua"):
        '''
        calc_phase_voltage - calc rms voltage U = sqrt(U2^2 + U2^2 + ...)
        '''
        if name in names_par.get_phase_voltage_names():
            voltage = 0
            for vec_val in self.set_harmonics.values():
                voltage += vec_val.get_ampl(name) ** 2
        return voltage ** 0.5
    

    def calc_linear_voltage(self, name="Uab"):
        '''
        calc_linear_voltage calcs voltage between two phases. ! Now calc only on main frequency
        name - string name between two phases. Valid names Uab, Ubc, Uca
        '''
        if name in names_par.get_linear_vltg_names():
            pass
            
        return 0

def make_signal_from_csv_source(txt_par_dict, num_pnt):
    '''

    '''
    par = txt_par_dict[num_pnt]
    freq = float(par["F"])
    signal = Signal(freq)
    main_freq_signal = VectorValues()
    main_freq_signal.set("Ua", float(par["Ua"]), 0)
    main_freq_signal.set("Ub", float(par["Ub"]), float(par["Phi_Uab"]))   # ??? phase correct ???
    main_freq_signal.set("Uc", float(par["Uc"]), float(par["Phi_Uac"]))
    main_freq_signal.set("Ia", float(par["Ia"]), float(par["Phi_A"]))
    main_freq_signal.set("Ib", float(par["Ib"]), float(par["Phi_B"]))
    main_freq_signal.set("Ic", float(par["Ic"]), float(par["Phi_C"]))
    signal.add(main_freq_signal)

    # put harmonics into signal    
    for harm in names_par.get_voltage_harmonic_names():
        uh_name, ih_name, phi_name_uh, phi_name_ih = harm
        if par[uh_name] != '0' or par[ih_name] != '0':  #  check if Uh<num> != 0 or Ih != 0 for add harmonic to signal
            harm = VectorValues()
            val_uh, val_phi_uh = float(par[uh_name]), float(par[phi_name_uh])  # 3 phases have identical values
            for name in names_par.get_phase_voltage_names():
                harm.set(name, val_uh, val_phi_uh)

            val_ih, val_phi_ih = float(par[ih_name]), float(par[phi_name_ih])
            for name in names_par.get_phase_current_names():
                harm.set(name, val_ih, val_phi_ih)
            
            signal.add_harm(names_par.get_num_harm(uh_name) ,harm)
    
    # put interharmonics into signal. Notice!!! current csv scenary don't have phase shift on interharmonics!!!
    for inter_harm in names_par.get_voltage_interharmonic_names():
        ui_name, ii_name = inter_harm
        if par[ui_name] != '0' or par[ii_name] != '0':
            harm = VectorValues()
            val_ui = float(par[ui_name])
            for name in names_par.get_phase_voltage_names():
                harm.set(name, val_ui, 0)
            val_ii = float(par[ii_name])
            for name in names_par.get_phase_current_names():
                harm.set(name, val_ii, 0)
            signal.add_interharm(names_par.get_num_harm(ui_name), harm)

    return signal
 


if __name__ == "__main__":
    pass