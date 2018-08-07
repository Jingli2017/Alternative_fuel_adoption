import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

df = pd.read_excel('C:/Users/jing_li/Desktop/Alternative_pathway.xlsx', sheet_name="Frame")
other_con_2030 = 55259800  # Ton LSFO
other_con_2050 = 55259800  # Ton LSFO
other_num = 15267
CAPEX_ICE = 700  # from published paper
dis_2030 = 0.75  # LNG equipment 75% discount in 2030
dis_LNG_2050 = 0.75  # LNG equipment 75% discount in 2030
dis_H2_2050 = 0.4  # H2 equipment cut down to 30%
dis_Me_2050 = 0.75  # bio_me equipment cut down 50%
carprice = 1.1  # carbon price 20% MBM
df['2030_price_LSFO_($/ton)'] = 716  # Robin Meech 2030
df['2030_price_LNG_($/ton)'] = 548  # Global
df['2030_price_Biodiesel_($/ton)'] = 1163  # from IEA advanced
df['2030_price_Methanol_($/ton)'] = 451  # from IHS data or from online article
df['2030_price_Hydrogen_($/ton)'] = 242*3  # 3 times of LNG price

df['2050_price_LSFO_($/ton)'] = 600  # DNV GL MGO price
LSFO_2050_price = 600
df['2050_price_LNG_($/ton)'] = 548  # IEEJ USA
df['2050_price_Biodiesel_($/ton)'] = 615  # same as LSFO
df['2050_price_Methanol_($/ton)'] = 429*0.75 # calculated from online article
df['2050_price_Hydrogen_($/ton)'] = 242*3*0.25  # lower to 25 percent of fuel price.

df['NPV_LNG_2030'] = (df['consumption_LSFO_(tonnes)']*df['2030_price_LSFO_($/ton)']-df['consumption_LNG_(tonnes)']
                 *df['2030_price_LNG_($/ton)'])*df['payback_5']-(df['CAPEX_LNG_($/KW)']*dis_2030-CAPEX_ICE)*df['Installed_Power_(KW)']

df['NPV_Me_2030'] = (df['consumption_LSFO_(tonnes)']*df['2030_price_LSFO_($/ton)']-df['consumption_Methanol_(tonnes)']
                 *df['2030_price_Methanol_($/ton)'])*df['payback_5']-(df['CAPEX_Methanol_($/KW)']*dis_2030-CAPEX_ICE)*df['Installed_Power_(KW)']

df['NPV_Bd_2030'] = (df['consumption_LSFO_(tonnes)']*df['2030_price_LSFO_($/ton)']-df['consumption_Biodiesel_(tonnes)']
                 *df['2030_price_Biodiesel_($/ton)'])*df['payback_5']-(CAPEX_ICE*0.05)*df['Installed_Power_(KW)']

df['NPV_H2_2030'] = (df['consumption_LSFO_(tonnes)']*df['2030_price_LSFO_($/ton)']-df['consumption_Hydrogen_(tonnes)']
                 *df['2030_price_Hydrogen_($/ton)'])*df['payback_5']-(df['CAPEX_Hydrogen_($/KW)']*dis_2030-CAPEX_ICE)*df['Installed_Power_(KW)']

# Selection the largest NPV value as alternative fuel
conditions = [
    (df['NPV_LNG_2030'] > df['NPV_Me_2030']) & (df['NPV_LNG_2030'] > df['NPV_Bd_2030'])& (df['NPV_LNG_2030'] > df['NPV_H2_2030']),
    (df['NPV_Me_2030'] > df['NPV_LNG_2030']) & (df['NPV_Me_2030'] > df['NPV_Bd_2030'])& (df['NPV_Me_2030'] > df['NPV_H2_2030']),
    (df['NPV_Bd_2030'] > df['NPV_LNG_2030']) & (df['NPV_Bd_2030'] > df['NPV_Me_2030'])& (df['NPV_Bd_2030'] > df['NPV_H2_2030']),
    (df['NPV_H2_2030'] > df['NPV_LNG_2030']) & (df['NPV_H2_2030'] > df['NPV_Me_2030'])& (df['NPV_H2_2030'] > df['NPV_Bd_2030'])]
choices_2030 = ['LNG', 'Methanol', 'Biodiesel', 'Hydrogen']
df['Selection_2030'] = np.select(conditions, choices_2030)

df['NPV_2030'] = df[['NPV_LNG_2030', 'NPV_Me_2030', 'NPV_Bd_2030', 'NPV_H2_2030']].max(axis=1)
df.loc[df.NPV_2030 <= 0, 'Selection_2030'] = 'LSFO'
print(df[['Ship_type', 'Size_category', 'Selection_2030']])
# Ship numbers
num_LSFO_2030 = df['Ship_2030'][df['Selection_2030'] == 'LSFO'].sum()+df['Ship_2030_ex'].sum()+15267
num_LNG_2030 = df['Ship_2030'][df['Selection_2030'] == 'LNG'].sum()
num_Me_2030 = df['Ship_2030'][df['Selection_2030'] == 'Methanol'].sum()
num_Bd_2030 = df['Ship_2030'][df['Selection_2030'] == 'Biodiesel'].sum()
num_Hydrogen_2030 = df['Ship_2030'][df['Selection_2030'] == 'Hydrogen'].sum()
num_sum_2030 = num_LSFO_2030 + num_LNG_2030 + num_Me_2030 + num_Bd_2030 + num_Hydrogen_2030

# Fuel consumption
con_LSFO_2030 = (df['Ship_2030']*df['consumption_LSFO_(tonnes)'])[df['Selection_2030'] == 'LSFO'].sum()\
                +(df['Ship_2030_ex']*df['consumption_LSFO_(tonnes)']).sum()+ other_con_2030
con_LNG_2030 = (df['Ship_2030']*df['consumption_LNG_(tonnes)'])[df['Selection_2030'] == 'LNG'].sum()
con_Me_2030 = (df['Ship_2030']*df['consumption_Methanol_(tonnes)'])[df['Selection_2030'] == 'Methanol'].sum()
con_Bd_2030 = (df['Ship_2030']*df['consumption_Biodiesel_(tonnes)'])[df['Selection_2030'] == 'Biodiesel'].sum()
con_H2_2030 = (df['Ship_2030']*df['consumption_Hydrogen_(tonnes)'])[df['Selection_2030'] == 'Hydrogen'].sum()
con_sum_2030 = con_LSFO_2030+con_LNG_2030+con_Me_2030+con_Bd_2030+con_H2_2030
con_LSFO_2016 = (df['Ship_2030']*df['consumption_HFO_(tonnes)']).sum() +\
                (df['Ship_2030_ex']*df['consumption_HFO_(tonnes)']).sum()

energy_LSFO_2030 = con_LSFO_2030*1000*40.5*10**-12  # 40.5 MJ/kg unit PJ
energy_LNG_2030 = con_LNG_2030*1000*48.6*10**-12  # 48.6 MJ/kg unit PJ
main_output_2030 = (con_LSFO_2030/(179*10**-6)+con_LNG_2030/(150*10**-6))/2.777778*10**-11  # output unit EJ
print('Energy consumption 2030 ', energy_LSFO_2030+energy_LNG_2030)
print('Energy main engine output 2030', main_output_2030)
# CO2 emission
emi_LSFO_2030 = (df['Ship_2030']*df['consumption_LSFO_(tonnes)']*3.114)[df['Selection_2030'] == 'LSFO'].sum() + \
                (df['Ship_2030_ex']*df['consumption_LSFO_(tonnes)']*3.114).sum() + other_con_2030*3.114
emi_LNG_2030 = (df['Ship_2030']*df['consumption_LNG_(tonnes)']*2.750)[df['Selection_2030'] == 'LNG'].sum()
emi_Me_2030 = (df['Ship_2030']*df['consumption_Methanol_(tonnes)']*1.370)[df['Selection_2030'] == 'Methanol'].sum()
emi_Bd_2030 = (df['Ship_2030']*df['consumption_Biodiesel_(tonnes)']*0)[df['Selection_2030'] == 'Biodiesel'].sum()
emi_H2_2030 = (df['Ship_2030']*df['consumption_Hydrogen_(tonnes)']*0)[df['Selection_2030'] == 'Hydrogen'].sum()
emi_sum_2030 = emi_LSFO_2030+emi_LNG_2030+emi_Me_2030+emi_Bd_2030+emi_H2_2030

########################################################################################################################
########################################################################################################################

df['NPV_LNG_2050'] = (df['consumption_LSFO_(tonnes)']*df['2050_price_LSFO_($/ton)']*carprice-df['consumption_LNG_(tonnes)']
                 *df['2050_price_LNG_($/ton)'])*df['payback_5']-(df['CAPEX_LNG_($/KW)']*dis_LNG_2050-CAPEX_ICE)*df['Installed_Power_(KW)']

df['NPV_Me_2050'] = (df['consumption_LSFO_(tonnes)']*df['2050_price_LSFO_($/ton)']*carprice-df['consumption_Methanol_(tonnes)']
                 *df['2050_price_Methanol_($/ton)'])*df['payback_5']-(df['CAPEX_Methanol_($/KW)']*dis_Me_2050-CAPEX_ICE)*df['Installed_Power_(KW)']

df['NPV_Bd_2050'] = (df['consumption_LSFO_(tonnes)']*df['2050_price_LSFO_($/ton)']*carprice-df['consumption_Biodiesel_(tonnes)']
                 *df['2050_price_Biodiesel_($/ton)'])*df['payback_5']-(CAPEX_ICE*0.05)*df['Installed_Power_(KW)']

df['NPV_H2_2050'] = (df['consumption_LSFO_(tonnes)']*df['2050_price_LSFO_($/ton)']*carprice-df['consumption_Hydrogen_(tonnes)']
                 *df['2050_price_Hydrogen_($/ton)'])*df['payback_5']-(df['CAPEX_Hydrogen_($/KW)']*dis_H2_2050-CAPEX_ICE)*df['Installed_Power_(KW)']

# Selection the largest NPV value as alternative fuel
conditions = [
    (df['NPV_LNG_2050'] > df['NPV_Me_2050']) & (df['NPV_LNG_2050'] > df['NPV_Bd_2050'])& (df['NPV_LNG_2050'] > df['NPV_H2_2050']),
    (df['NPV_Me_2050'] > df['NPV_LNG_2050']) & (df['NPV_Me_2050'] > df['NPV_Bd_2050'])& (df['NPV_Me_2050'] > df['NPV_H2_2050']),
    (df['NPV_Bd_2050'] > df['NPV_LNG_2050']) & (df['NPV_Bd_2050'] > df['NPV_Me_2050'])& (df['NPV_Bd_2050'] > df['NPV_H2_2050']),
    (df['NPV_H2_2050'] > df['NPV_LNG_2050']) & (df['NPV_H2_2050'] > df['NPV_Me_2050'])& (df['NPV_H2_2050'] > df['NPV_Bd_2050'])]
choices_2050 = ['LNG', 'Methanol', 'Biodiesel', 'Hydrogen']
df['Selection_2050'] = np.select(conditions, choices_2050)

df['NPV_2050'] = df[['NPV_LNG_2050', 'NPV_Me_2050', 'NPV_Bd_2050', 'NPV_H2_2050']].max(axis=1)
df.loc[df.NPV_2050 <= 0, 'Selection_2050'] = 'LSFO'
# df = df.sort_values('Selection_2050')
# print(df[['Ship_type', 'Size_category', 'Selection_2050']])

# Ship numbers
num_LSFO_2050 = df['Ship_2050'][df['Selection_2050'] == 'LSFO'].sum()+other_num
num_LNG_2050 = df['Ship_2050'][df['Selection_2050'] == 'LNG'].sum()
num_Me_2050 = df['Ship_2050'][df['Selection_2050'] == 'Methanol'].sum()
num_Bd_2050 = df['Ship_2050'][df['Selection_2050'] == 'Biodiesel'].sum()
num_Hydrogen_2050 = df['Ship_2050'][df['Selection_2050'] == 'Hydrogen'].sum()
num_sum_2050 = num_LSFO_2050 + num_LNG_2050 + num_Me_2050 + num_Bd_2050 + num_Hydrogen_2050

# Fuel consumption
con_LSFO_2050 = (df['Ship_2050']*df['consumption_LSFO_(tonnes)'])[df['Selection_2050'] == 'LSFO'].sum()+ other_con_2050
con_LNG_2050 = (df['Ship_2050']*df['consumption_LNG_(tonnes)'])[df['Selection_2050'] == 'LNG'].sum()
con_Me_2050 = (df['Ship_2050']*df['consumption_Methanol_(tonnes)'])[df['Selection_2050'] == 'Methanol'].sum()
con_Bd_2050 = (df['Ship_2050']*df['consumption_Biodiesel_(tonnes)'])[df['Selection_2050'] == 'Biodiesel'].sum()
con_H2_2050 = (df['Ship_2050']*df['consumption_Hydrogen_(tonnes)'])[df['Selection_2050'] == 'Hydrogen'].sum()
con_sum_2050 = con_LSFO_2050+con_LNG_2050+con_Me_2050+con_Bd_2050+con_H2_2050

def main_engine_output(fuel_con, SFOC):
    main_engine_output = fuel_con/(SFOC*10**-6)/2.777778*10**-11
    return main_engine_output

main_LSFO_2050 = main_engine_output(con_LSFO_2050, 179)
main_LNG_2050 = main_engine_output(con_LNG_2050, 150)
main_Me_2050 = main_engine_output(con_Me_2050, 381)
main_Bd_2050 = main_engine_output(con_Bd_2050, 187)
main_H2_2050 = main_engine_output(con_H2_2050, 57)
main_sum_2050 = main_LSFO_2050+main_Bd_2050+main_LNG_2050+main_Me_2050+main_H2_2050

energy_LSFO_2050 = con_LSFO_2050*1000*40.5*10**-12  # 40.5 MJ/kg unit PJ
energy_LNG_2050 = con_LNG_2050*1000*48.6*10**-12  # 48.6 MJ/kg unit PJ
energy_Me_2050 = con_Me_2050*1000*20.0*10**-12  # 20.0 MJ/kg unit PJ
energy_Bd_2050 = con_Bd_2050*1000*37.9*10**-12  # 37.9 MJ/kg unit PJ
energy_H2_2050 = con_H2_2050*1000*120.0*10**-12  # 120.0 MJ/kg unit PJ
energy_sum_2050 = energy_LSFO_2050+energy_LNG_2050+energy_Me_2050+energy_Bd_2050+energy_H2_2050

print('Energy consumption 2050 ', energy_sum_2050)
print('Energy main engine output 2050', main_sum_2050)

# CO2 emission
emi_LSFO_2050 = (df['Ship_2050']*df['consumption_LSFO_(tonnes)']*3.206)[df['Selection_2050'] == 'LSFO'].sum()+ other_con_2050*3.206
emi_LNG_2050 = (df['Ship_2050']*df['consumption_LNG_(tonnes)']*2.750)[df['Selection_2050'] == 'LNG'].sum()
emi_Me_2050 = (df['Ship_2050']*df['consumption_Methanol_(tonnes)']*1.370)[df['Selection_2050'] == 'Methanol'].sum()
emi_Bd_2050 = (df['Ship_2050']*df['consumption_Biodiesel_(tonnes)']*3.114*0.2)[df['Selection_2050'] == 'Biodiesel'].sum()
emi_H2_2050 = (df['Ship_2050']*df['consumption_Hydrogen_(tonnes)']*0)[df['Selection_2050'] == 'Hydrogen'].sum()
emi_sum_2050 = emi_LSFO_2050+emi_LNG_2050+emi_Me_2050+emi_Bd_2050+emi_H2_2050
print('emission in 2030  '+"%.0f" % round(emi_sum_2030*10**-6, 0))
print('emission in 2050  '+"%.0f" % round(emi_sum_2050*10**-6, 0))

# offset calculation
offset = con_LSFO_2050*LSFO_2050_price*0.1*0.15/10.23  # unit ton offset price 10.23 $/ton
print('emission in 2050 with offset  '+"%.0f" % round((emi_sum_2050-offset)*10**-6, 0))
# Plot section
# figure style setting
mpl.rcParams['legend.fancybox'] = False
mpl.rcParams['legend.loc'] = 'upper right'
mpl.rcParams['legend.numpoints'] = 2
mpl.rcParams['legend.fontsize'] = 14
mpl.rcParams['legend.framealpha'] = None
mpl.rcParams['legend.scatterpoints'] = 3
mpl.rcParams['legend.edgecolor'] = 'inherit'
mpl.rcParams['patch.force_edgecolor'] = True
mpl.rc('ytick', labelsize=14)
mpl.rc('xtick', labelsize=14)
colors = plt.cm.get_cmap("Set2", 6)

ship_num_2030 = [num_LSFO_2030, num_LNG_2030, num_Me_2030, num_Bd_2030, num_Hydrogen_2030, num_sum_2030]
fuel_type = ['LSFO', 'LNG', 'Methanol', 'Biodiesel', 'Hydrogen', 'Total']
# Plot
fig = plt.figure()
ax1 = plt.subplot(321)
fig.set_size_inches(20, 15)

width = 0.5
p1 = ax1.bar(fuel_type, ship_num_2030, width, color=colors(0))
for i in range(6):
    p1[i].set_color(colors(i))
    p1[i].set_edgecolor('black')

con_2030 = [con_LSFO_2030, con_LNG_2030, con_Me_2030, con_Bd_2030, con_H2_2030, con_sum_2030]
con_2030 = np.asarray(con_2030)*10**-6
fuel_type = ['LSFO', 'LNG', 'Methanol', 'Biodiesel', 'Hydrogen', 'Total']
ax1.set_ylim(0, 35000)

# Plot
ax2 = plt.subplot(323)
width = 0.5
p1 = ax2.bar(fuel_type, con_2030, width, color=colors(0))
for i in range(6):
    p1[i].set_color(colors(i))
    p1[i].set_edgecolor('black')

emi_2030 = [emi_LSFO_2030, emi_LNG_2030, emi_Me_2030, emi_Bd_2030, emi_H2_2030, emi_sum_2030]
emi_2030 = np.asarray(emi_2030)*10**-6

fuel_type = ['LSFO', 'LNG', 'Methanol', 'Biodiesel', 'Hydrogen', 'Total']
# Plot
ax3 = plt.subplot(325)
width = 0.5
p1 = ax3.bar(fuel_type, emi_2030, width, color=colors(0))
for i in range(6):
    p1[i].set_color(colors(i))
    p1[i].set_edgecolor('black')

# 2050
ship_num_2050 = [num_LSFO_2050, num_LNG_2050, num_Me_2050, num_Bd_2050, num_Hydrogen_2050, num_sum_2050]
fuel_type = ['MGO', 'LNG', 'Methanol', 'Biodiesel', 'Hydrogen', 'Total']
ax4 = plt.subplot(322)
ax4.set_ylim(0, 35000)
p1 = ax4.bar(fuel_type, ship_num_2050, width, color=colors(0))
for i in range(6):
    p1[i].set_color(colors(i))
    p1[i].set_edgecolor('black')

con_2050 = [con_LSFO_2050, con_LNG_2050, con_Me_2050, con_Bd_2050, con_H2_2050, con_sum_2050]
con_2050 = np.asarray(con_2050)*10**-6
fuel_type = ['MGO', 'LNG', 'Methanol', 'Biodiesel', 'Hydrogen', 'Total']
# Plot
ax5 = plt.subplot(324)
width = 0.5
p1 = ax5.bar(fuel_type, con_2050, width, color=colors(0))
for i in range(6):
    p1[i].set_color(colors(i))
    p1[i].set_edgecolor('black')

emi_2050 = [emi_LSFO_2050, emi_LNG_2050, emi_Me_2050, emi_Bd_2050, emi_H2_2050, emi_sum_2050-offset]
emi_2050 = np.asarray(emi_2050)*10**-6
fuel_type = ['MGO', 'LNG', 'Methanol', 'Biodiesel', 'Hydrogen', 'Total']
Offset = [0, 0, 0, 0, 0, offset]
Offset = np.asarray(Offset)*10**-6
# Plot
ax6 = plt.subplot(326)
width = 0.5
p1 = ax6.bar(fuel_type, emi_2050, width, color=colors(0))
p2 = ax6.bar(fuel_type, Offset, width, bottom = emi_2050, color='black', label='offset')
for i in range(6):
    p1[i].set_color(colors(i))
    p1[i].set_edgecolor('black')
for i in range(6):
    p2[i].set_color('black')
    p2[i].set_edgecolor('black')
# Plot settings
ax1.yaxis.grid(linestyle='dotted')
ax2.yaxis.grid(linestyle='dotted')
ax3.yaxis.grid(linestyle='dotted')
ax4.yaxis.grid(linestyle='dotted')
ax5.yaxis.grid(linestyle='dotted')
ax6.yaxis.grid(linestyle='dotted')
ax1.set_ylim(0, 50000)
ax4.set_ylim(0, 50000)
ax2.set_ylim(0, 350)
ax5.set_ylim(0, 350)
ax3.set_ylim(0, 820)
ax6.set_ylim(0, 820)
ax6.legend(loc = 'upper left')
ax1.set_ylabel('Ship number', fontsize=14)
ax2.set_ylabel('Fuel consumption (MT)', fontsize=14)
ax3.set_ylabel('CO2 emission (MT)', fontsize=14)
# ax4.get_yaxis().set_ticks([])
plt.tight_layout()
plt.subplots_adjust(left=0.11, bottom=None, right=None, top=None, wspace=None, hspace=0.25)
ax1.yaxis.set_label_coords(-0.15, 0.5)
ax2.yaxis.set_label_coords(-0.15, 0.5)
ax3.yaxis.set_label_coords(-0.15, 0.5)
# fig.savefig("C:/Users/jing_li/Desktop/CO2_i.jpg", dpi =900)

# Energy_2016 = (3.08, 4.71, 0.52, 1.76, 1.39)
# Energy_2030 = (2.83, 0.17, 0.00, 0.00, 0.00)
# Energy_2050 = (1.54, 0.77, 1.18, 1.44, 0.03)
#
# fig_a = plt.figure()
# ax1 = plt.subplot(111)
# fig_a.set_size_inches(20, 12)
#
# x = np.arange(len(Energy_2016))
# ax1.bar(x-0.2, Energy_2016, width=0.2,color='b', align='center', label='Current fuel production')
# ax1.bar(x, Energy_2030, width=0.2, color='g', align='center', label='2030 fuel demand')
# ax1.bar(x+0.2, Energy_2050,width=0.2, color='r', align='center', label='2050 fuel demand')
# ax1.set_xticks(x)
# ax1.set_xticklabels(('HFO/MGO', 'LNG', 'Methanol', 'Biodiesel', 'Hydrogen'), fontsize = 20)
# ax1.set_ylabel("Energy supply or demand (PJ)", fontsize = 20)
# ax1.legend(fontsize = 20)
# ax1.set_title("Current worldwide fuel production and future fuel demand", fontsize = 20)
# ax1.yaxis.grid(linestyle='dotted')
# fig_a.savefig("C:/Users/jing_li/Desktop/CO2_i.jpg", dpi=900)
plt.show()