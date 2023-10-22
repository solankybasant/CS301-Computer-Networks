import matplotlib.pyplot as plt

x = [2,4,6,8,10]
y = [396265.3751,315612.0358,268167.0139,236504.1640,205171.1073]

plt.plot(x,y)

plt.xlabel('Delay(ms)')
plt.ylabel('Avg. Throughput (bps)')

plt.title('Avg. Throughput changing with delay')

plt.show()
