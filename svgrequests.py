'''
Create SVG requestst to binom for read data
First  stage: ping Binom on line
Second stage: ask channel names and create dict {ip_addr_1: {UID_1: name, UID_2: name, ...}, ip_addr_2: {UID_1: name, UID_2: name, ...}}
Third  stage: ask all binoms 
'''
import requests
import struct
import time
import os

prot = "http://"
ip_addr = "192.168.99.235"

# may be we don't need this feature
variable_names = ("P", "Ua", "Ub", "Uc", "AngUab", "AngUbc", "AngUca", "Uab", "Ubc", "Uca", "Ia", "Ib", "Ic", "AngIab", "AngIbc", "AngIca", "AngSym1")


UID_DBnames_mapping = dict()
DBNames_value_mapping = dict()

def create_request_string(req):
    return prot + ip_addr + "/" + req


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def connect_binom():
    '''
    connect_binom - connects to binom through http protocol return session obj
    '''
    login = {"login" : "root", "password" : "root"}
    s = requests.Session()
    request_str = 'http://' + ip_addr + '/~login'
    print("Try login to Binom3 " + request_str)
    req = s.post(request_str, params=login)
    print("Status code: " + str(req.status_code))
    return s



def ActionsHandler():

    #debug peace of code


    binom_session = connect_binom()
    menu_items = ("1 - send GET request","2 - ~svginfo?name=db:PSI_data" ,
                  "3 - open data", "4 - close data","5 - exit")
    work = True
    while work:
        print(*menu_items,sep='\n')
        try:
            usr_inp = int(input())
        except ValueError as ve:
            print("input number")
            continue
        if usr_inp == 1:
            print("input request")
            req = input()
            r = binom_session.get(create_request_string(req))
            print("Response len = ", len(r.content))
            txt_content = r.content.decode("utf-8").split(";")
            print("\n".join(txt_content))
        elif usr_inp == 2:
            req = "~svginfo?name=db:PSI_data"
            print("Send request: " + req)
            r = binom_session.get(create_request_string(req))
            print("Response")
            txt_content = r.content.decode("utf-8").split(";")
            print("\n".join(txt_content))
        elif usr_inp == 3:
             # ask channel output names
            UID_DBnames_mapping.update(ask_channel_out_names(binom_session))
            print(UID_DBnames_mapping)

            if len(UID_DBnames_mapping) == 0: 
                print("Can't read names from channel output")                
                continue

            code, content, len_content = read_binom_data(binom_session, True)  # open channel for read
            if code == 200:
                for _ in range(0, 10):
                    code, content, len_content = read_binom_data(binom_session)  # read channel events
                    if code == 200:
                        parce_answer_fr_binom(content)
                    elif code == 204:
                        print("no data")
                    else:
                        print("err occur")
                    time.sleep(5)
                close_binom_data(binom_session)
            else:
                print("Can't open svg channel check parametrization")
                
        elif usr_inp == 4:
            pass
        elif usr_inp == 5:
            work = False

    print("Program complete")

def ask_channel_out_names(binom_sess):
    '''
    ask svg channel out and return dict {UID_1: nameDB, UID_2: nameDB}
    '''
    req = "~svginfo?name=db:PSI_data"
    print("Send request: " + req) 
    r = binom_sess.get(create_request_string(req))
    cells_names = r.content.decode("utf-8").split(";")  # format: 000000000, name, BLOB.MINMAX
    res = dict()
    for el in cells_names:
        record = el.split(",")
        if len(record) > 2:
            res[int(record[0])] = record[1]
    return res
        



def read_binom_data(binom_sess, open=False):
    print("Request current time")
    request = "~time"
    r = binom_sess.get(create_request_string(request))
    time = r.content.decode("utf-8")
    print("time: " + time)
    request = "~svgdata?name=db:PSI_data" if open else "~svgevent?name=db:PSI_data"
    print("Send request: " + request)
    r = binom_sess.get(create_request_string(request))
    print("Status code: ", r.status_code)
    print("Read data len ", len(r.content))
    return r.status_code, r.content, len(r.content)


def close_binom_data(binom_sess):
    print("close svg channel")
    request = "svgclose?name=db:Ua"
    print("Send request: " + request)
    r = binom_sess.get(create_request_string(request))
    print("Status code: ", r.status_code)
    print(r.content)
    


def parce_answer_fr_binom(binom_answer):
    '''
    parce answer with event from binom
    binom_answer - binary data received from binom
    uid_dict - UID: name dictionary
    '''
    offset_UID = 4
    offset_average_data = 64 + 8
    global DBNames_value_mapping 
    for _ in range(0, len(variable_names)):
        uid = struct.unpack_from("I", binom_answer, offset_UID)[0]   # get uid from binom data
        value = struct.unpack_from("f", binom_answer, offset_average_data)[0]  # get average value data
        name_cell = UID_DBnames_mapping.get(uid, None)
        if name_cell is not None:
            DBNames_value_mapping[name_cell] = value
        else:
            raise Exception("Received undefined UID " + str(uid))
        
        offset_average_data += 128
        offset_UID  += 128
    
    for name, value in DBNames_value_mapping.items():
        print("{:^10s}".format(name), "=", value)

if __name__ == "__main__":
   # parce_answer_fr_binom(rcv_binary_str)  # it's only for debug
    ActionsHandler()