import math
import scipy.stats
import matplotlib.pyplot as plt

global god
god = 365

global step
step = 0.01

class Calculation():

    def d1(self, S, K, V, T):
        return (math.log(S / float(K)) + (V**2 / 2) * T) / (V * math.sqrt(T))

    def d2(self, S, K, V, T):
        return self.d1(S, K, V, T) - (V * math.sqrt(T))

    def theo(self, S, K, V, T, dT):
        if dT == 'C':
            return S * scipy.stats.norm.cdf(self.d1(S, K, V, T)) - K * scipy.stats.norm.cdf(self.d2(S, K, V, T))
        else:
            return K * scipy.stats.norm.cdf(-self.d2(S, K, V, T)) - S * scipy.stats.norm.cdf(-self.d1(S, K, V, T))


    def delta(self, S, K, V, T, dT):
        if dT == 'C':
            delta = scipy.stats.norm.cdf(self.d1(S, K, V, T))
        elif dT == 'P':
            delta = scipy.stats.norm.cdf(self.d1(S, K, V, T)) - 1
        else:
            delta = 1
        return delta

    def vega(self, S, K, V, T):
        vega = (S * math.sqrt(T) * scipy.stats.norm.pdf(self.d1(S, K, V, T))) / 100
        return vega

    def theta(self, S, K, V, T):
        theta = -((S * V * scipy.stats.norm.pdf(self.d1(S, K, V, T))) / (2 * math.sqrt(T))) / god
        return theta

    def gamma(self, S, K, V, T):
        gamma = scipy.stats.norm.pdf(self.d1(S, K, V, T))/(S * V * math.sqrt(T))
        return gamma


    def deltaFull(self, fPrice, params, exp):
        i = 0
        n = len(params)
        deltaFull = 0
        while i < n:
            param = params[i]
            if exp:
                param['exp'] = exp
            deltaSingle = self.delta(fPrice, param['strike'], param['vola'], param['exp'], param['dType']) * param['quant']
            deltaFull = deltaFull + deltaSingle
            i+=1
        return deltaFull

    def vegaFull(self, fPrice, params, exp):
        i = 0
        n = len(params)
        vegaFull = 0
        while i < n:
            param = params[i]
            if exp:
                param['exp'] = exp
            if param['dType'] != 'F':
                vegaSingle = self.vega(fPrice, param['strike'], param['vola'], param['exp']) * param['quant']
                vegaFull = vegaFull + vegaSingle
            i+=1
        return vegaFull

    def thetaFull(self, fPrice, params, exp):
        i = 0
        n = len(params)
        thetaFull = 0
        while i < n:
            param = params[i]
            if exp:
                param['exp'] = exp
            if param['dType'] != 'F':
                thetaSingle = self.theta(fPrice, param['strike'], param['vola'], param['exp']) * param['quant']
                thetaFull = thetaFull + thetaSingle
            i+=1
        return thetaFull
        
    def gammaFull(self, fPrice, params, exp):
        i = 0
        n = len(params)
        gammaFull = 0
        while i < n:
            param = params[i]
            if exp:
                param['exp'] = exp
            if param['dType'] != 'F':
                gammaSingle = self.gamma(fPrice, param['strike'], param['vola'], param['exp']) * param['quant']
                gammaFull = gammaFull + gammaSingle
            i+=1
        return gammaFull

    def p_l(self, fPrice, params, exp):
        i = 0
        n = len(params)
        plF = 0
        while i < n:
            param = params[i]
            if exp:
                param['exp'] = exp
            if param['dType'] == 'F':
                plS = (fPrice - param['price']) * param['quant']
            else:
                theo = round(self.theo(fPrice, param['strike'], param['vola'], param['exp'], param['dType']), 3)
                plS = (theo - param['price']) * param['quant']
            #print(param['dType'], plS)
            plF = plF + plS
            i+=1
        return plF

    def plotPL(self, bePriceS, bePriceF, params, exp):
        bePrice = []
        i = bePriceS
        while i <= bePriceF:
            bePrice.append(i)
            i+=step
        P_L = []
        for s in bePrice:
           P_L.append(self.p_l(s, params, exp))
        plt.plot(bePrice, P_L, label=int(exp*god))
        
    def plotDelta(self, bePriceS, bePriceF, params, exp):
        bePrice = []
        i = bePriceS
        while i <= bePriceF:
            bePrice.append(i)
            i+=step
        D = []
        for s in bePrice:
           D.append(self.deltaFull(s, params, exp))  
        plt.plot(bePrice, D, label=int(exp*god))
        
    def plotTheta(self, bePriceS, bePriceF, params, exp):
        bePrice = []
        i = bePriceS
        while i <= bePriceF:
            bePrice.append(i)
            i+=step
        T = []
        for s in bePrice:
           T.append(self.thetaFull(s, params, exp))
        plt.plot(bePrice, T, label=int(exp*god))
        
    def plotVega(self, bePriceS, bePriceF, params, exp):
        bePrice = []
        i = bePriceS
        while i <= bePriceF:
            bePrice.append(i)
            i+=step
        V = []
        for s in bePrice:
           V.append(self.vegaFull(s, params, exp))
        plt.plot(bePrice, V, label=int(exp*god))
        
    def plotGamma(self, bePriceS, bePriceF, params, exp):
        bePrice = []
        i = bePriceS
        while i <= bePriceF:
            bePrice.append(i)
            i+=step
        V = []
        for s in bePrice:
           V.append(self.gammaFull(s, params, exp))
        plt.plot(bePrice, V, label=int(exp*god))

    def searchDelta(self, fPrice, deep, acc, paramD, params):
        """if paramD['dType'] == 'C':
            if paramD['quant'] < 0:
                direct = 'U'
            else:
                direct = 'D'
        else:
            if paramD['quant'] < 0:
                direct = 'D'
            else:
                direct = 'U'
        if direct == 'U':
            start = fPrice
            finish = fPrice + deep
        else:
            start = fPrice - deep
            finish = fPrice"""
        matrix = []
        start = fPrice - deep
        finish = fPrice + deep
        while start <= finish:
            deltaD = round((self.delta(start, paramD['strike'], paramD['vola'], paramD['exp'], paramD['dType'])) * paramD['quant'], 4)
            deltaF = round(self.deltaFull(start, params, 0), 3)
            #print(start, '|', deltaD, '|', deltaF)
            if deltaD == -deltaF:
                if paramD['dType'] != 'F':
                    theo = round(self.theo(start, paramD['strike'], paramD['vola'], paramD['exp'], paramD['dType']), 3)
                else:
                    theo = 0
                matrix.append([round(start, 2), paramD['dType'], paramD['strike'], paramD['quant'], deltaD, deltaF , theo])
                #break
            start = start + acc
        i = 0
        n = len(matrix)
        prices = []
        while i < n:
            if prices:
                if matrix[i-1][4] != matrix[i][4]:
                    prices.append(matrix[i])
            else:
                prices.append(matrix[i])
            i = i + 1
        for j in prices:
            print(j[0], '|', j[1], '|', j[2], '|', j[3], '|', j[4], '|', j[5], '|', j[6])


calc = Calculation()

deep = 2

acc = 0.0001

exp = 15 / god

fPrice = 55

volaShift = 0/100

exp2 = 12
exp3 = 9

params = []

dType = 'F'
quant = 4
price = 55.36
strike = 0
vola = 0
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

dType = 'C'
quant = 10
price = 1.31
strike = 56
vola = 27.25/100 + volaShift
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

dType = 'P'
quant = 8
price = 1.24
strike = 56
vola = 27.25/100 + volaShift
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

dType = 'P'
quant = 5
price = 0.82
strike = 55
vola = 27.7/100 + volaShift
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

bePriceS = fPrice - deep
bePriceF = fPrice + deep

calc.plotPL(bePriceS, bePriceF, params, exp)
calc.plotPL(bePriceS, bePriceF, params, exp2/god)
calc.plotPL(bePriceS, bePriceF, params, exp3/god)
plt.ylabel("P/L")
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.show()

calc.plotDelta(bePriceS, bePriceF, params, exp)
calc.plotDelta(bePriceS, bePriceF, params, exp2/god)
calc.plotDelta(bePriceS, bePriceF, params, exp3/god)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Delta")
plt.show()

calc.plotTheta(bePriceS, bePriceF, params, exp)
calc.plotTheta(bePriceS, bePriceF, params, exp2/god)
calc.plotTheta(bePriceS, bePriceF, params, exp3/god)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Theta")
plt.show()

calc.plotVega(bePriceS, bePriceF, params, exp)
calc.plotVega(bePriceS, bePriceF, params, exp2/god)
calc.plotVega(bePriceS, bePriceF, params, exp3/god)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Vega")
plt.show()

calc.plotGamma(bePriceS, bePriceF, params, exp)
calc.plotGamma(bePriceS, bePriceF, params, exp2/god)
calc.plotGamma(bePriceS, bePriceF, params, exp3/god)
plt.xlabel("Price")
plt.title("Option")
plt.grid(True)
plt.legend()
plt.ylabel("Gamma")
plt.show()


print('D:\t', round(calc.deltaFull(fPrice, params, exp), 2))

print('V:\t', round(calc.vegaFull(fPrice, params, exp), 2))

print('T:\t', round(calc.thetaFull(fPrice, params, exp), 2))

print('G:\t', round(calc.gammaFull(fPrice, params, exp), 2))

print('P/L:\t', calc.p_l(fPrice, params, exp))

#Donee

dType = 'F'
strike = 0
price = 0
quant = -1
vola = 0
paramD_1 = {'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp}

dType = 'F'
strike = 0
price = 0
quant = 1
vola = 0
paramD1 = {'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp}

dType = 'F'
strike = 0
price = 0
quant = -2
vola = 0
paramD_2 = {'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp}

dType = 'F'
strike = 0
price = 0
quant = 2
vola = 0
paramD2 = {'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp}

dType = 'F'
strike = 0
price = 0
quant = -3
vola = 0
paramD_3 = {'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp}

dType = 'F'
strike = 0
price = 0
quant = 3
vola = 0
paramD3 = {'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp}




calc.searchDelta(fPrice, deep, acc, paramD1, params)
calc.searchDelta(fPrice, deep, acc, paramD_1, params)
calc.searchDelta(fPrice, deep, acc, paramD2, params)
calc.searchDelta(fPrice, deep, acc, paramD_2, params)
calc.searchDelta(fPrice, deep, acc, paramD3, params)
calc.searchDelta(fPrice, deep, acc, paramD_3, params)

S = 54
K = 53
V = 0.35
T = 3
dT = "P"

#print('One: ', round(calc.theo(S, K, V, T/god, dT), 2))