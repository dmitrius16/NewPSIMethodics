'''
test_point_signal - module containes classes for description test point
'''
from names_parameters import get_names_harm_vector
class VectorValues:
    def __init__(self,**kwargs):
        self.storage = dict(zip(get_names_harm_vector(), ((0, 0),) * 6 ))
    def set(self, name, ampl, phase_grad):
        '''
        name_param: string with name param. Valid names: Ua, Ub, Uc, Ia, Ib, Ic
        ampl: signal amplitude
        phase_grad: signal phase
        '''
        if name in get_names_harm_vector():
            self.storage[name] = (ampl, phase_grad)
    
    def get(self, name):
        '''
        get - return pair amplitude, phase of given name
        '''
        return self.storage[name]


class Signal:
    '''
    Signal represents point in generator.
    '''
    def __init__(self, freq):
        self.frequency = freq
        self.set_harmonics = dict()
    def add(self, vector_values):
        '''
        add main frequency vector values
        vector_values - type VectorValues from test_point_signal.py
        '''
        self.set_harmonics[0] = vector_values

    def add_harm(self, num_harm, vector_values):
        '''
        add harmonics to signal
        vector_values - type VectorValues from test_point_signal.py
        '''
        self.set_harmonics[num_harm] = vector_values
    


if __name__ == __main__:
    pass