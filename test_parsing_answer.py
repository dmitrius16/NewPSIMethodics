'''
Functions from Alexey
'''
import math
import get_common_params_Counter
import get_common_params_Generator

test_gen_vltg_str = "RSU1=1,-8.1596E-1+0.0000E+0-5.8515E+3-1.4906E+4-4.8632E-1+2.2096E+0+3.0670E-1\
+3.2926E+0-6.1154E-1+5.1914E-1-1.1498E+3+3.5535E+2+1.5143E+0-2.4576E+0\
+1.9288E+0+1.5160E+0+2.6277E+0+4.1370E+0+3.2185E+2+1.4137E+3-2.0033E-1\
-6.6022E+0+2.6850E-2-2.8454E+0+7.1025E-1-4.6049E-1+7.7811E-2-2.5264E+0\
-6.3355E-1+1.2601E+0+2.7806E-1+2.7833E+0-7.6836E-1-1.3983E+0-7.3533E-1\
-4.4604E-1-1.3231E+0-1.9477E+0+2.0036E+0+2.6099E-1+1.1561E+3+4.5556E+2\
+1.4737E-1+1.3723E+0-2.7541E+0+1.6767E+0-2.4290E-1+6.0855E-1-1.4716E+0\
-7.4359E-1+9.0278E-1+9.0522E-1+6.3716E-1+6.5885E-1-2.3901E+0+1.2467E-1\
-4.2556E-1+3.8690E+0-1.6313E+0+1.1791E+0-8.8034E+2+2.0066E+2+2.7732E-1\
-3.4177E-1+5.4442E-1-1.0312E+0+8.2512E-1-2.8552E-1+8.5314E-1-6.3806E-1\
-3.0569E+0-7.5819E-1+3.6516E-2-9.0539E-2+1.7543E+0-2.9458E+0-3.4332E+0\
-4.0987E+0+1.8043E+0-1.2818E+0-5.8302E-2+5.2695E-1+1.4685E+0-1.0208E+0\
-3.4275E-1+1.0340E-1+1.8254E-1+1.4110E+0-6.8059E-1+3.2402E-1+4.3896E-1\
+8.2247E-1-2.6417E-1+1.3981E+0-1.1315E-2+2.0619E+0+2.0367E+0+9.8156E-1\
-4.5368E+0+2.7012E+0+1.6904E+0-1.6455E+0+2.4463E+0+7.4046E-1-8.4617E-1\
-1.0643E-1-1.5904E+0-1.0854E+0-1.8769E-1-8.4075E-1+3.7675E-1-1.9642E+0\
-2.6016E-1-1.3612E+0+9.2350E-1-2.6723E-1+1.1314E+0-4.6097E-1+1.6335E+0\
-4.5696E+0-3.1771E+0+5.0842E+0+5.3989E-1+2.5758E+0+2.8264E-1+4.5005E-1\
+2.5807E-1-2.4964E-1\r"

test_gen_current_str = "RSI1=1,+1.4889E+0+0.0000E+0-1.6193E+4-2.5196E+3-6.4056E-1-5.6108E-1-1.7295E+0\
+2.7092E+0-7.0147E-2-4.9538E-1-1.1732E+2-1.1443E+2+2.6749E-1+2.8024E-1-1.1778E+0+1.0878E+0-8.4176E-1\
+1.0816E-1-7.5784E-1+1.3990E+0+9.0228E+1+1.3647E+2+8.1165E-1-5.5245E-1+1.4482E+0-4.9610E-1-6.5433E-1\
+2.1157E-1-9.8769E-2-1.9350E-1+7.8781E-2-2.5845E-1-4.2034E-1+2.4337E-1+2.0823E-1-5.8144E-2-7.4162E-1\
+1.5311E-2+1.2111E+0+3.2218E-1-1.4830E+2-7.5737E+1+1.2909E+0+4.0331E-3-8.3710E-1-2.6440E-2+6.7675E-1\
-2.9812E-1-2.9089E-1-9.0456E-1-5.1044E-2+1.4938E-1-3.2883E-1+6.3729E-1-1.6698E+0-5.2250E-2+1.2219E+0\
-1.7446E+0-2.4921E+0+4.2557E-1-5.5450E+2+6.4276E+2-1.0839E+0-8.3150E-1+3.1970E+0+5.1547E-1-4.6121E-1\
-1.2844E+0-1.0543E-1-4.3645E-1-4.2615E-1-4.7695E-1+7.3079E-1+9.6628E-1+8.7110E-2+8.5235E-2+6.6043E-1\
-3.6960E+0-1.0279E-1+1.6505E+0+7.4937E-2+8.1233E-1+6.6459E-1-1.8939E+0-4.6382E-1+7.2354E-1-7.1664E-1\
+1.0658E+0+5.2768E-3-2.8653E-1+5.0925E-3-1.2401E-1-2.8444E-1+3.2166E-1-9.6888E-1+1.0445E+0-9.0744E-1\
+3.4622E-2-5.3170E-1+9.6687E-1+2.3348E+0-4.8928E-1+3.5912E-1+3.7222E-1+4.5462E-1+2.2671E-1-5.2883E-1\
+3.6971E-2-4.3184E-2+8.6936E-2+5.0697E-1-7.5336E-2-6.6959E-1-2.2484E-1-6.1623E-1-2.7340E-1-1.6717E+0\
-4.0233E-1+1.6191E+0-3.2019E-1+1.3662E+0-4.0186E-1+1.7121E+0+6.9642E-1+5.1404E-1-1.2337E-1+4.7794E-1+2.8155E-2"


def parse_MTE_Generator_Harm_answer(textFromMTE, numPhase, numUI, ser):              # парсить ответ от МТЕ по общим параметрам: 3 числа по 3 фазам
    '''

    '''
    print("parse_MTE_Harm_answer: " + textFromMTE)

    # распарсить значения -> сгруппировать Ре и Им части в массивы -> узнать текущй диапазонизмерения -> 
    # -> расчет окончательного результата

    textFromMTE_common = textFromMTE.split(",")
    
    if float(textFromMTE_common[1]) == 0:
        print("No harmonics. Amplifier switched off")
        return

    flafNewVal = textFromMTE_common[0][-1]      # доступны ли новые данные для считывания

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

    list_module = []
    list_angle = []

    radToDeg_coef = 180.0 / math.pi

    for idx in range(len_re_im_div20):
        list_module.append( math.sqrt(list_re[idx]*list_re[idx] + list_im[idx]*list_im[idx]) )
        if list_re[idx] != 0.0:
            list_angle.append( radToDeg_coef * math.atan(list_im[idx]/list_re[idx])) 
        else:
            list_angle.append(0) 

        print('{0:4d} {1:14f} {2:14f}'.format(idx, list_module[idx], list_angle[idx]))


    return zip(list_module, list_angle)

def parse_MTE_Counter_answer(textFromMTE=test_gen_vltg_str, UI_max=130):              # парсить ответ от МТЕ по общим параметрам: 3 числа по 3 фазам

    #####print("parse_MTE_Harm_answer: " + textFromMTE)

    # формат принимаемой строки: RS(U/I)<ph>=<0/1>,<re0><im0><re1><im1> ... <re31><im31>
    # формат значения: <re[i]> = (+/-)Z.zzzzE(+/-)Z (итого 10 символов)
    #   распарсенное значение: re[i] = float(str_re_i[0:7:1])*10**float(str_re_i[8:10:1])
    
    # распарсить значения -> сгруппировать Ре и Им части в массивы -> узнать текущй диапазонизмерения -> 
    # -> расчет окончательного результата

    textFromMTE_common = textFromMTE.split(",")
    flafNewVal = textFromMTE_common[0][-1]      # доступны ли новые данные для считывания

    ### Begin распарсить значения -> сгруппировать Ре и Им части в массивы ->
    re_im_str = textFromMTE_common[1]       # строка только из форматированных значений Re и Im

    len_re_im_div20 = 32         # 31 + 1 = 32 - Число гармоник которое считает МТЕ (31) плюс основная гармоника

    list_re = []    # списки со значениями Ре (и Им)
    list_im = []

    t_re = t_im = 0 # промежуточные переменные для формирования значений Ре и Им
    t_idx = 0

    for idx in range(len_re_im_div20):
        t_idx = idx*20
        t_re = float(re_im_str[t_idx:t_idx+7:1])*10**float(re_im_str[t_idx+8:t_idx+10:1])
        list_re.append(t_re)
        t_idx = t_idx + 10
        t_im = float(re_im_str[t_idx:t_idx+7:1])*10**float(re_im_str[t_idx+8:t_idx+10:1])
        list_im.append(t_im)
    ### End распарсить значения -> сгруппировать Ре и Им части в массивы ->

    # шапка таблицы результатов измерения гармоник
    print('{0:^4s} {1:^14s} {2:^14s}'.format("harm №", "Abs","Ang, [°]"))

    list_module = []
    list_angle = []

    radToDeg_coef = 180.0 / math.pi
    harm_coef = UI_max / 32767.0

    for idx in range(len_re_im_div20):
        list_re[idx] = list_re[idx] * harm_coef    # списки со значениями Ре (и Им)
        list_im[idx] = list_im[idx] * harm_coef

        list_module.append( math.sqrt(list_re[idx]*list_re[idx] + list_im[idx]*list_im[idx]) )
        list_angle.append( radToDeg_coef * math.atan(list_im[idx]/list_re[idx])) 

        print('{0:4d} {1:14f} {2:14f}'.format(idx, list_module[idx], list_angle[idx]))

    
    
    #! Вызовы функции Дмитрия: "получить значения спектра:  1) амплитуд гармоник  (0..31) \
    #                                                       2) фаз гармоник       (0..31) \ 
    #                                                       3) напряжение/ток     (0,1,2) \
    #                                                       4) фаза A/B/C         (0,1) \                "
    return zip(list_module, list_angle)



if __name__ == "__main__":
    pass