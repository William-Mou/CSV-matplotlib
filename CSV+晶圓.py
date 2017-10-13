import os
import csv
import matplotlib.pyplot as plt

def form(name):
    n=str(name)
    name=[]
    for i in range(8):
        name.append([])
        for j in range(7):
            if i==0 and j==0:
                name[i].append(n)
            elif i==0:
                name[i].append(j-3)
            elif j==0:
                name[i].append(7-i)
            else:
                name[i].append('')

    return name

header = ['Lot ID', 'PKG ID', 'X', 'Y', 'VDD(V)', 'VDDPST(V)','ISB_VDD_1.1x (mA)', 'ISB_VDD_1.0x (mA)', 'ISB_CVDD_1.1x (mA)', 'ISB_CVDD_1.0x (mA)',  'ISB_VDDPST_1.1x (mA)', 'ISB_VDDPST_1.0x (mA)','ISB_VDD_bin (mA)','ICC_VDD_1.1x', 'ICC_VDD_1.0x', 'ICC_CVDD_1.1x', 'ICC_CVDD_1.0x',  'ICC_VDDPST_1.1x', 'ICC_VDDPST_1.0x','Vccmin(mV)@5Mhz','Vccmin(mV)@0.5Mhz','Vccmin_CVDD=1.44V','Vccmax_CVDD=1.44V','Vccmin_CVDD=1.53V','Vccmax_CVDD=1.53V','Vccmin_CVDD=1.8V','Vccmax_CVDD=1.8V','Vccmin_CVDD=2.0V','Vccmax_CVDD=2.0V','VSDR(mV)','VDDP(mV)','Bin']
cwd = os.path.abspath('.')
files_name = []
for f in os.listdir('.'):
    if os.path.isfile(f) and '.txt' in f:
        files_name.append(f)
for file_name in files_name:
    first=True
    data_list=[]
    data_dict={}
    data_list.append(header)   
    
    file=open(file_name,'r')
    for data_str in file:
        data_row=data_str.split()
        if 5<len(data_row)<32 or len(data_row)==0:
            continue
        elif len(data_row)==5:
            for i in range(27):
                data_row.insert(4,"")
            data_dict[(data_row[2],data_row[3])]=data_row
        else:
            if first:
                if float(data_row[12])<0.01:
                    file_namec='N40C'
                elif 0.01<float(data_row[12])<0.1:
                    file_namec='25C'
                elif 0.1<float(data_row[12])<1:
                    file_namec='85C'    
                elif 1<float(data_row[12]):
                    file_namec='125C'
                first=False
            data_dict[(data_row[2],data_row[3])]=data_row

    for each in data_dict:
        data_list.append(data_dict[each])
    
    out_name=str(file_name[0:17]+'_'+file_namec+'.csv')
    out_file=open(out_name,'w',newline='')
    out_w=csv.writer(out_file)
    out_w.writerows(data_list)
    out_file.close()

    print(out_name)
    
    
    #圖表
    cols=[6,8,10,12]
    form_dict={'6':'ISB_VDD_1.1x (mA)','8':'ISB_CVDD_1.1x (mA)','10':'ISB_VDDPST_1.1x (mA)','12':'ISB_VDD_bin (mA)','20':'Vccmin(mV)@0.5Mhz','31':'Bin'}
    form_data={}
    first=True
    
    file=open(out_name,'r')
    for row in csv.reader(file):
        for each in form_dict:
            if first:
                first=False
                break
            if each in form_data:
                pass
            else:
                form_data[each]=form(form_dict[each])
            form_data[each][int(row[2])+3][7-int(row[3])]=row[int(each)]
