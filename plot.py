from pricing import Pricing
import matplotlib.pyplot as plt

god = 365

class Plot(Pricing):
    def plotPL(self, bePriceS, bePriceF, params, exp, step):
        bePrice = []
        i = bePriceS
        while i <= bePriceF:
            bePrice.append(i)
            i+=step
        P_L = []
        for s in bePrice:
           P_L.append(self.p_l(s, params, exp))
        plt.plot(bePrice, P_L, label=int(exp*god))
        
    def plotDelta(self, bePriceS, bePriceF, params, exp, step):
        bePrice = []
        i = bePriceS
        while i <= bePriceF:
            bePrice.append(i)
            i+=step
        D = []
        for s in bePrice:
           D.append(self.deltaFull(s, params, exp))  
        plt.plot(bePrice, D, label=int(exp*god))
        
    def plotTheta(self, bePriceS, bePriceF, params, exp, step):
        bePrice = []
        i = bePriceS
        while i <= bePriceF:
            bePrice.append(i)
            i+=step
        T = []
        for s in bePrice:
           T.append(self.thetaFull(s, params, exp))
        plt.plot(bePrice, T, label=int(exp*god))
        
    def plotVega(self, bePriceS, bePriceF, params, exp, step):
        bePrice = []
        i = bePriceS
        while i <= bePriceF:
            bePrice.append(i)
            i+=step
        V = []
        for s in bePrice:
           V.append(self.vegaFull(s, params, exp))
        plt.plot(bePrice, V, label=int(exp*god))
        
    def plotGamma(self, bePriceS, bePriceF, params, exp, step):
        bePrice = []
        i = bePriceS
        while i <= bePriceF:
            bePrice.append(i)
            i+=step
        V = []
        for s in bePrice:
           V.append(self.gammaFull(s, params, exp))
        plt.plot(bePrice, V, label=int(exp*god))