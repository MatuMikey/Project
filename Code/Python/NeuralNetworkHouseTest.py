from NeuralNetworker import NeuralNetwork
from NeuralNetworker import normalise
import csv
import matplotlib.pyplot as plt
import datetime
from KalmanFilter import KalmanFilter

kFilter1 = KalmanFilter(1,1,0.01)
kFilter2 = KalmanFilter(1,1,0.01)
kFilter3 = KalmanFilter(1,1,0.01)
n1 = NeuralNetwork(11,1)
n2 = NeuralNetwork(11,1)
n3 = NeuralNetwork(11,1)
n1.setWeights([-0.218788, 0.518393, -0.333481, -0.390596, -0.175823, 0.21197, -0.915951, -0.945299, 0.974385, 0.387424, -0.180784, 0.24832, 0.601386, -0.104627, -0.40223, 0.981041, 0.930184, -0.757875, 0.131709, 0.17211, -0.663473, -0.472646, 0.921197, -0.975197, 0.102504, -0.190601, -0.92337, -0.471781, 0.996065, 0.911577, -0.93847, 0.899338, 0.908742, -0.313213, -0.855279, -0.364136, -0.306024, -0.475977, 0.255888, 0.422726, -0.553563, -0.927198, 0.032341, 0.25364, -0.91652])
n2.setWeights([0.928169, -0.484684, 0.385694, 0.881541, 0.212824, -0.934946, -0.586629, -0.526488, -0.454734, -0.385876, 0.533982, 0.752168, -0.277664, 0.412462, 0.520905, -0.277887, -0.479069, 0.592334, 0.345505, -0.585069, -0.288327, 0.434479, -0.231896, -0.673852, -0.590521, -0.820682, -0.215185, -0.617577, 0.916679, -0.469671, -0.972164, -0.946014, -0.725467, 0.617744, 0.364938, 0.511791, 0.03651, 0.385448, 0.786171, -0.291749, -0.126394, -0.633175, -0.774067, 0.061192, -0.215491])
n3.setWeights([-0.680501, -0.715207, -0.281537, -0.7374, 0.742753, 0.766232, 0.619028, -0.668628, -0.335874, 0.541612, 0.398226, 0.518879, -0.52445, 0.206504, 0.431796, -0.606786, -0.016391, -0.550873, -0.287677, 0.331439, 0.934513, 0.594169, -0.114775, 0.386435, -0.98498, -0.860275, 0.109254, -0.978023, -0.664958, -0.70606, 0.248496, 0.942915, 0.677829, -0.363277, -0.263849, -0.546045, -0.726076, -0.1324, 0.416673, -0.706917, 0.925891, 0.603731, 0.187877, -0.014026, -0.61599])

time1 = []
time2 = []
sensor1 = []
sensor2 = []
sensor3 = []
with open('HouseData.csv', 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=';', quotechar='"')
    data = list(data)
    for i in range(5, len(data)-5):
        for j in range(0, len(data[i])):
            data[i][j] = float(data[i][j])
        if (data[i][2] == 0.0 or data[i][3] == 0.0 or data[i][4] == 0.0):
            continue
        time1.append(data[i][1])
        time2.append(data[i][1] + 86399*(data[i][0]-3))
        sensor1.append(kFilter1.updateEstimate(data[i][2]))
        sensor2.append(kFilter2.updateEstimate(data[i][3]))
        sensor3.append(kFilter3.updateEstimate(data[i][4]))

normalise(time1, sensor1, sensor2, sensor3)
    
output1 = []
output2 = []
output3 = []
for i in range(0, len(sensor1)):
   output1.append(n1.predict([sensor2[i], sensor3[i], time1[i]]))
   output2.append(n2.predict([sensor1[i], sensor3[i], time1[i]]))
   output3.append(n3.predict([sensor1[i], sensor2[i], time1[i]]))



for i in range(0, len(output1)):
    output1[i] = output1[i]*(35.515-20.995)+20.995
    sensor1[i] = sensor1[i]*(35.515-20.995)+20.995
    
    output2[i]  = output2[i]*(28.981-24.372)+24.372
    sensor2[i] = sensor2[i]*(28.981-24.372)+24.372
    
    output3[i]  = output3[i]*(29.357-23.545)+23.95
    sensor3[i] = sensor3[i]*(29.357-23.545)+23.545
    
plt.figure(6)
plt.plot(output1, color='red')
plt.xlabel("Time (days)")
plt.ylabel("Temperature (degrees Celcius)")
plt.title("Sensor and neural network temperature readings over a 5 day period")
plt.plot(sensor1, color = 'green')

plt.figure(7)
plt.plot(output2, color='red')
plt.plot(sensor2, color = 'green')
plt.xlabel("Time (days)")
plt.ylabel("Temperature (degrees Celcius)")
plt.title("Sensor and neural network temperature readings over a 5 day period")

plt.figure(8)
plt.plot(output3, color='red')
plt.plot(sensor3, color = 'green')
plt.xlabel("Time (days)")
plt.ylabel("Temperature (degrees Celcius)")
plt.title("Sensor and neural network temperature readings over a 5 day period")
