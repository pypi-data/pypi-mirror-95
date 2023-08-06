##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

import numpy as np
from scipy import optimize
import copy

from ...finutils.FinError import FinError
from ...finutils.FinDate import FinDate
from ...finutils.FinHelperFunctions import labelToString
from ...finutils.FinHelperFunctions import checkArgumentTypes, _funcName
from ...finutils.FinGlobalVariables import gDaysInYear
from ...market.curves.FinInterpolator import FinInterpTypes, FinInterpolator
from ...market.curves.FinDiscountCurve import FinDiscountCurve
from ...products.rates.FinIborDeposit import FinIborDeposit
from ...products.rates.FinIborFRA import FinIborFRA
from ...products.rates.FinIborSwap import FinIborSwap

swaptol = 1e-10

###############################################################################
# TODO: CHANGE times to dfTimes
###############################################################################


def _f(df, *args):
    ''' Root search objective function for swaps '''
    discountCurve = args[0]
    indexCurve = args[1]
    valueDate = args[2]
    swap = args[3]

    numPoints = len(indexCurve._times)
    indexCurve._dfs[numPoints - 1] = df

    # For curves that need a fit function, we fit it now 
    indexCurve._interpolator.fit(indexCurve._times, indexCurve._dfs)     
    v_swap = swap.value(valueDate, discountCurve, indexCurve, None)

    notional = swap._fixedLeg._notional
    v_swap /= notional
    return v_swap

###############################################################################


def _g(df, *args):
    ''' Root search objective function for swaps '''

    discountCurve = args[0]
    curve = args[1]
    valueDate = args[2]
    fra = args[3]
    numPoints = len(curve._times)
    curve._dfs[numPoints - 1] = df

    # For curves that need a fit function, we fit it now 
    curve._interpolator.fit(curve._times, curve._dfs)     
    v_fra = fra.value(valueDate, discountCurve, curve)
    v_fra /= fra._notional
    return v_fra

###############################################################################


class FinIborDualCurve(FinDiscountCurve):
    ''' Constructs an index curve as implied by the prices of Ibor
    deposits, FRAs and IRS. Discounting is assumed to be at a discount rate
    that is an input and usually derived from OIS rates. '''

###############################################################################

    def __init__(self,
                 valuationDate: FinDate,
                 discountCurve: FinDiscountCurve,
                 iborDeposits: list,
                 iborFRAs: list,
                 iborSwaps: list,
                 interpType: FinInterpTypes = FinInterpTypes.FLAT_FWD_RATES,
                 checkRefit: bool = False):  # Set to True to test it works
        ''' Create an instance of a FinIbor curve given a valuation date and
        a set of ibor deposits, ibor FRAs and iborSwaps. Some of these may
        be left None and the algorithm will just use what is provided. An
        interpolation method has also to be provided. The default is to use a
        linear interpolation for swap rates on coupon dates and to then assume
        flat forwards between these coupon dates.

        The curve will assign a discount factor of 1.0 to the valuation date.
        '''

        checkArgumentTypes(getattr(self, _funcName(), None), locals())

        self._valuationDate = valuationDate
        self._discountCurve = discountCurve
        self._validateInputs(iborDeposits, iborFRAs, iborSwaps)
        self._interpType = interpType
        self._checkRefit = checkRefit
        self._buildCurve()

###############################################################################

    def _buildCurve(self):
        ''' Build curve based on interpolation. '''

        self._buildCurveUsing1DSolver()

###############################################################################

    def _validateInputs(self,
                        iborDeposits,
                        iborFRAs,
                        iborSwaps):
        ''' Validate the inputs for each of the Ibor products. '''

        numDepos = len(iborDeposits)
        numFRAs = len(iborFRAs)
        numSwaps = len(iborSwaps)

        depoStartDate = self._valuationDate
        swapStartDate = self._valuationDate

        if numDepos + numFRAs + numSwaps == 0:
            raise FinError("No calibration instruments.")

        # Validation of the inputs.
        if numDepos > 0:

            depoStartDate = iborDeposits[0]._startDate

            for depo in iborDeposits:

                if isinstance(depo, FinIborDeposit) is False:
                    raise FinError("Deposit is not of type FinIborDeposit")

                startDt = depo._startDate

                if startDt < self._valuationDate:
                    raise FinError("First deposit starts before value date.")

                if startDt < depoStartDate:
                    depoStartDate = startDt

            for depo in iborDeposits:
                startDt = depo._startDate
                endDt = depo._maturityDate
                if startDt >= endDt:
                    raise FinError("First deposit ends on or before it begins")

        # Ensure order of depos
        if numDepos > 1:

            prevDt = iborDeposits[0]._maturityDate
            for depo in iborDeposits[1:]:
                nextDt = depo._maturityDate
                if nextDt <= prevDt:
                    raise FinError("Deposits must be in increasing maturity")
                prevDt = nextDt

        # REMOVED THIS AS WE WANT TO ANCHOR CURVE AT VALUATION DATE 
        # USE A SYNTHETIC DEPOSIT TO BRIDGE GAP FROM VALUE DATE TO SETTLEMENT DATE
        # Ensure that valuation date is on or after first deposit start date
        # if numDepos > 1:
        #    if iborDeposits[0]._effectiveDate > self._valuationDate:
        #        raise FinError("Valuation date must not be before first deposit settles.")

        if numFRAs > 0:
            for fra in iborFRAs:
                if isinstance(fra, FinIborFRA) is False:
                    raise FinError("FRA is not of type FinIborFRA")

                startDt = fra._startDate
                if startDt <= self._valuationDate:
                    raise FinError("FRAs starts before valuation date")

        if numFRAs > 1:
            prevDt = iborFRAs[0]._maturityDate
            for fra in iborFRAs[1:]:
                nextDt = fra._maturityDate
                if nextDt <= prevDt:
                    raise FinError("FRAs must be in increasing maturity")
                prevDt = nextDt

        if numSwaps > 0:

            swapStartDate = iborSwaps[0]._effectiveDate

            for swap in iborSwaps:

                if isinstance(swap, FinIborSwap) is False:
                    raise FinError("Swap is not of type FinIborSwap")

                startDt = swap._effectiveDate
                if startDt < self._valuationDate:
                    raise FinError("Swaps starts before valuation date.")

                if swap._effectiveDate < swapStartDate:
                    swapStartDate = swap._effectiveDate

        if numSwaps > 1:

            # Swaps must all start on the same date for the bootstrap
            startDt = iborSwaps[0]._effectiveDate
            for swap in iborSwaps[1:]:
                nextStartDt = swap._effectiveDate
                if nextStartDt != startDt:
                    raise FinError("Swaps must all have same start date.")

            # Swaps must be increasing in tenor/maturity
            prevDt = iborSwaps[0]._maturityDate
            for swap in iborSwaps[1:]:
                nextDt = swap._maturityDate
                if nextDt <= prevDt:
                    raise FinError("Swaps must be in increasing maturity")
                prevDt = nextDt

            # Swaps must have same cashflows for bootstrap to work
            longestSwap = iborSwaps[-1]
            longestSwapCpnDates = longestSwap._fixedLeg._paymentDates
            for swap in iborSwaps[0:-1]:
                swapCpnDates = swap._fixedLeg._paymentDates
                numFlows = len(swapCpnDates)
                for iFlow in range(0, numFlows):
                    if swapCpnDates[iFlow] != longestSwapCpnDates[iFlow]:
                        raise FinError("Swap coupons are not on the same date grid.")

        #######################################################################
        # Now we have ensure they are in order check for overlaps and the like
        #######################################################################

        lastDepositMaturityDate = FinDate(1, 1, 1900)
        firstFRAMaturityDate = FinDate(1, 1, 1900)
        lastFRAMaturityDate = FinDate(1, 1, 1900)

        if numDepos > 0:
            lastDepositMaturityDate = iborDeposits[-1]._maturityDate

        if numFRAs > 0:
            firstFRAMaturityDate = iborFRAs[0]._maturityDate
            lastFRAMaturityDate = iborFRAs[-1]._maturityDate

        if numSwaps > 0:
            firstSwapMaturityDate = iborSwaps[0]._maturityDate

        if numDepos > 0 and numFRAs > 0:
            if firstFRAMaturityDate <= lastDepositMaturityDate:
                print("FRA Maturity Date:", firstFRAMaturityDate)
                print("Last Deposit Date:", lastDepositMaturityDate)
                raise FinError("First FRA must end after last Deposit")

        if numFRAs > 0 and numSwaps > 0:
            if firstSwapMaturityDate <= lastFRAMaturityDate:
                raise FinError("First Swap must mature after last FRA")

        # If both depos and swaps start after T, we need a rate to get them to
        # the first deposit. So we create a synthetic deposit rate contract.
        
        if swapStartDate > self._valuationDate:

            if numDepos == 0:
                raise FinError("Need a deposit rate to pin down short end.")

            if depoStartDate > self._valuationDate:
                firstDepo = iborDeposits[0]
                if firstDepo._startDate > self._valuationDate:
                    print("Inserting synthetic deposit")
                    syntheticDeposit = copy.deepcopy(firstDepo)
                    syntheticDeposit._startDate = self._valuationDate
                    syntheticDeposit._maturityDate = firstDepo._startDate
                    iborDeposits.insert(0, syntheticDeposit)
                    numDepos += 1

        # Now determine which instruments are used
        self._usedDeposits = iborDeposits
        self._usedFRAs = iborFRAs
        self._usedSwaps = iborSwaps
        self._dayCountType = None

###############################################################################

    def _buildCurveUsing1DSolver(self):
        ''' Construct the discount curve using a bootstrap approach. This is
        the non-linear slower method that allows the user to choose a number
        of interpolation approaches between the swap rates and other rates. It
        involves the use of a solver. '''

        self._interpolator = FinInterpolator(self._interpType)

        self._times = np.array([])
        self._dfs = np.array([])

        # time zero is now.
        tmat = 0.0
        dfMat = 1.0
        self._times = np.append(self._times, 0.0)
        self._dfs = np.append(self._dfs, dfMat)
        self._interpolator.fit(self._times, self._dfs)

        # A deposit is not margined and not indexed to Libor so should
        # probably not be used to build an indexed Libor curve from
        for depo in self._usedDeposits:
            dfSettle = self.df(depo._startDate)
            dfMat = depo._maturityDf() * dfSettle
            tmat = (depo._maturityDate - self._valuationDate) / gDaysInYear
            self._times = np.append(self._times, tmat)
            self._dfs = np.append(self._dfs, dfMat)
            self._interpolator.fit(self._times, self._dfs)

        oldtmat = tmat

        for fra in self._usedFRAs:

            tset = (fra._startDate - self._valuationDate) / gDaysInYear
            tmat = (fra._maturityDate - self._valuationDate) / gDaysInYear

            # if both dates are after the previous FRA/FUT then need to
            # solve for 2 discount factors simultaneously using root search

            if tset < oldtmat and tmat > oldtmat:
                dfMat = fra.maturityDf(self)
                self._times = np.append(self._times, tmat)
                self._dfs = np.append(self._dfs, dfMat)
            else:
                self._times = np.append(self._times, tmat)
                self._dfs = np.append(self._dfs, dfMat)
                argtuple = (self._discountCurve, self, self._valuationDate, fra)
                dfMat = optimize.newton(_g, x0=dfMat, fprime=None,
                                        args=argtuple, tol=swaptol,
                                        maxiter=50, fprime2=None)

        for swap in self._usedSwaps:
            # I use the lastPaymentDate in case a date has been adjusted fwd
            # over a holiday as the maturity date is usually not adjusted CHECK
            maturityDate = swap._fixedLeg._paymentDates[-1]
            tmat = (maturityDate - self._valuationDate) / gDaysInYear

            self._times = np.append(self._times, tmat)
            self._dfs = np.append(self._dfs, dfMat)

            argtuple = (self._discountCurve, self, self._valuationDate, swap)

            dfMat = optimize.newton(_f, x0=dfMat, fprime=None, args=argtuple,
                                    tol=swaptol, maxiter=50, fprime2=None,
                                    full_output=False)

        if self._checkRefit is True:
            self._checkRefits(1e-10, swaptol, 1e-5)

###############################################################################

    # def _buildCurveLinearSwapRateInterpolation(self):
    #     ''' Construct the discount curve using a bootstrap approach. This is
    #     the linear swap rate method that is fast and exact as it does not
    #     require the use of a solver. It is also market standard. '''

    #     self._interpolator = FinInterpolator(self._interpType)

    #     self._times = np.array([])
    #     self._dfs = np.array([])

    #     # time zero is now.
    #     tmat = 0.0
    #     dfMat = 1.0
    #     self._times = np.append(self._times, 0.0)
    #     self._dfs = np.append(self._dfs, dfMat)
    #     self._interpolator.fit(self._times, self._dfs)

    #     for depo in self._usedDeposits:
    #         dfSettle = self.df(depo._effectiveDate)
    #         dfMat = depo._maturityDf() * dfSettle
    #         tmat = (depo._maturityDate - self._valuationDate) / gDaysInYear
    #         self._times = np.append(self._times, tmat)
    #         self._dfs = np.append(self._dfs, dfMat)
    #         self._interpolator.fit(self._times, self._dfs)

    #     oldtmat = tmat

    #     for fra in self._usedFRAs:

    #         tset = (fra._startDate - self._valuationDate) / gDaysInYear
    #         tmat = (fra._maturityDate - self._valuationDate) / gDaysInYear

    #         # if both dates are after the previous FRA/FUT then need to
    #         # solve for 2 discount factors simultaneously using root search

    #         if tset < oldtmat and tmat > oldtmat:
    #             dfMat = fra.maturityDf(self)
    #             self._times = np.append(self._times, tmat)
    #             self._dfs = np.append(self._dfs, dfMat)
    #             self._interpolator.fit(self._times, self._dfs)
    #         else:
    #             self._times = np.append(self._times, tmat)
    #             self._dfs = np.append(self._dfs, dfMat)
    #             self._interpolator.fit(self._times, self._dfs)

    #             argtuple = (self._discountCurve, self, self._valuationDate, fra)
    #             dfMat = optimize.newton(_g, x0=dfMat, fprime=None,
    #                                     args=argtuple, tol=swaptol,
    #                                     maxiter=50, fprime2=None)

    #     if len(self._usedSwaps) == 0:
    #         if self._checkRefit is True:
    #             self._checkRefits(1e-10, swaptol, 1e-5)
    #         return

    #     #######################################################################
    #     # ADD SWAPS TO CURVE
    #     #######################################################################

    #     # Find where the FRAs and Depos go up to as this bit of curve is done
    #     foundStart = False
    #     lastDate = self._valuationDate
    #     if len(self._usedDeposits) != 0:
    #         lastDate = self._usedDeposits[-1]._maturityDate

    #     if len(self._usedFRAs) != 0:
    #         lastDate = self._usedFRAs[-1]._maturityDate

    #     # We use the longest swap assuming it has a superset of ALL of the
    #     # swap flow dates used in the curve construction
    #     longestSwap = self._usedSwaps[-1]
    #     couponDates = longestSwap._adjustedFixedDates
    #     numFlows = len(couponDates)

    #     # Find where first coupon without discount factor starts
    #     startIndex = 0
    #     for i in range(0, numFlows):
    #         if couponDates[i] > lastDate:
    #             startIndex = i
    #             foundStart = True
    #             break

    #     if foundStart is False:
    #         raise FinError("Found start is false. Swaps payments inside FRAs")

    #     swapRates = []
    #     swapTimes = []

    #     # I use the last coupon date for the swap rate interpolation as this
    #     # may be different from the maturity date due to a holiday adjustment
    #     # and the swap rates need to align with the coupon payment dates
    #     for swap in self._usedSwaps:
    #         swapRate = swap._fixedCoupon
    #         maturityDate = swap._adjustedFixedDates[-1]
    #         tswap = (maturityDate - self._valuationDate) / gDaysInYear
    #         swapTimes.append(tswap)
    #         swapRates.append(swapRate)

    #     interpolatedSwapRates = [0.0]
    #     interpolatedSwapTimes = [0.0]

    #     for dt in couponDates[1:]:
    #         swapTime = (dt - self._valuationDate) / gDaysInYear
    #         swapRate = np.interp(swapTime, swapTimes, swapRates)
    #         interpolatedSwapRates.append(swapRate)
    #         interpolatedSwapTimes.append(swapTime)

    #     # Do I need this line ?
    #     interpolatedSwapRates[0] = interpolatedSwapRates[1]

    #     accrualFactors = longestSwap._fixedYearFracs

    #     acc = 0.0
    #     df = 1.0
    #     pv01 = 0.0
    #     dfSettle = self.df(longestSwap._effectiveDate)

    #     for i in range(1, startIndex):
    #         dt = couponDates[i]
    #         df = self.df(dt)
    #         acc = accrualFactors[i-1]
    #         pv01 += acc * df

    #     for i in range(startIndex, numFlows):

    #         dt = couponDates[i]
    #         tmat = (dt - self._valuationDate) / gDaysInYear
    #         swapRate = interpolatedSwapRates[i]
    #         acc = accrualFactors[i-1]
    #         pv01End = (acc * swapRate + 1.0)
    #         dfMat = (dfSettle - swapRate * pv01) / pv01End

    #         self._times = np.append(self._times, tmat)
    #         self._dfs = np.append(self._dfs, dfMat)
    #         self._interpolator.fit(self._times, self._dfs)

    #         pv01 += acc * dfMat

    #     if self._checkRefit is True:
    #         self._checkRefits(1e-10, swaptol, 1e-5)

###############################################################################

    def _checkRefits(self, depoTol, fraTol, swapTol):
        ''' Ensure that the Ibor curve refits the calibration instruments. '''
        for depo in self._usedDeposits:
            v = depo.value(self._valuationDate, self) / depo._notional
            if abs(v - 1.0) > depoTol:
                print("Value", v)
                raise FinError("Deposit not repriced.")

        for fra in self._usedFRAs:
            v = fra.value(self._valuationDate, 
                          self._discountCurve, self) / fra._notional
            if abs(v) > fraTol:
                print("Value", v)
                raise FinError("FRA not repriced.")

        for swap in self._usedSwaps:
            # We value it as of the start date of the swap
            v = swap.value(swap._effectiveDate, self._discountCurve, 
                           self, None)
            v = v / swap._fixedLeg._notional
            if abs(v) > swapTol:
                print("Swap with maturity " + str(swap._maturityDate)
                      + " Not Repriced. Has Value", v)
                swap.printFixedLegPV()
                swap.printFloatLegPV()
                raise FinError("Swap not repriced.")

###############################################################################

    def __repr__(self):
        ''' Print out the details of the Ibor curve. '''

        s = labelToString("OBJECT TYPE", type(self).__name__)
        s += labelToString("VALUATION DATE", self._valuationDate)

        for depo in self._usedDeposits:
            s += labelToString("DEPOSIT", "")
            s += depo.__repr__()

        for fra in self._usedFRAs:
            s += labelToString("FRA", "")
            s += fra.__repr__()

        for swap in self._usedSwaps:
            s += labelToString("SWAP", "")
            s += swap.__repr__()

        numPoints = len(self._times)

        s += labelToString("INTERP TYPE", self._interpType)
        s += labelToString("GRID TIMES", "GRID DFS")

        for i in range(0, numPoints):
            s += labelToString("% 10.6f" % self._times[i],
                               "%12.10f" % self._dfs[i])
        return s

###############################################################################

    def _print(self):
        ''' Simple print function for backward compatibility. '''
        print(self)

###############################################################################
