import time ## Delays
import numpy as np
import matplotlib.pyplot as plt

print("HEY")



OX = []
OY = []

fecha = time.strftime('09-05-2017')

with open ('Data/'+str(fecha)+'.txt', 'rt') as in_file:
    for line in in_file:
        tab = line.split()
        var1=tab[2].split(":")
        seg=int(var1[0])*3600+int(var1[1])*60+int(var1[2])-28800
        OY.append(int(tab[3]))
        OX.append(seg)
                          
##fig, ax = plt.subplots()

plt.figure(figsize=( 16,9), dpi=100)

plt.scatter(OX,OY)

#plt.figure(figsize=(7.195,3.841), dpi=100)

plt.xlabel('Hora')
plt.ylabel('Cantidad de alumnos')
plt.title('Cantidad de alumnos ' + fecha)

plt.xticks([w*3600 for w in range(17)], 
  ["8:00 am","9:00 am","10:00 am","11:00 am","12:00 mm","1:00 pm","2:00 pm","3:00 pm","4:00 pm","5:00 pm","6:00 pm","7:00 pm","8:00 pm","9:00 pm","10:00 pm","11:00 pm"], rotation=90)
plt.axis([0, 55000, 0, 40])
plt.tight_layout()


plt.savefig(str(fecha)+".jpg", dpi=1000)
plt.show()

##rects1 = plt.bar(index, means_men, bar_width, alpha=opacity,color='b',label='Alumnos')

##
##plt.xlabel('Hora')
##plt.ylabel('Cantidad de alumnos')
##plt.title('Cantidad de alumnos ' + fecha)
##plt.xticks(index + bar_width / 2,OX, rotation=90)
##
##plt.tight_layout()

#plt.savefig('Data/'+str(fecha)+".svg", dpi=150)

#plt.show()



