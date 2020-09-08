import xlwings as xs
import time
import measurement

template_file_name = ".\\Template.xlsx"
head_range = "A1:AJ1"
result_range = "A2:AJ13"

cur_col_output = "A2"


'''
import xlwings as xw

wb = xw.Book('mybook.xlxs')
sht = wb.sheets['Sheet1']
sht2 = wb.sheets['Sheet2']

sht.range('A1:A6').api.copy
sht2.range("A1").api.select
sht2.api.paste

wb.app.api.CutCopyMode=False
'''

# class 

"""
def create_test_report(num_point, signal_fr_csv):
    '''

    '''
    result_file = '.\\Reports\\Report_' + time.strftime("%Y_%m_%d:%H:%M:%S",time.localtime()) + ".xlsx"
    wb_template = xs.Book(template_file_name)
    
    wb = xs.Book()
    # copy template to new excel 
    # wb_template.sheets["Template"].Range(template_range).copy(wb.sheets["Result"].range(template_range))
    wb_template.sheets["Template"]

    '''
    Todo: 
    1 write copy header 
    2 write set values (from csv)
    3 wrute MTE meas values with ()
    '''


    wb.save(result_file) 
"""

def copy_head_fr_template(wb_src, wb_dest):
    src_sh = wb_src.sheets['Template']
    dst_sh = wb_dest.sheets[0]

    src_sh.range(head_range).api.copy
    dst_sh.range("A1").api.select
    dst_sh.api.paste

def copy_result_field_fr_template(wb_src, wb_dest):
    src_sh = wb_src.sheets['Template']
    dst_sh = wb_dest.sheets[0]

    src_sh.range(result_range).api.copy
    dst_sh.range(cur_col_output).api.select
    dst_sh.api.paste

def next_output_cell(wb_result):
    cur_range = wb_result.sheets[0].range(cur_col_output).offset(12, 0)
    cur_col_output = cur_range.address().replace("$", "")

    


    
def write_etalon_result(wb_result, cur_pnt):
    etalon = measurement.measurement_storage.get_etalon_signal(cur_pnt)
    cur_range = wb_result.sheets[0].range(cur_col_output).offset(0, 1)
    cur_range.value = cur_pnt
    cur_range = cur_range.offset(0, 1)
    cur_range.value = list(etalon.meas_result.results.values())


def set_mte_result(wb_result, cur_pnt):
#    mte = measurement.measurement_storage.get_etalon_signal(cur_pnt)
#    cur_range = wb_result.sheets[0].range(cur_col_output)
#    cur_range.value = cur_pnt
#    cur_range = cur_range.offset(0, 1)
#    cur_range.value = list(etalon.meas_result.results.values())
    pass

def write_binom_result(wb_result, cur_pnt):
    binom_result = measurement.measurement_storage.get_binom_signal(cur_pnt)
    cur_range = wb_result.sheets[0].range(cur_col_output).offset(7, 1)
    cur_range.value = cur_pnt
    cur_range = cur_range.offset(0, 1)
    cur_range.value = list(binom_result.results.values())
    # write error
    

    
def generate_report(st_pnt, end_pnt):
    # 1. copy head from template
    # 2. copy result from csv file and MTE counter
    
    # 3. copy results part for Binom
    # 4. copy results
    res_excel_file =  '.\\Reports\\Report_' + time.strftime("%Y_%m_%d:%H:%M:%S",time.localtime()) + ".xlsx"
    
    # excel_app = xs.App(visible=False)  #uncomment if visible not desired
    wb_template = xs.Book(template_file_name)
    wb_result = xs.Book()
    copy_head_fr_template(wb_template, wb_result)
    #-------------------------------------------------
    cur_pnt = st_pnt
    while cur_pnt <= end_pnt:
        measurement.measurement_storage.calc_error(cur_pnt)
        copy_result_field_fr_template(wb_template, wb_result)

        write_etalon_result(wb_result, cur_pnt)
        # write mte result
        write_binom_result(wb_result, cur_pnt)


        next_output_cell(wb_result)
        cur_pnt += 1
    #-------------------------------------------------
    wb_result.save(res_excel_file)
    pass


if __name__ == '__main__':
    pass