"""
MTE_device - base class for classes MTE_Generator and MTE_counter
"""

from MTE_Device import C_MTE_device

#import csv
#import collections
#import names_parameters     # All names measurement parameters and generator's parameters (Дмитрий)
import MTE_parameters 

from math import (pi, atan, sqrt)

#import signal

'''
---Обработчики меню

GetMenuHandler		    -- меню выбора измерений генератора
GetCommonMenu_Handler	-- подменю измерения общих параметров генератора

--Set/Get команды

OFF_signal		        --выключить сигнал на выходе генератора МТЕ
SET_cmd			        --включить сигнал и применить установленные значения
get_current_PSI_pnt_num --получить текущей номер точки ПСИ
set_meas_time		    --установить время измерения генератора (минимальное время 1 секунда)
set_PSI_point		    --установить точку ПСИ


---Вспомогательные функции

calculate_spectrum_by_generator --запросить, принять и распарсить значения спектра
send_to_MTE		        --переопределение метода "передать команду устройству МТЕ"
parse_MTE_Harm_answer	--парсинг строки-спектра от генератора МТЕ
'''

class C_MTE_Generator(C_MTE_device):
    def __init__(self ,ser, ser_timeout, start_cmd,b_print_cmd,b_print_answ):
        # Необходимо вызвать метод инициализации родителя.
        # В Python 3.x это делается при помощи функции super()
        #http://pythonicway.com/education/python-oop-themes/21-python-inheritance

        super().__init__(ser, ser_timeout, start_cmd,b_print_cmd,b_print_answ)

        self.num_PSI_point = 0        # номер текущей, установленной точки ПСИ
        #self.pnts_for_generator = []  

        self.GetCommonMenuItems_mas = [  "\r\nChoose common params values:",                        0,  0,
                                            "1 - Currents [A]: I1, I2, I3",                         1,  1,
                                            "2 - Voltages [V]: U1, U2, U3",                         2,  2,
                                            "3 - Phi current absolute [°]: phiU1, phiU2, phiU3",    3,  12,
                                            "4 - Phi voltage absolute [°]: phiI1, phiI2, phiI3",    4,  13,
                                            "5 - Frequency [Hz]: freq",                             5,  1113,
                                            "6 - Back",                                             6,  1123]    
        self.harm_dict = {    0: 1,
                                1: 2,
                                2: 3,
                                3: "RSU",
                                4: "RSI"}
        self.numUI = 0
        self.numPhase = 0

        self.list_module = []
        self.list_angle = []

        self.flag_exist_vol_harm = False
        self.flag_exist_cur_harm = False

        self.is_PSI_pnt_set = False

        self.list_Ua_mod = []
        self.list_Ua_ang = []
        self.list_Ub_mod = []
        self.list_Ub_ang = []
        self.list_Uc_mod = []
        self.list_Uc_ang = []

        self.list_Ia_mod = []
        self.list_Ia_ang = []
        self.list_Ib_mod = []
        self.list_Ib_ang = []
        self.list_Ic_mod = []
        self.list_Ic_ang = []

        self.list_name_m = [self.list_Ua_mod,\
                            self.list_Ub_mod,\
                            self.list_Uc_mod,\
                            self.list_Ia_mod,\
                            self.list_Ib_mod,\
                            self.list_Ic_mod]
        
        self.list_name_a = [self.list_Ua_ang,\
                            self.list_Ub_ang,\
                            self.list_Uc_ang,\
                            self.list_Ia_ang,\
                            self.list_Ib_ang,\
                            self.list_Ic_ang]
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Переопределение метода посылки команд для генератора
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def send_to_MTE(self,write_str):
        print("Send cmd to Generator")
        self.send_direct_cmd(write_str)

    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Выключить каналы генератора. OFF1 - мгновенно, OFF - плавно (около 1,5 сек.)
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def OFF_signal(self):
        #self.send_to_MTE("OFF1\r")
        self.send_direct_cmd("OFF\r")

    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Применить настройки и включить сигнал по всем каналам и фазам генератора
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def SET_cmd(self):
        self.send_to_MTE("SET\r")

    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Вернуть номер текущей (установленной) точки ПСИ
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def get_current_PSI_pnt_num(self):
        return self.num_PSI_point

    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Обработчик меню измерений генератора
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def GetMenuHandler(self):
        while(True):

            print("\r\nGet menu:")
            print("1 - Common params measurements")
            print("2 - Harmonics measurements")
            print("3 - Back")

            num = int(input())

            if num == 3:
                print("\r\nPressed: 3 - Back")
                return
            elif num == 1:
                print("\r\nPressed: 1 - Common params measurements")
                for number in range(int(len(self.GetCommonMenuItems_mas)/3)):
                    print(self.GetCommonMenuItems_mas[number*3])

                self.GetCommonMenu_Handler()  # обработчик ответа от генератора МТЕ
            elif num == 2:
                print("\r\nPressed: 2 - Harmonics measurements Generator")
                # режим гармоник -> выбор фазы -> выбор ток/напряжение -> парсим ответ
                print("\r\nChoose phase A/B/C:")
                print("1 - A")
                print("2 - B")
                print("3 - C")
                print("4 - Back") #  меню выбора гармоник     выбор фазы ->
                GetHarmPhase_num = int(input())
                if GetHarmPhase_num == 4:
                    print("\r\nPressed: 4 - Back")
                else:
                    print("\r\nChoose phase U/I:")
                    print("1 - U")
                    print("2 - I")
                    print("3 - Back")    #  меню выбора гармоник     выбор ток/напряжение ->
                    GetHarmUI_num = int(input())
                    if GetHarmUI_num == 3:
                        print("\r\nPressed: 3 - Back")
                    else:
                        print("get_harms_params_Generator.calculate_spectrum_by_generator")
                        num_spectrum = (GetHarmPhase_num - 1)*3 + (GetHarmUI_num - 1)
                        self.calculate_spectrum_by_generator(GetHarmPhase_num,GetHarmUI_num, num_spectrum)
                        #self.Harms_Type_Harms_Handler(GetHarmPhase_num,GetHarmUI_num)    # -> парсим ответ		
            else:
                print("Something go wrong! input num (1-4) 'Measure menu 'Generator MTE''.")

    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----обработчик выбора фазы для которой измерить гармоники 
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    '''
    def Harms_Type_Harms_Handler(self,numPhase,numUI):

        harm_dict = {  0: 1, 1: 2, 2: 3, 3: "RSU", 4: "RSI"}
        harmCommand = harm_dict[numUI+2] + str(harm_dict[numPhase-1]) + "\r" # строка: команда запроса спектра с генератора МТЕ
        #self.send_to_MTE(harmCommand)

        self.ser_port.timeout = 1        
        
        harmCommand_answer = self.send_cmd_to_device(harmCommand)
        #textFromMTE = get_common_params_Counter.sendCommandToMTE(ser,harmCommand,1,1)   # ответ генератора МТЕ
        self.parse_MTE_Harm_answer(harmCommand_answer)              # парсинг строки-спектра от генератора МТЕ
        
        self.ser_port.timeout = 0.5
    '''

    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Установить время измерения генератора
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def set_meas_time(self, meas_time):

        if meas_time < 1.0:
            print("Input generator measurement time is less then 1 sec. Minimum meas time is 1.0 sec.")
            print("Generator measurement time 1 sec. is setted")
            meas_time = 1.0

        self.set_measure_time(meas_time)

    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Установить точку ПСИ
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def set_PSI_point(self, sig):

        #0 проверка на корректность введенного номера точки
        '''
        if num_PSI_point > 0 and num_PSI_point < 157:
            self.num_PSI_point = num_PSI_point
            pnt_param = self.pnts_for_generator.get(self.num_PSI_point)     # параметры точки
        else:
            print("Error in input num PSI point/ Input int number in interval 1 - 156.  You input: "+str(num_PSI_point))
            return
        '''
        #self.num_PSI_point = 1
        #pnt_param_old = self.pnts_for_generator.get(self.num_PSI_point)

        main_sig = sig.get_main_freq_vector()
        main_freq = sig.get_frequency()

        #1 - увеличиваем время между командами, для обработки генератором "длинных последовательностей команд"
        self.ser_port.timeout = 1 # [sec.]

        #2 - выключение сигнала на выходе генератора
        self.OFF_signal()

        #3 - установка всех параметров и диапазонов генератора для следующей точки ПСИ
        #3.1 - генерация строки команд управления генератором МТЕ
        cmd_remove_harms = "OWI1,0,0;OWI2,0,0;OWI3,0,0;OWU1,0,0;OWU2,0,0;OWU3,0,0;"
        cmd_base_param = cmd_remove_harms + MTE_parameters.generate_commands_base_params(main_sig,main_freq) 

        #3.2 - установить диапазоны для генератора МТЕ
        cmd_ranges_param = MTE_parameters.get_ranges_GEN()
        self.send_to_MTE(cmd_ranges_param)

        #3.3 - установить параметры сигнала основной частоты в генератор МТЕ
        self.send_to_MTE(cmd_base_param)

        #'''
        #3.4 - установить параметры гармоник в генератор МТЕ
        cmd_vol_harm_param, cmd_curr_harm_param = MTE_parameters.generate_harm_cmd(sig)

        if cmd_vol_harm_param != "":
            self.flag_exist_vol_harm = True
            self.send_to_MTE(cmd_vol_harm_param)

        if cmd_curr_harm_param != "":
            self.flag_exist_cur_harm = True
            self.send_to_MTE(cmd_curr_harm_param)

        # 'Проверка по генератору'
        # команда запрос - парсинг ответа -> если (измеренное значение - установленное значение) < дельта
        # то переходим к 'проверке по счетчику',
        # Если > дельта, то измеряем снова, но не более 5 раз. Если после 5 раз условие все еще не выполнено,
        # то устанавливаем точку ПСИ заново: generator_MTE.set_PSI_point(num_pnt). Если и в этом случае точка не установлена,
        # выходим в основное меню, сообщаем о том что точка не установлена, сбрасываем сигнал в ноль

        self.ser_port.timeout = 1
        self.send_to_MTE("??????")  # искусственная пауза   
        self.ser_port.timeout = 1
        
        #3.5 - Установить сигнал на выходе генератора
        self.SET_cmd()
        
        #3.6 - "Проверка по генератору" по сигналу основной частоты
        self.is_PSI_pnt_set = self.check_PSI_point_main_freq(sig)         

        #3.6.1 - Если с первого раза точка не установилась, то попробовать еще раз
        if self.is_PSI_pnt_set == False:                            
            print("Trying to set PSI point again")
            self.ser_port.timeout = 1
            self.send_to_MTE("??????")               #искусственная пауза
            self.ser_port.timeout = 1
            
            self.SET_cmd()

            self.ser_port.timeout = 1
            self.send_to_MTE("??????")            #искусственная пауза
            self.ser_port.timeout = 1

            self.is_PSI_pnt_set = self.check_PSI_point_main_freq(sig)

            if self.is_PSI_pnt_set == False:
                print("Set PSI point again - Fail. PSI point still non set.\n Off signal on generator \n Back to main menu")
                self.OFF_signal()
                return self.is_PSI_pnt_set

        
        #if (self.flag_exist_vol_harm == True) or (self.flag_exist_cur_harm == True):     # проверка по гармоникам
        #    self.is_PSI_pnt_set = self.check_PSI_point_harms(sig)
        
        #5 - вернуть короткое время между ответами генератора
        self.ser_port.timeout = 0.2

        return self.is_PSI_pnt_set


    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Обработчик 'проверки по генератору' по гармоникам
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    
    def check_PSI_point_harms(self,sig):
        # Алгоритм работы следующий:
        # запрсили-сохранили-распарсили все спектры с генератора
        # проверяем по амплитудам гармоник и по всем фазам установку сигнала

        keys_vect_dict = ["Ua", "Ub", "Uc", "Ia", "Ib", "Ic"]
        #1 запрсили-сохранили-распарсили все спектры с генератора
        numUI_mas = [1,2]   # 1-U, 2-I
        numPhase_mas = [1,2,3]   # 1-A, 2-B, 3-C
  
        idx_list = 0
        for idx_ui in range(len(numUI_mas)):                # цикл: напряжение/ток
            for idx_ph in range(len(numPhase_mas)):         # цикл: по фазам А/B/C
                self.calculate_spectrum_by_generator(numUI_mas[idx_ui],numPhase_mas[idx_ph],(idx_ph-1)*3+(idx_ui-1))
                print("idx_list "+str(idx_list))
                idx_list += 1

        print("self.list_Ua_ang, "+str(len(self.list_Ua_ang))+\
                    " self.list_Ub_ang, "+str(len(self.list_Ub_ang))+\
                    " self.list_Uc_ang, "+str(len(self.list_Uc_ang))+\
                    " self.list_Ia_ang, "+str(len(self.list_Ia_ang))+\
                    " self.list_Ib_ang, "+str(len(self.list_Ib_ang))+\
                    " self.list_Ic_ang, "+str(len(self.list_Ic_ang)) )
        
        print(" self.list_Ua_mod, "+str(len(self.list_Ua_mod))+\
                           " self.list_Ub_mod, "+str(len(self.list_Ub_mod))+\
                           " self.list_Uc_mod, "+str(len(self.list_Uc_mod))+\
                           " self.list_Ia_mod, "+str(len(self.list_Ia_mod))+\
                           " self.list_Ib_mod, "+str(len(self.list_Ib_mod))+\
                           " self.list_Ic_mod, "+str(len(self.list_Ic_mod)) )

        #print("list_magn " + str(len(list_magn)))
        #print("list_angl " + str(len(list_angl)))

        #2 проверяем по амплитудам гармоник и по всем фазам установку сигнала
        delta = 5   # [%]
        set_PSI_point_flag = True

        for idx_harm_num in range(2, 32):   # цикл по всем гармоникам
            cur_harm_signal = sig.get_vector_harm(idx_harm_num)    # текущий объект Vector_values с параметрами idx_harm_num гармоники
            for idx_phase in range(6):              # цикл по содержимому векторов

                etalon_ampl = cur_harm_signal.get(keys_vect_dict[idx_phase])[0] 
                print("idx_phase: "+str(idx_phase)+"  idx_harm_num " + str(idx_harm_num))
                
                measered_ampl = self.list_name_m[idx_phase][idx_harm_num]
                #measered_ampl = self.list_Ua_mod[idx_harm_num]

                if etalon_ampl != 0.0: 
                    cur_delta = abs((etalon_ampl - measered_ampl)/etalon_ampl) * 100.0
                elif measered_ampl != 0.0: 
                    cur_delta = abs((measered_ampl - etalon_ampl)/measered_ampl) * 100.0
                else:
                    cur_delta = 0

                if cur_delta > delta:
                    print("Error on phase "+str(idx_phase)+" harm num: "+str(idx_harm_num)+\
                          ": measered_ampl: " + str(measered_ampl)+" etalon_ampl: " + str(etalon_ampl) +\
                                " calc delta %: "+str(cur_delta)+" max delta %: "+str(delta))
                    set_PSI_point_flag = False
                else:
                    set_PSI_point_flag = True

        print("finally set_PSI_point_flag HARMS: "+str(set_PSI_point_flag))
        return set_PSI_point_flag

    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Обработчик 'проверки по генератору' по основной частоте
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    
    def check_PSI_point_main_freq(self,sig):

        ask_str_mas = ["?2;","?1;","?13;","?12;","FRQ;"]      # команда-запрос: "I,U,phI,phU,FRQ"
        
        #Ua, Ub,  Uc,  Ia,  Ib, Ic  = 0    # амплитуды
        #pUa, pUb, pUc, pIa, pIb, pIc = 0    # фазы
        meas_vals = []

        # отправка команды получение ответа (по одной)
        self.ser_port.flushInput()
        self.ser_port.flushOutput()

        main_sig = sig.get_main_freq_vector()
        etalon_freq = sig.get_frequency()
        measfreq = 0

        keys_vect_dict = ["Ua", "Ub", "Uc", "Ia", "Ib", "Ic"]
        etalon_vals = []

        for idx_keys in keys_vect_dict:
            etalon_vals.append(main_sig.get_ampl(idx_keys))

        for idx_keys in keys_vect_dict:    
            t_phase = main_sig.get_phase(idx_keys)
            if t_phase > 180: t_phase = t_phase - 360
            if t_phase < -180: t_phase = t_phase + 360
            etalon_vals.append(t_phase)

        ##########################
        ##########################
        ##########################
        N_total_iter = 4    #  Сколько раз повторно спрашиваем измерения с генератора МТЕ
        delta = 4   # [%]
        set_PSI_point_flag = [] # список флагов: пройдена ли проверка по этому параметру. 
        #Сигнал считается установленным когда по всем параметрам пройдена проверка. Наиболее часто не устанавливается сигнал тока фазы А

        self.ser_port.timeout = 0.2     # интервал между опросами коротких команд
        ##########################
        ##########################
        ##########################
        print("check_PSI_point Generator")
        # ПРОВЕРКА с "Эталоном"
        '''
        Проверка на то, установились ли правильные значения.
        Проверяем по относительной погрешности установившихся значений: если погршность меньше 1% (а может и 5%), то считаем что все в порядке
        '''

        for check_gen_iter in range(N_total_iter):              # Внешний цикл по итерациям - опрос-анализ ответа от МТЕ
            print("check_gen_iter: "+str(check_gen_iter+1))
            self.ser_port.flushInput()
            self.ser_port.flushOutput()
            
            meas_vals = []                      # обнуление списков после каждой итерации опроса
            set_PSI_point_flag = []
            #meas_vals.clear()
            #set_PSI_point_flag.clear()
            check_set_PSI = False

            for ask in range(len(ask_str_mas)):
                self.ser_port.write(ask_str_mas[ask].encode())  
                textFromMTE = self.ser_port.read(800)
                textFromMTE = textFromMTE.decode()
                if ask < 3:

                    if ask < 2:                     # Обработка ответов на запрос 1-ампл. тока, 2-ампл. напряжения
                        va, vb, vc = self.parse_MTE_answer_text(textFromMTE)
                        meas_vals.append(va)
                        meas_vals.append(vb)
                        meas_vals.append(vc)
                        #print("va: "+str(va)+"vb: "+str(vb)+"vc: "+str(vc))
                    else:
                        # ask == 2 - phase_U
                        va, vb, vc = self.parse_MTE_answer_text(textFromMTE)
                        
                        # проверка если значение близко к 180 по модулю 360
                        margin_angle = 5
                        delta_a = abs(abs(va) - 180.0)
                        delta_b = abs(abs(vb) - 180.0)
                        delta_c = abs(abs(vc) - 180.0)
                        
                        va = va*(-1)
                        vb = vb*(-1)
                        vc = vc*(-1)
                        if (va < -180.0) or (delta_a < margin_angle): va += 360    
                        if (vb < -180.0) or (delta_b < margin_angle): vb += 360
                        if (vc < -180.0) or (delta_c < margin_angle): vc += 360
                        
                        meas_vals.append(va)
                        meas_vals.append(vb)
                        meas_vals.append(vc)

                        #print("va: "+str(va)+"vb: "+str(vb)+"vc: "+str(vc))
                    for t_idx in range(3):
                        phase_idx = ask*3 + t_idx
                        
                        if etalon_vals[phase_idx] != 0.0: 
                            cur_delta = abs((etalon_vals[phase_idx] - meas_vals[phase_idx])/etalon_vals[phase_idx]) * 100.0
                        elif meas_vals[phase_idx] != 0.0: 
                            cur_delta = abs(meas_vals[phase_idx]) * 100.0
                        else:
                            cur_delta = 0

                        if cur_delta > delta:
                            #print("Error on phase "+str(t_idx)+": measured value: " + str(meas_vals[phase_idx])+" etalon value: " + str(etalon_vals[phase_idx]) +\
                            #           " calc delta %: "+str(cur_delta)+" max delta %: "+str(delta))
                            #set_PSI_point_flag = False
                            set_PSI_point_flag.append(False)
                        else:
                            #set_PSI_point_flag = True
                            set_PSI_point_flag.append(True)
                elif ask == 3:

                    # ask == 3 - phase_I
                    va, vb, vc = self.parse_MTE_answer_text(textFromMTE)
                    
                    # проверка если значение близко к 180 по модулю 360
                    margin_angle = 5
                    delta_a = abs(abs(va) - 180.0)
                    delta_b = abs(abs(vb) - 180.0)
                    delta_c = abs(abs(vc) - 180.0)
                        
                    va = va*(-1)
                    vb = vb*(-1)
                    vc = vc*(-1)
                    if (va < -180.0) or (delta_a < margin_angle): va += 360    
                    if (vb < -180.0) or (delta_b < margin_angle): vb += 360
                    if (vc < -180.0) or (delta_c < margin_angle): vc += 360
                            
                    meas_vals.append(va)
                    meas_vals.append(vb)
                    meas_vals.append(vc)
                    #print("va: "+str(va)+"vb: "+str(vb)+"vc: "+str(vc))

                    for t_idx in range(3):
                        phase_idx = ask*3 + t_idx
                        
                        if etalon_vals[phase_idx] != 0.0: 
                            cur_delta = abs((etalon_vals[phase_idx] - meas_vals[phase_idx])/etalon_vals[phase_idx]) * 100.0
                        elif meas_vals[phase_idx] != 0.0: 
                            cur_delta = abs(meas_vals[phase_idx]) * 100.0
                        else:
                            cur_delta = 0

                        if cur_delta > delta:
                            #print("Error I phase on phase "+str(t_idx)+": measured value: " + str(meas_vals[phase_idx])+" etalon value: " + str(etalon_vals[phase_idx]) +\
                            #           " calc delta %: "+str(cur_delta)+" max delta %: "+str(delta))
                            #set_PSI_point_flag = False
                            set_PSI_point_flag.append(False)
                        else:
                            #set_PSI_point_flag = True
                            set_PSI_point_flag.append(True)
                else:
                    measfreq = self.parse_MTE_answer_Freq_text(textFromMTE)
                    #print("vfreq: "+str(measfreq))

                    if etalon_vals[phase_idx] != 0.0: 
                        cur_delta = abs((etalon_freq - measfreq)/etalon_freq) * 100.0
                    else:
                        cur_delta = 0

                    if cur_delta > delta:
                        #print("Error in Frequency measured value: " + str(measfreq)+" etalon value: " + str(etalon_freq) +\
                        #           " calc delta %: "+str(cur_delta)+" max delta %: "+str(delta))
                        #set_PSI_point_FREQ_flag = False
                        set_PSI_point_flag.append(False)
                    else:
                        #set_PSI_point_FREQ_flag = True
                        set_PSI_point_flag.append(True)
                        
            check_set_PSI = True
            for flag_elem in set_PSI_point_flag:
                if flag_elem == False:
                    check_set_PSI = False
                    break

            if check_set_PSI == True:
                break
            
            self.ser_port.timeout = 1
            self.ser_port.write("".encode())        # перерыв между опросами в одной итерации равный 1 секунде
            self.ser_port.timeout = 0.2

        print("finally Generator: check_set_PSI == "+str(check_set_PSI))
        return check_set_PSI

    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Обработчик измерения общих параметров генератора
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def GetCommonMenu_Handler(self):
        print("GetCommonMenu_Handler")
        num = int(input())
        if num == 6:
            print("\r\nPressed: 6 - Back")
            return
        elif num >= 1 and num <= 4:
            print("Waiting for measured: " + self.GetCommonMenuItems_mas[num*3]) 
            write_str = "?" + str(self.GetCommonMenuItems_mas[num*3+2]) + ";"

            self.send_cmd_to_device(write_str)

        elif num == 5:
            print("Waiting for measured: FREQ")
            write_str = "FRQ\r"

            self.send_cmd_to_device(write_str)   

        else:
            print("Something go wrong! input num set menu item.")
            return

        #textFromMTE = read_MTE_answer(ser)              #1 считываем строку измерений МТЕ (из виртуального порта)
        
        if num != 5:
            vA = vB = vC = 0
            vA, vB, vC = self.parse_MTE_answer()   #2 парсим считанную строку
            print("\r\nValue A: ",str(vA),\
                "Value B: ",str(vB),\
                "Value C: ",str(vC))                     #3 выводим распарсенный результат
        else:
            vFreq = 0
            vFreq = self.parse_MTE_answer_Freq()      #2 парсим считанную строку
            print("\r\nFreq is: ",str(vFreq), "  Hz")                      #3 выводим распарсенный результат


    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Измерение спектра (генератор)
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def calculate_spectrum_by_generator(self,numUI,numPhase,num_list_m):
        self.numUI = numUI
        self.numPhase = numPhase

        self.ser_port.timeout = 1  
        
        harmCommand = self.harm_dict[self.numUI+2] + str(self.harm_dict[self.numPhase-1]) + "\r"            # строка: команда запроса спектра с генератора МТЕ
        harm_text = self.send_cmd_to_device(harmCommand) 

        self.ser_port.timeout = 0.2

        self.parse_MTE_Harm_answer(harm_text,num_list_m)              # парсинг строки-спектра от генератора МТЕ
    
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Измерение спектра (генератор)
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def get_spectrum_result(self):
        return self.list_module, self.list_angle

    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    #-----Парсинг строки-спектра (генератор)
    #-----------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------#
    def parse_MTE_Harm_answer(self,textFromMTE,num_list_m):# парсинг строки-спектра от генератора МТЕ
        #print("parse_MTE_Harm_answer: " + textFromMTE)
        # распарсить значения -> сгруппировать Ре и Им части в массивы -> расчет окончательного результата
        textFromMTE_common = textFromMTE.split(",")
        
        if len(textFromMTE_common) <= 1:
            print("no elements in string: parse_MTE_Harm_answer")
            return

        if float(textFromMTE_common[1]) == 0:
            print("No harmonics. Amplifier switched off")
            return

        #flafNewVal = textFromMTE_common[0][-1]      # доступны ли новые данные для считывания

        ### Begin распарсить значения -> сгруппировать Ре и Им части в массивы ->
        
        multFactor = float(textFromMTE_common[1])   # общий множитель
        re_im_str = textFromMTE_common[2]           # строка только из форматированных значений Re и Im
        len_re_im_div20 = 32         # 31 + 1 = 32 - Число гармоник которое считает МТЕ (31) плюс основная гармоника

        list_re = []    # списки со значениями Ре (и Им)
        list_im = []

        t_re = t_im = 0 # промежуточные переменные для формирования значений Ре и Им
        t_idx = 0

        #coefMult = multFactor / 32767.0

        for idx in range(len_re_im_div20):
            # string Re Im -> int Re Im -> float Re Im -> mult multFactor -> div 32767
            t_idx = idx*8
            t_re = float(int(re_im_str[t_idx:t_idx+4:1], 16) ) / 32767.0
            if t_re > 1.0:
                t_re = t_re - 2.0

            t_re = t_re * multFactor
            list_re.append(t_re)

            #print("Re "+str(idx) +"  "+ re_im_str[t_idx:t_idx+4:1] + " " +str(list_re[idx]))
            t_idx = t_idx + 4
            t_im = float(int(re_im_str[t_idx:t_idx+4:1], 16) ) / 32767.0
            if t_im > 1.0:
                t_im = t_im - 2.0

            t_im = t_im * multFactor
            list_im.append(t_im)

            #print("Im "+str(idx) +"  "+ re_im_str[t_idx:t_idx+4:1] + " " +str(list_im[idx]))
        ### End распарсить значения -> сгруппировать Ре и Им части в массивы ->
        
        # шапка таблицы результатов измерения гармоник
        print('{0:^4s} {1:^14s} {2:^14s}'.format("harm №", "Abs","Ang, [°]"))

        #########################################
        #########################################
        self.list_name_m[num_list_m].clear()
        self.list_name_m[num_list_m].clear()
        #########################################
        #########################################

        radToDeg_coef = 180.0 / pi

        for idx in range(len_re_im_div20):
            self.list_name_m[num_list_m].append( sqrt(list_re[idx]*list_re[idx] + list_im[idx]*list_im[idx]) )
            ###list_m.append( sqrt(list_re[idx]*list_re[idx] + list_im[idx]*list_im[idx]) )
            if list_re[idx] != 0.0:
                #self.list_angle.append( radToDeg_coef * math.atan2(list_im[idx], list_re[idx]))

                self.list_name_a[num_list_m].append( radToDeg_coef * atan(list_im[idx]/list_re[idx])) 

                ###list_a.append( radToDeg_coef * atan(list_im[idx]/list_re[idx])) 
            else:
                ###list_a.append(0) 
                self.list_name_a[num_list_m].append( 0.0) 

            print('{0:4d} {1:14f} {2:14f}'.format(idx, self.list_name_m[num_list_m][idx], self.list_name_a[num_list_m][idx]))

        #####################################
        #####################################
        #####################################
        #self.list_name_m[num_list_m] = list_m
        #self.list_name_m[num_list_m] = list_a

        # Передавать в функцию номер массива и сделать тут перекопирование в нужный self. массив. Вместо передачи ссылки как аргумента функции

        #! Вызовы функции Дмитрия: "получить значения спектра:  1) амплитуд гармоник [list_module] (0..31) \
        #                                                       2) фаз гармоник      [list_angle]  (0..31) \ 
        #                                                       3) напряжение/ток                  (0,1)   \
        #                                                       4) фаза A/B/C                      (0,1,2) \  
            



if __name__ == "__main__":
    pass



        