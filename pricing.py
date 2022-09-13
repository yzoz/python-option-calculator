from bsm import BSM

class Pricing(BSM):

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
            plF = plF + plS
            i+=1
        return plF