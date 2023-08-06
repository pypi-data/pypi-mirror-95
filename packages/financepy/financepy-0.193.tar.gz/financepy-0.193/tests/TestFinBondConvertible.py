###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

# TODO
import time
import numpy as np

import sys
sys.path.append("..")

from financepy.products.bonds.FinBondConvertible import FinBondConvertible
from financepy.finutils.FinDate import FinDate
from financepy.finutils.FinFrequency import FinFrequencyTypes
from financepy.finutils.FinDayCount import FinDayCountTypes
from financepy.market.curves.FinDiscountCurveFlat import FinDiscountCurveFlat

from FinTestCases import FinTestCases, globalTestCaseMode
testCases = FinTestCases(__file__, globalTestCaseMode)

###############################################################################


def test_FinBondConvertible():

    settlementDate = FinDate(31, 12, 2003)
    startConvertDate = FinDate(31, 12, 2003)
    maturityDate = FinDate(15, 3, 2022)
    conversionRatio = 38.4615  # adjust for face
    coupon = 0.0575
    freqType = FinFrequencyTypes.SEMI_ANNUAL
    accrualBasis = FinDayCountTypes.ACT_365F
    face = 1000.0

    callPrice = 1100
    callDates = [FinDate(20, 3, 2007),
                 FinDate(15, 3, 2012),
                 FinDate(15, 3, 2017)]
    callPrices = np.array([callPrice, callPrice, callPrice])

    putPrice = 90
    putDates = [FinDate(20, 3, 2007),
                FinDate(15, 3, 2012),
                FinDate(15, 3, 2017)]
    putPrices = np.array([putPrice, putPrice, putPrice])

    bond = FinBondConvertible(maturityDate,
                              coupon,
                              freqType,
                              startConvertDate,
                              conversionRatio,
                              callDates,
                              callPrices,
                              putDates,
                              putPrices,
                              accrualBasis,
                              face)
#    print(bond)

    dividendDates = [FinDate(2007, 3, 20),
                     FinDate(2008, 3, 15),
                     FinDate(2009, 3, 15),
                     FinDate(2010, 3, 15),
                     FinDate(2011, 3, 15),
                     FinDate(2012, 3, 15),
                     FinDate(2013, 3, 15),
                     FinDate(2014, 3, 15),
                     FinDate(2015, 3, 15),
                     FinDate(2016, 3, 15),
                     FinDate(2017, 3, 15),
                     FinDate(2018, 3, 15),
                     FinDate(2019, 3, 15),
                     FinDate(2020, 3, 15),
                     FinDate(2021, 3, 15),
                     FinDate(2022, 3, 15)]

    dividendYields = [0.00] * 16
    stockPrice = 28.5
    stockVolatility = 0.370
    rate = 0.04
    discountCurve = FinDiscountCurveFlat(settlementDate,
                                         rate,
                                         FinFrequencyTypes.CONTINUOUS)
    creditSpread = 0.00
    recoveryRate = 0.40
    numStepsPerYear = 20

    testCases.header("LABEL")
    testCases.print("NO CALLS OR PUTS")

    testCases.header("TIME", "NUMSTEPS", "PRICE")

    for numStepsPerYear in [5, 10, 20, 80]:
        start = time.time()
        res = bond.value(settlementDate,
                         stockPrice,
                         stockVolatility,
                         dividendDates,
                         dividendYields,
                         discountCurve,
                         creditSpread,
                         recoveryRate,
                         numStepsPerYear)

        end = time.time()
        period = end - start
        testCases.print(period, numStepsPerYear, res)

    dividendYields = [0.02] * 16
    testCases.header("LABEL")
    testCases.print("DIVIDENDS")

    testCases.header("TIME", "NUMSTEPS", "PRICE")
    for numStepsPerYear in [5, 20, 80]:
        start = time.time()
        res = bond.value(settlementDate,
                         stockPrice,
                         stockVolatility,
                         dividendDates,
                         dividendYields,
                         discountCurve,
                         creditSpread,
                         recoveryRate,
                         numStepsPerYear)
        end = time.time()
        period = end - start
        testCases.print(period, numStepsPerYear, res)

###############################################################################


test_FinBondConvertible()
testCases.compareTestCases()
