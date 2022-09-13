from pricing import Pricing

#in deep development

class Search(Pricing):
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

search = Search()

god = 365
step = 10
deep = 7500

exp = 30 / god
exp2 = 15 / god
exp3 = 5 / god

fPrice = 21000

params = []

dType = 'F'
quant = 1
price = 20000
strike = 0
vola = 0
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

dType = 'C'
quant = 1
price = 500
strike = 25000
vola = 0.75
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

dType = 'P'
quant = 1
price = 100
strike = 15000
vola = 0.75
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

dType = 'P'
quant = -1
price = 25
strike = 10000
vola = 1.5
params.append({'dType': dType, 'price': price, 'quant': quant, 'strike': strike, 'vola': vola, 'exp': exp})

bePriceS = fPrice - deep
bePriceF = fPrice + deep

acc = 0.1

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

search.searchDelta(fPrice, deep, acc, paramD1, params)
search.searchDelta(fPrice, deep, acc, paramD_1, params)
search.searchDelta(fPrice, deep, acc, paramD2, params)
search.searchDelta(fPrice, deep, acc, paramD_2, params)
search.searchDelta(fPrice, deep, acc, paramD3, params)
search.searchDelta(fPrice, deep, acc, paramD_3, params)