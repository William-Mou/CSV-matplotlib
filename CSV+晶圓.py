
# coding: utf-8

import os
import csv
import xlsxwriter
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
    
    out_name=str(file_name[0:16]+'_'+file_namec+'.csv')
    out_file=open(out_name,'w',newline='')
    out_w=csv.writer(out_file)
    out_w.writerows(data_list)
    out_file.close()

    print(out_name)
    
    
    #圖表
    form_dict={'6':'ISB_VDD_1.1x (mA)','8':'ISB_CVDD_1.1x (mA)','10':'ISB_VDDPST_1.1x (mA)','12':'ISB_VDD_bin (mA)','20':'Vccmin(mV)@0.5Mhz','31':'Bin'}
    form_data={}
    first=True
    #讀取並析出資料
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
    file.close()
    
    form_sum={}
    form_av={}
    for each in form_dict:
        form_sum[str(form_data[each])]=[]
        for row in range(1,8):
            for col in range(1,7):
                try:
                    form_sum[str(form_data[each])].append(float(form_data[each][row][col]))
                except:
                    pass
        form_sum[str(form_data[each])].sort()
        form_av[str(form_data[each])]=[float(form_sum[str(form_data[each])][int(len(form_sum[str(form_data[each])])//3)])]
        form_av[str(form_data[each])].append(float(form_sum[str(form_data[each])][int(len(form_sum[str(form_data[each])])//3*2)]))
    form_sum[form_data[each]]=form_data[each][row][col]
    
    #輸出表格
    #worksheet=['ISB_VDD_1.1x (mA)','ISB_CVDD_1.1x (mA)','ISB_VDDPST_1.1x (mA)','ISB_VDD_bin (mA)','Vccmin(mV)@0.5Mhz','Bin']
    worksheet={}
    workbook = xlsxwriter.Workbook(str(file_name[0:16]+'_'+file_namec+'_map.xlsx'))
    for each in form_dict:
        worksheet[each] = workbook.add_worksheet(form_dict[each])
        for row in range(8):
            for col in range(7):
                if row == 0 or col ==0:
                    worksheet[each].write(row,col,form_data[each][row][col])
                elif form_data[each][row][col] =="":
                    pass
                elif float(form_data[each][row][col])>=form_av[str(form_data[each])][1]:
                    
                    ItemStyl = workbook.add_format({'bg_color':'#CC0000',})
                    worksheet[each].write(row,col,form_data[each][row][col],ItemStyl)
                elif float(form_data[each][row][col])>=form_av[str(form_data[each])][0]:
                    ItemStyl = workbook.add_format({'bg_color':'#FFFFFF',})
                    worksheet[each].write(row,col,form_data[each][row][col],ItemStyl)
                elif float(form_data[each][row][col])<form_av[str(form_data[each])][0]:
                    ItemStyl = workbook.add_format({'bg_color':'#00DD00',})
                    worksheet[each].write(row,col,form_data[each][row][col],ItemStyl)
        
        plt.title(str(form_dict[each])+" p-chart") #標題
        plt.xlabel("Value") #x軸標題
        plt.ylabel("Pacent(%)") #y軸標題
        plt.grid(True) #格線
        x=form_sum[str(form_data[each])]
        form_sum_lenp=100/len(form_sum[str(form_data[each])])
        #print(form_sum_lenp)
        y=[i for i in range(int(form_sum_lenp),101,int(form_sum_lenp))]
        #print(y)
        plt.plot(x, y ,marker='o')
        plt.savefig("C:\\Users\\P8H61-ML\\Documents\\晶圓資料處理\\"+file_name[0:16]+'_'+file_namec+'_'+str(form_dict[each])+".jpg", dpi=120)
        #plt.show()
        plt.close()

