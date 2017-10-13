import os
import csv
import matplotlib.pyplot as plt

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