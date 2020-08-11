"""
MenuItems for get data from MTE counter
"""


## соберем строки вывода в один массив
GetCommonMenuItems_mas = [  "\r\nChoose common params values:",                     0,  0,
                            "1 - Currents [A]: I1, I2, I3",                         1,  1,
                            "2 - Voltages [V]: U1, U2, U3",                         2,  2,
                            "3 - Phi current absolute [°]: phiU1, phiU2, phiU3",    3,  12,
                            "4 - Phi voltage absolute [°]: phiI1, phiI2, phiI3",    4,  13,
                            "5 - Frequency [Hz]: freq",                             5,  1113,
                            "6 - Back",                                             6,  1123]                            

# обработчик выбора типа измерения. Список 1-10
def GetCommonMenu_Handler(num, ser):
    print("GetCommonMenu_Handler")
    if num == 6:
        print("\r\nPressed: 6 - Back")
        return
    elif num >= 1 and num <= 4:
        print("Waiting for measured: " + GetCommonMenuItems_mas[num*3]) 
        write_str = "?" + str(GetCommonMenuItems_mas[num*3+2]) + ";"

        textFromMTE = sendCommandToMTE(ser,write_str,1,1)

    elif num == 5:
        print("Waiting for measured: FREQ")
        write_str = "FRQ\r"

        textFromMTE = sendCommandToMTE(ser,write_str,1,1)    

    else:
        print("Something go wrong! input num set menu item.")
        return

    #textFromMTE = read_MTE_answer(ser)              #1 считываем строку измерений МТЕ (из виртуального порта)
    
    if num != 5:
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
	    print("send command to MTE counter: " + str_command)
	    print("Waiting for MTE answer: ") 
    else:
        t=0

    textFromMTE = ser.read(1000)
    textFromMTE = textFromMTE.decode()

    # выводим в консоль принятый ответ на команду
    if printComFrom == 1:					
        print("Answer from MTE: " + textFromMTE)
    else:
        t=0

    return textFromMTE


def parse_MTE_answer_Freq(textFromMTE):             

    mStr = textFromMTE.split("=")               # Делим строку результата на блоки.
    if mStr[1].startswith("--"): #
        vFreq = 0                  # Нет значения в результатах измерений 
    else:
        lastVal = mStr[1]       # Убираем в конце символ <CR>
        vFreq = float(lastVal[0:len(lastVal)-1:1])     # переводим значение во float

    return vFreq

def parse_MTE_answer(textFromMTE):              # парсить ответ от МТЕ по общим параметрам: 3 числа по 3 фазам
    #print("parse_MTE_answer: " + textFromMTE)
    mStr = textFromMTE.split(",")               # Делим строку результата на блоки.
    if mStr[1].startswith("-"): # фаза А
        vA = 0                  # Нет значения в результатах измерений 
    else:
        vA = float(mStr[1])     # переводим значение во float
    if mStr[2].startswith("-"): # фаза Б
        vB = 0                  # Нет значения в результатах измерений 
    else:
        vB = float(mStr[2])     # переводим значение во float
    if mStr[3].startswith("-"): # фаза C
        vC = 0                  # Нет значения в результатах измерений 
    else:
        lastVal = mStr[3]       # Убираем в конце символ <CR>
        vC = float(lastVal[0:len(lastVal)-1:1])     # переводим значение во float

    return vA, vB, vC
