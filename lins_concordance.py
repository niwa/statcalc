#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import math

from tabulate import tabulate


def calculate_concordance(source_data):
    """Created march 2003 by G.W.Payne
       Concordance calculator as described by Mr Graham McBride.
    """
    xydata = []
    data_raw = source_data.split('~')  #this splits the text string passed in into an array based on where the hashes were
    num_data_points = len(data_raw) / 2
    current_data_point = 0
    while current_data_point < num_data_points:
        x_val = float(data_raw[current_data_point * 2])
        y_val = float(data_raw[(current_data_point * 2) + 1])
        xydata.append([x_val, y_val])
        current_data_point = current_data_point + 1

    #define all the variables used
    #xydata=[(1.1,0.1),(2,0.3),(3,0.6),(4,0.9),(5,1.2),(6,1.5),(7,1.8),(8,2.1),(9,2.4),(10,2.7),(11,3.0)]

    n = 0  #number pairs
    SumX = float(0)  #sum of X values
    SumY = float(0)  #sum of Y values
    SumXX = float(0)  #sum of squares of x values
    SumYY = float(0)  #sum of squares of x values
    VarX = float(0)  #variance of X values
    VarY = float(0)  #variance of Y
    MeanX = float(0)  #Mean of X values
    MeanY = float(0)  #Mean of Y values
    #SQR_MeanX=float(0)              #MeanX squared
    #SQR_MeanY=float(0)              #Mean of Y squared
    SumCoVarXY = float(0)  #Sum of CoVariance of X,Y pairs
    CoVarXY = float(0)  #CoVariance of X,Y pairs
    Lins_rc = float(0)  #Sample Concordance corerelation coefficient (Lins rc)
    Zestimate = float(0)  #tanh-1(Lins_rc)
    r = float(0)  #Pearson's r
    r2 = float(0)  #Pearson's r squared
    One_r2 = float(0)  #1-Pearson's r
    One_Lins_rc = float(0)  #1-Lins_rc
    Lins_rc_sq = float(0)  #Lins_rc squared
    One_Lins_rc_sq = float(0)  #1-(Lins_rc squared)
    One_Lins_rc_sq_sq = float(0)  #(1-(Lins_rc squared)) squared
    Lins_rc_3 = float(0)  #Lins_rc^3
    Lins_rc_4 = float(0)  #Lins_rc^4
    u = float(0)  #(MeanX - MeanY)/(VarX*VarY)^0.25
    u2 = float(0)  #u^2
    u4 = float(0)  #u^4
    Numerator1 = float(0)  #One_r2*Lins_rc_squared/(One_Lins_rc_sq*r2)
    Numerator2 = float(0)  #2*Lins_rc_3*One_Lins_rc*u2/(r*One_Lins_rc_sq_sq)
    Numerator3 = float(0)  #Lins_rc_4*u4/(2*r2*One_Lins_rc_sq_sq)
    SE_Zestimate = float(0)  #(SQRT((Numerator1+Numerator2-Numerator3)/(n-2))
    Lower_1_95_CL_for_Z = float(0)  #Zestimate-1.6449*SE_of_Zestimate
    Upper_1_95_CL_for_Z = float(0)  #Zestimate+1.6449*SE_of_Zestimate
    Lower_2_95_CL_for_Z = float(0)  #Zestimate-1.96*SE_of_Zestimate
    Upper_2_95_CL_for_Z = float(0)  #Zestimate+1.96*SE_of_Zestimate

    Lower_1_95_CL_for_rc = float(0)  #TANH(Lower_1_95_CL_for_Z)
    Upper_1_95_CL_for_rc = float(0)  #TANH(Upper_1_95_CL_for_Z)
    Lower_2_95_CL_for_rc = float(0)  #TANH(Lower_2_95_CL_for_Z)
    Upper_2_95_CL_for_rc = float(0)  #TANH(Upper_2_95_CL_for_Z)

    #calculate sums and sums of squares
    for point in xydata:
        n = n + 1
        SumX = SumX + (point[0])
        SumY = SumY + (point[1])
        SumXX = SumXX + (point[0])**2
        SumYY = SumYY + (point[1])**2
    #calculate means
    MeanX = SumX / n
    MeanY = SumY / n
    #calculate Square roots of Means
    #SQR_MeanX=math.sqrt(MeanX)
    #SQR_MeanY=math.sqrt(MeanY)
    #calculate variance for X and Y's
    VarX = (n * SumXX - SumX**2) / n**2
    VarY = (n * SumYY - SumY**2) / n**2
    #calculate Covariance of X,Y pairs
    for point in xydata:
        SumCoVarXY = SumCoVarXY + ((point[0]) - MeanX) * ((point[1]) - MeanY)
    CoVarXY = SumCoVarXY / n
    #calculate Lins concordance
    Lins_rc = 2 * CoVarXY / (VarX + VarY + (MeanX - MeanY)**2)
    #calculate Zestimate
    Zestimate = math.atanh(Lins_rc)

    #calculate Pearson's r value
    r = CoVarXY / math.sqrt(VarX * VarY)
    #calculate Pearsons value squared
    r2 = r**2
    #calculate 1-Pearsons r squared
    One_r2 = 1 - r2
    #calculate 1-Lins_rc
    One_Lins_rc = 1 - Lins_rc
    #calculate Lins_rc squared
    Lins_rc_sq = Lins_rc**2
    #calculate 1-Lins_rc squared
    One_Lins_rc_sq = 1 - Lins_rc_sq
    #calculate (1-Lins_rc squared) squared
    One_Lins_rc_sq_sq = (1 - Lins_rc_sq)**2
    #calculate Lins_rc to power 3
    Lins_rc_3 = Lins_rc**3
    #calculate Lins_rc to power 4
    Lins_rc_4 = Lins_rc**4
    #calculate u
    u = (MeanX - MeanY) / (VarX * VarY)**0.25
    #calculate u squared and u to power 4
    u2 = u**2
    u4 = u**4
    #calculate Numerator1
    Numerator1 = (One_r2 * Lins_rc_sq) / (One_Lins_rc_sq * r2)
    #calculate Numerator2
    Numerator2 = (2 * Lins_rc_3 * One_Lins_rc * u2) / (r * One_Lins_rc_sq_sq)
    #calculate Numerator3
    Numerator3 = (Lins_rc_4 * u4) / (2 * r2 * One_Lins_rc_sq_sq)
    #calculate SE Zestimate
    SE_Zestimate = math.sqrt((Numerator1 + Numerator2 - Numerator3) / (n - 2))
    #calculate lower and upper one sided confidence limits for Z
    Lower_1_95_CL_for_Z = Zestimate - 1.6449 * SE_Zestimate
    Upper_1_95_CL_for_Z = Zestimate + 1.6449 * SE_Zestimate
    #calculate lower and upper two sided confidence limits for Z
    Lower_2_95_CL_for_Z = Zestimate - 1.96 * SE_Zestimate
    Upper_2_95_CL_for_Z = Zestimate + 1.96 * SE_Zestimate
    #calculate lower and upper one sided confidence limits for rc
    Lower_1_95_CL_for_rc = math.tanh(Lower_1_95_CL_for_Z)
    Upper_1_95_CL_for_rc = math.tanh(Upper_1_95_CL_for_Z)
    #calculate lower and upper two sided confidence limits for rc
    Lower_2_95_CL_for_rc = math.tanh(Lower_2_95_CL_for_Z)
    Upper_2_95_CL_for_rc = math.tanh(Upper_2_95_CL_for_Z)
    #    print 'n = ',n
    #    print 'SumX = ',SumX
    #    print 'SumXX = ',SumXX
    #   print 'MeanX = ',MeanX
    #   print 'SQR_MeanX = ',SQR_MeanX
    #    print 'SumY = ',SumY
    #    print 'SumYY = ',SumYY
    #    print 'MeanY = ',MeanY
    #    print 'SQR_MeanY = ',SQR_MeanY
    #    print 'VarX = ',VarX
    #    print 'VarY = ',VarY
    #    print 'CoVarXY = ',CoVarXY
    #    print 'Lins_rc = ',Lins_rc
    #    print 'Pearson r = ',r
    #    print 'Pearsons r2 = ',r2
    #    print '1-pearsons r2 = ', One_r2
    #    print '1-Lins_rc = ',One_Lins_rc
    #    print 'Lins_rc squared = ',Lins_rc_sq
    #    print '1-Lins_rc_sq = ',One_Lins_rc_sq
    #    print '(1-Lins_rc_sq) squared = ',One_Lins_rc_sq_sq
    #    print 'Lins_rc to power 3 = ',Lins_rc_3
    #    print 'Lins_rc to power 4 = ',Lins_rc_4
    #    print 'u = ',u
    #    print 'u2 = ',u2
    #    print 'u4 = ',u4
    #    print 'Numerator1 = ',Numerator1
    #    print 'Numerator2 = ',Numerator2
    #    print 'Numerator3 = ',Numerator3
    #    print 'SE Lins_rc = ',SE_Lins_rc
    #    print 'Lower 1 sided 95% CL = ',Lower_1_95_CL
    #    print 'Upper 1 sided 95% CL = ',Upper_1_95_CL
    #    print 'Lower 2 sided 95% CL = ',Lower_2_95_CL
    #    print 'Upper 2 sided 95% CL = ',Upper_2_95_CL

    #write out table of results (all lines with #* at beginning)- note {} denote variable names, output text as is.

    #* Sample concordance correlation coefficient (rc) = {Lins_rc}
    #*                   Lower one-sided 95% CL for Pc = {Lower_1_95_CL_for_rc}
    #*                  Sample two-sided 95% CL for Pc = {Lower_2_95_CL_for_rc}
    #*                   Upper one-sided 95% CL for Pc = {Upper_1_95_CL_for_rc}
    #*                   Upper two-sided 95% CL for Pc = (Upper_2_95_CL_for_rc}

    headers = ['Concordance Results']
    table = []
    table.append(['Sample concordance correlation coefficient (pc) = ' + str(Lins_rc)[:6]])
    table.append(['Lower one-sided 95% CL for pc = ' + str(Lower_1_95_CL_for_rc)[:6]])
    table.append(['Lower two-sided 95% CL for pc = ' + str(Lower_2_95_CL_for_rc)[:6]])
    table.append(['Upper one-sided 95% CL for pc = ' + str(Upper_1_95_CL_for_rc)[:6]])
    table.append(['Upper two-sided 95% CL for pc = ' + str(Upper_2_95_CL_for_rc)[:6]])
    return tabulate(table, headers=headers, tablefmt="grid")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source_data",
        help="must be tilde (~) delimited.",
        type=str)
    args = parser.parse_args()
    concordance = calculate_concordance(args.source_data)
    print(concordance)

if __name__ == '__main__':
    main()
