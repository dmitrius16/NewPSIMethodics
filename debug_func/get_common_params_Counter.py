"""
MenuItems for get data from MTE counter
"""


## соберем строки вывода в один массив
GetCommonMenuItems_mas = [  "\r\nChoose common params values:",             0,  0,
                            "1 - Currents [A]: I1, I2, I3",                 1,  1,
                            "2 - Voltages [V]: U1, U2, U3",                 2,  2,
                            "3 - Powers Active [W]: P1, P2, P3",            3,  3,
                            "4 - Powers Reactive [var]: Q1, Q2, Q3",        4,  4,
                            "5 - Powers Full [VA]: S1, S2, S3",             5,  5,
                            "6 - Angle UI [°]: phiUI1, phiUI2, phiUI3",     6,  9,
                            "7 - Linear Voltages [V]: U12, U23, U31",       7,  12,
                            "8 - Angle UU [°]: phiU1U2, phiU2U3, phiU3U1",  8,  21,
                            "9 - Angle II [°]: phiI3I1, phiI3I1, phiI3I1",  9,  22,
                            "10 - Frequency [Hz]: freq",                    10,  13,
                            "11 - Back",                                    11,  123]                            

# обработчик выбора типа измерения. Список 1-10
def GetCommonMenu_Handler(num, ser):
    print("GetCommonMenu_Handler")
    if num == 11:
        print("\r\nPressed: 11 - Back")
        return
    elif num >= 1 and num <= 10:
        print("Waiting for measured: " + GetCommonMenuItems_mas[num*3]) 
        write_str = "?" + str(GetCommonMenuItems_mas[num*3+2]) + "\r"

        textFromMTE = sendCommandToMTE(ser,write_str,1,1)
    else:
        print("Something go wrong! input num set menu item.")
        return

    #textFromMTE = read_MTE_answer(ser)              #1 считываем строку измерений МТЕ (из виртуального порта)
    
    if num != 10:
        vA = vB = vC = 0
        vA, vB, vC = parse_MTE_answer(textFromMTE)   #2 парсим считанную строку
        print("\r\nValue A: ",str(vA),\
            "Value B: ",str(vB),\
            "Value C: ",str(vC))                     #3 выводим распарсенный результат
    else:
        vFreq = 0
        vFreq = parse_MTE_answer_Freq(textFromMTE)      #2 парсим считанную строку
        print("\r\nFreq is: ",str(vFreq), "  Hz")                      #3 выводим распарсенный результат



def sendCommandToMTE(ser,str_command,printComTo,printComFrom):
    ser.flushInput()
    ser.flushOutput()

    ser.write(str_command.encode())
	
    # выводим в консоль отправленную команду
    if printComTo == 1:					
	    print("send command to MTE: " + str_command)
	    print("Waiting for MTE answer: ") 
    else:
        t=0

    textFromMTE = ser.read(1500)
    textFromMTE = textFromMTE.decode()

    

    # выводим в консоль принятый ответ на команду
    if printComFrom == 1:					
        print("Answer from MTE: " + textFromMTE)
    else:
        t=0

    return textFromMTE






# считать ответ от МТЕ
"""
def read_MTE_answer(ser):
    seq = []
    while True:
        for i in ser.read():                   # Обработка ответа от генератора МТЕ
            seq.append(chr(i))
            joined_seq = ''.join(str(v) for v in seq)  ## Make a string from array
            if chr(i) == '\r':                 # Если принят символ возврата каретки <CR>
                textFromMTE = str(joined_seq)  # принятая из COM1 порта строка (ответ генератора МТЕ)
                print("Line: " + textFromMTE)
                return textFromMTE
"""

def parse_MTE_answer_Freq(textFromMTE):              # парсить ответ от МТЕ по общим параметрам: 3 числа по 3 фазам
    #print("parse_MTE_answer: " + textFromMTE)
    mStr = textFromMTE.split(",")               # Делим строку результата на блоки.
    if mStr[1].startswith("--"): #
        vFreq = 0                  # Нет значения в результатах измерений 
    else:
        lastVal = mStr[1]       # Убираем в конце символ <CR>
        vFreq = float(lastVal[0:len(lastVal)-1:1])     # переводим значение во float

    return vFreq

def parse_MTE_answer(textFromMTE):              # парсить ответ от МТЕ по общим параметрам: 3 числа по 3 фазам
    #print("parse_MTE_answer: " + textFromMTE)
    mStr = textFromMTE.split(",")               # Делим строку результата на блоки.
    if mStr[1].startswith("--"): # фаза А
        vA = 0                  # Нет значения в результатах измерений 
    else:
        vA = float(mStr[1])     # переводим значение во float
    if mStr[2].startswith("--"): # фаза Б
        vB = 0                  # Нет значения в результатах измерений 
    else:
        vB = float(mStr[2])     # переводим значение во float
    if mStr[3].startswith("--"): # фаза C
        vC = 0                  # Нет значения в результатах измерений 
    else:
        lastVal = mStr[3]       # Убираем в конце символ <CR>
        vC = float(lastVal[0:len(lastVal)-1:1])     # переводим значение во float

    return vA, vB, vC
