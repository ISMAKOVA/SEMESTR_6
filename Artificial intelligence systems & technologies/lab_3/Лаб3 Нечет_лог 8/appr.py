import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


beta = (0.25, 0.75, 0.5) # темный
#beta = (1, 1, 5) # светлый
#beta = (1, 0.25, 5) # средний
#beta = (1, 5, 2) # средний

def f(x, b0, b1, b2):
    return b0 + b1 * np.exp(-b2 * x**2) # темный
    #return 1 /(1 + (-b0* np.exp(-b1*x+b2)) )# светлый
    #return b0*np.exp(-b1*(x-b2)**2) # средний
    #return 1/(b0+(ABS((A1-b1)/2))^(2*b2)) # средний


# зададим массив точек хi
xdata = np.linspace(0, 5, 50)
# создаем теоретически правильные значения точек yi (без шума)
y = f(xdata, *beta)
# зашумляем эти данные
ydata = y + 0.05 * np.random.randn(len(xdata))

beta_opt, beta_cov = curve_fit(f, xdata, ydata)
print(beta_opt)     # array([ 0.25733353, 0.76867338, 0.54478761])

lin_dev =  sum(beta_cov[0])
print (lin_dev)

residuals = ydata - f(xdata,*beta_opt)
fres = sum(residuals**2)
print (fres)

fig, ax = plt.subplots()
ax.scatter(xdata, ydata)
ax.plot(xdata, y, 'r', lw=2, label="Theoretical")
ax.plot(xdata, f(xdata, *beta_opt), 'b', lw=2, label="Fit")
ax.legend()
ax.set_xlim(0, 5)
ax.set_xlabel(r"$x$", fontsize=18)
ax.set_ylabel(r"$f(x, \beta)$", fontsize=18)
plt.show()
