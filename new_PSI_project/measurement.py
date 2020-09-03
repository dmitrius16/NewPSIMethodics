import vector_signal as vs
import names_parameters as names_par
import collections
import csv

def create_dict_test_points(csv_file_name):
    """
    Read csv line by line and create dict of points
    """
    csv_dict = collections.OrderedDict()
    with(open(csv_file_name, 'r')) as csv_file:
        reader = csv.DictReader(csv_file, fieldnames = names_par.get_csv_parameters_names(), delimiter=";")
        for num_pnt, pnt_param in enumerate(reader):
            pnt_param = {k:v.replace(",", ".") if type(v) == str else v for k, v in pnt_param.items()}
            csv_dict[num_pnt + 1] = pnt_param

    # here make measurement signal
    for num_pnt in range(1, 156):
        make_signal_from_csv_source(csv_dict, num_pnt)
   
class MeasurementStorage(): # make as singleton!
    def __init__(self):
        self.psi_pnts = []
        for i in range(1, 161):
            etalon = vs.Signal()
            mte = vs.Signal()
            self.psi_pnts.append(PSIPointMesurement(i, etalon, mte))

    def get_etalon_signal(self, num_pnt):
        '''
        Return etalon signal(Signal from scenariy.csv) from measurement storage
        num_pnt - number of point start form: 1, end: 156
        '''
        return self.psi_pnts[num_pnt - 1].etalon_signal

    def get_mte_signal(self, num_pnt):
        '''
        Return mte signal(Signal measured by MTE)
        num_pnt - number of point start from: 1, end: 156
        '''
        return self.psi_pnts[num_pnt - 1].MTE_signal

    def set_etalon_measured_signal(self, ):
        pass

    def set_binom_measured_signal(self, num_pnt, num_binom=0, **kwarg):
        '''
        set measured signal from binom
        num_pnt - num PSI point 
        num_binom - no used, reserved for future
        **kwarg - binom results {Ua: val, Ub: val etc}
        '''
        self.psi_pnts[num_pnt - 1].Binom_signals.update(**kwarg)
    
    def set_mte_measured_signal(self, num_pnt, meas_vals):
        '''
        set values measured by MTE
        num_pnt - number point 
        result - (Ua, phaseUa),....(Ic, phaseIc)
        '''
        mte_signal = self.get_mte_signal(num_pnt)  # no need num_pnt - 1, get_mte_signal makes it 
        main_freq_vec = mte_signal.get_main_freq_vector()
        main_freq_vec.update(meas_vals)


# this class inner implementation 
class PSIPointMesurement:
    def __init__(self, num_pnt, etalon_signal, mte_signal):
        self.num_pnt = num_pnt
        self.etalon_signal = etalon_signal       # place signal from CSV type Signal
        self.MTE_signal = mte_signal             # place signal return from MTE
        self.Binom_signals = vs.MeasuredSignal() # [] in future it must be list of Binoms

    def calc_inaccuracy(self):
        pass

def make_signal_from_csv_source(txt_par_dict, num_pnt):
    '''

    '''
    par = txt_par_dict[num_pnt]
    freq = float(par["F"])
    signal = measurement_storage.get_etalon_signal(num_pnt)

    signal.set_frequency(freq)             
    main_freq_signal = signal.get_main_freq_vector() # vs.VectorValues()

    nominals = (float(par["Ua"]), float(par["Ub"]), float(par["Uc"]), float(par["Ia"]), float(par["Ib"]), float(par["Ic"]))

    phiUb = float(par["Phi_Uab"])
    phiUc = float(par["Phi_Uac"])
    
    main_freq_signal.set("Ua", nominals[0], 0)
    main_freq_signal.set("Ub", nominals[1], phiUb)   # ??? phase correct ???
    main_freq_signal.set("Uc", nominals[2], phiUc)
    
    main_freq_signal.set("Ia", nominals[3], 0 + float(par["Phi_A"]))
    main_freq_signal.set("Ib", nominals[4], phiUb + float(par["Phi_B"]))
    main_freq_signal.set("Ic", nominals[5], phiUc + float(par["Phi_C"]))
    
    for num_harm, harm_names in zip(range(2, 51) ,names_par.get_voltage_harmonic_names()):
        uh_name, ih_name, phi_name_uh, phi_name_ih = harm_names
        
        harm = signal.get_vector_harm(num_harm)  # vs.VectorValues()
        
        percent_uh, phi_uh = float(par[uh_name]), float(par[phi_name_uh])  # 3 phases have identical values
        for ind, name in enumerate(names_par.get_phase_voltage_names()):
            harm.set(name, nominals[ind] * percent_uh / 100, phi_uh)

        percent_ih, phi_ih = float(par[ih_name]), float(par[phi_name_ih])
        for ind, name in enumerate(names_par.get_phase_current_names()):
            harm.set(name, nominals[3 + ind] * percent_ih / 100, phi_ih)
            
        # signal.add_harm(names_par.get_num_harm(uh_name), harm)
    
    # put interharmonics into signal. Notice!!! current csv scenary don't have phase shift on interharmonics!!!
    for num_interharm, inter_harm in zip(range(1, 50), names_par.get_voltage_interharmonic_names()):
        ui_name, ii_name = inter_harm
        harm =  signal.get_vector_interharm(num_interharm)  # vs.VectorValues()
        percent_ui = float(par[ui_name])
        for ind, name in enumerate(names_par.get_phase_voltage_names()):
            harm.set(name, nominals[ind] * percent_ui / 100, 0)
        percent_ii = float(par[ii_name])
        for ind, name in enumerate(names_par.get_phase_current_names()):
            harm.set(name, nominals[3 + ind] * percent_ii / 100, 0)
        # signal.add_interharm(names_par.get_num_harm(ui_name), harm)
    
    signal.calc_measured_param()
    
    # return signal
     
measurement_storage = MeasurementStorage()

if __name__ == '__main__':
    pass