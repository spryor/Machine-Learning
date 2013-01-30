#Author: Stephen Pryor
#Date: September 22, 2012

import matplotlib.pyplot as plt
import random
import math
from linear_regression import linearRegression

#-----------------------------------------------------------------------START - Generate some linearly related datapoints
#generate data from the line y=20+0.4x plus some randomness
numDataPoints = 200
intercept = 20.0
slope = .4
data_x = [i for i in range(numDataPoints)]
original_line = [intercept+slope*x for x in data_x]
data_y = [random.gauss(y, 20) for y in original_line]
#-----------------------------------------------------------------------END - Generate some linearly related datapoints

#-----------------------------------------------------------------------START - Perform Regression
r_intercept, r_slope = linearRegression(data_x, data_y)
regression_line = [r_intercept+r_slope*x for x in data_x]
#-----------------------------------------------------------------------END - Perform Regression

#-----------------------------------------------------------------------START - Plot data
plt.plot(data_x, data_y, 'bo')
plt.plot(data_x, original_line, 'm-', linewidth=2, label='Original Line')
plt.plot(data_x, regression_line, 'r-', linewidth=2, label='Regression Line')
plt.title('Linear Regression')
plt.legend(loc='upper right')
plt.show()
#-----------------------------------------------------------------------END - Plot data
print 'Original Line: y = '+`intercept`+' + '+`slope`+"*x"
print 'Regression Line: y = '+`r_intercept`+' + '+`r_slope`+"*x"
