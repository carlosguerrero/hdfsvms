import plots

p = plots.PLOTS('20171017105257')

p.plotfitEvoluation()

import numpy as np
a = range(0,10)
b = range(0,10)

random.shuffle(b)

#np.mean(np.array([a,b]),axis=0)

z = np.array([a])
m = np.append(m,[a],axis=0)



vmScaleLevel = [2.0]
pmScaleLevel = [100]
fileNumberScaleLevel = [50]


#vmScaleLevel = [0.5,1.0,2.0,4.0]
#pmScaleLevel = [50,100,200,500]
#fileNumberScaleLevel = [25,50,100,200]  

import plots3
for vmSL in vmScaleLevel:
    for pmSL in pmScaleLevel:
        for fnSL in fileNumberScaleLevel:
            
            p = plots3.PLOTS3('20171023160008',vmSL,pmSL,fnSL)
            p.plotfitEvolution()