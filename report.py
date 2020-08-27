import xlwings as xs
import time
import measurement

template_file_name = ".\\Template.xlsx"
template_range = "A1:AJ8"

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

    


def add_to_report():
    pass


if __name__ == '__main__':
    create_test_report(123, None)