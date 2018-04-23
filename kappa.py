#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import math


def calculate_kappa(Npp_param, Npa_param, Nap_param, Naa_param, kappatest_param):
    """Created march 2003 by G.W.Payne
       Kappa calculator as described by Mr Graham McBride in Evaluation of Colilert Procedures
       Using Cohen's "Kappa" Statistic As The Measure Of Agreement With A Standard.
    """

    #define all the variables used
    n = 0  #number pairs
    Npp = float(0)
    Npa = float(0)
    Nap = float(0)
    Naa = float(0)
    #a,b,c,d are cell frequencies
    a = float(0)  #Npp/n
    b = float(0)  #Npa/n
    c = float(0)  #Nap/n
    d = float(0)  #Naa/n
    #p1,p2 row frequencies, q1,q2 column frequencies
    p1 = float(0)  #a+b
    p2 = float(0)  #a+c
    q1 = float(0)  #c+d
    q2 = float(0)  #b+d
    #po, pe observed and chance-expected agreement frequencies
    po = float(0)  #a+d
    pe = float(0)  #p1*p2 + q1*q2
    kappatest = float(0)  #test value of kappa between 0 and 1
    #estmated Kappa value - k is used to shorten expressions later
    kappahat = float(0)  #(po-pe)/(1.-pe)
    k = float(0)  #kappahat
    kappaplus = float(0)  #(a-p1*p2)/(p1-p1*p2)
    kappaminus = float(0)  #(d-q1*q2)/(q1-q1*g2)
    #Standard error for test of zero kappa (Fleiss)
    denom = float(0)  #(1.-pe)*sqrt(N)
    numer = float(0)  #sqrt(pe+pe**2-p1*p2*(p1+p2)-q1*q2*(q1+q2)
    se0 = float(0)  #numer/denom
    #Standard error test of non zero kappa (Fleiss, eqs 12.15-13.18)
    capA = float(0)  #a*(1.-(p1+p2)*(1.-k))**2+d*(1.-(q1+q2)*(1.-k))**2
    capB = float(0)  #((1.-k)**2) * (b*(p2+q1)**2+c*(p1+q2)**2)
    capC = float(0)  #(k-pe*(1.-k))**2
    sek = float(0)  #(sqrt(capA+capB-capC))/denom
    #Standard error test of non zero Kappa (Bishop et al 1975 eq 11.4-4,5,6)
    #theta3 = float(0)  #a*(p1+p2)+d*(q1+q2)
    #theta4 = float(0)  #a*(p1+p2)**2+b*(p2+q1)**2+c*(p1+q2)**2+d(q1+q2)**2
    #E = float(0)  #po*(1.-po)
    #F = float(0)  #2.*(1-po)*2.*po*pe-thetha3)/(1.-pe)
    #G = float(0)  #((1.-po)**2)*(theta4-4.*pe**2)/(1.-pe)**2
    # sekB=float(0)                   #sqrt((E+F+G))/denom - gives same result as sek, not used
    z = float(0)  #kappahat/se0
    p = float(0)  #1.-PROBN(z) kappa=<0

    if Npp_param == "" or Npa_param == "" or Nap_param == "" or Naa_param == "" or kappatest_param == "":
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>At least one of the fields is blank</td></tr>'
        return_string = return_string + '<tr><td>Use the back button to go back to the input page to correct and try again</td></tr>'
        return_string = return_string + '</table>'
        return return_string
    Npp = float(Npp_param)
    Npa = float(Npa_param)
    Nap = float(Nap_param)
    Naa = float(Naa_param)
    kappatest = float(kappatest_param)

    # all output lines are indicated by #* at beginning

    #estimated kappas (k is used later to shorten expressions
    n = Npp + Npa + Nap + Naa
    a = Npp / float(n)
    b = Npa / n
    c = Nap / n
    d = Naa / n
    #p1,p2 row frequencies, q1,q2 column frequencies
    p1 = a + b
    p2 = a + c
    q1 = c + d
    q2 = b + d
    #po, pe observed and chance-expected agreement frequencies
    po = a + d
    pe = p1 * p2 + q1 * q2
    #check for special cases
    #b=c=d=0
    if Npa == 0 and Nap == 0 and Naa == 0:
        #Write
        #*Perfect agreement (all rating pairs are "present")
        #*kappahat, kappa+ and kappa- are all undefined.
        #*No tests can be performed.
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Perfect agreement (all rating pairs are "present")</td></tr>'
        return_string = return_string + '<tr><td>kappahat, kappa+ and kappa- are all undefined.</td></tr>'
        return_string = return_string + '<tr><td>No tests can be performed.</td></tr></table>'
        return return_string
#a=b=c=0
    if Npp == 0 and Npa == 0 and Nap == 0:
        #Write
        #*Perfect agreement (all rating pairs are "absent")
        #*kappahat, kappa+ and kappa- are all undefined.
        #*No tests can be performed.
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Perfect agreement (all rating pairs are "absent")</td></tr>'
        return_string = return_string + '<tr><td>kappahat, kappa+ and kappa- are all undefined.</td></tr>'
        return_string = return_string + '<tr><td>No tests can be performed.</td></tr></table>'
        return return_string
#a=c=d=0
    if Npp == 0 and Nap == 0 and Naa == 0:
        #Write
        #*Perfect disagreement (all rating pairs are "present"/"absent")
        #*kappahat = kappa+ = 0 (= minimum value in this case), but kappa- is undefined.
        #*No tests performed.
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Perfect disagreement (all rating pairs are "present"/"absent")</td></tr>'
        return_string = return_string + '<tr><td>kappahat = kappa+ = 0 (= minimum value in this case), but kappa- is undefined.</td></tr>'
        return_string = return_string + '<tr><td>No tests performed.</td></tr></table>'
        return return_string
#a=b=d=0
    if Npp == 0 and Npa == 0 and Naa == 0:
        #Write
        #*Perfect disagreement (all rating pairs are "absent"/"present")
        #*kappahat = kappa- = 0 (= minimum value in this case), but kappa+ is undefined.
        #*No tests performed.
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Perfect disagreement (all rating pairs are "present"/"absent")</td></tr>'
        return_string = return_string + '<tr><td>kappahat = kappa- = 0 (= minimum value in this case), but kappa+ is undefined.</td></tr>'
        return_string = return_string + '<tr><td>No tests performed.</td></tr></table>'
        return return_string
#b=d=0
    if Npp != 0 and Npa == 0 and Nap != 0 and Naa == 0:
        #Write
        #*Rater B has marked all tests as "present"; rater A has "present" and "absent".
        #*In this case kappahat = kappa- = 0  but kappa+ is undefined.
        #*No tests are performed.
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Rater B has marked all tests as "present"; rater A has "present" and "absent".</td></tr>'
        return_string = return_string + '<tr><td>In this case kappahat = kappa- = 0  but kappa+ is undefined.</td></tr>'
        return_string = return_string + '<tr><td>No tests are performed.</td></tr></table>'
        return return_string
#a=c=0
    if Npp == 0 and Npa != 0 and Nap == 0 and Naa != 0:
        #write
        #*Rater B has marked all tests as "absent"; rater A has "present" and "absent".
        #*In this case kappahat = kappa+ = 0  but kappa- is undefined.
        #*No tests performed.
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Rater B has marked all tests as "absent"; rater A has "present" and "absent".</td></tr>'
        return_string = return_string + '<tr><td>In this case kappahat = kappa+ = 0  but kappa- is undefined.</td></tr>'
        return_string = return_string + '<tr><td>No tests performed.</td></tr></table>'
        return return_string
#c=d=0
    if Npp != 0 and Npa != 0 and Nap == 0 and Naa == 0:
        #write
        #*Rater A has marked all tests as "present"; rater B has "present" and "absent".
        #*In this case kappahat = kappa+ = 0  but kappa- is undefined.
        #*No tests are performed.
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Rater A has marked all tests as "present"; rater B has "present" and "absent".</td></tr>'
        return_string = return_string + '<tr><td>In this case kappahat = kappa+ = 0  but kappa- is undefined.</td></tr>'
        return_string = return_string + '<tr><td>No tests performed.</td></tr></table>'
        return return_string
#a=b=0
    if Npp == 0 and Npa == 0 and Nap != 0 and Naa != 0:
        #write
        #*Rater A has marked all tests as "absent"; rater B has "present" and "absent".
        #*In this case kappahat = kappa- = 0  but kappa+ is undefined.
        #*No tests are performed.
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Rater A has marked all tests as "absent"; rater B has "present" and "absent".</td></tr>'
        return_string = return_string + '<tr><td>In this case kappahat = kappa- = 0  but kappa+ is undefined.</td></tr>'
        return_string = return_string + '<tr><td>No tests performed.</td></tr></table>'
        return return_string
#b=c=0
    if Npa == 0 and Nap == 0 and Naa != 0 and Npp != 0:
        #write
        #*Perfect agreement (some rating pairs are "present", all others are "absent").
        #*In this case kappahat = kappa+ = kappa- = 1.
        #*No tests performed.
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Perfect agreement (some rating pairs are "present", all others are "absent").</td></tr>'
        return_string = return_string + '<tr><td>In this case kappahat = kappa+ = kappa- = 1.</td></tr>'
        return_string = return_string + '<tr><td>No tests performed.</td></tr></table>'
        return return_string

#test print
#print 'n = ',n
#print 'Npp = ',Npp
#rint 'Npa = ',Npa
#print 'Nap = ',Nap
#print 'Naa = ',Naa
#print 'a = ',a
#print 'b = ',b
#print 'c = ',c
#print 'd = ',d
#print 'p1 = ',p1
#print 'p2 = ',p2
#print 'q1 = ',q1
#print 'q2 = ',q2
#print 'po = ',po
#print 'pe = ',pe

#estmated Kappa value - k is used to shorten expressions later
    kappahat = (po - pe) / (1. - pe)
    k = kappahat
    kappaplus = (a - p1 * p2) / (p1 - p1 * p2)
    kappaminus = (d - q1 * q2) / (q1 - q1 * q2)
    #a=d=0
    if Npp == 0 and Naa == 0 and Nap != 0 and Npa != 0:
        #write
        #*Perfect disagreement (some rating pairs are "present/absent", all others are "absent/present").
        #*If there are equal numbers of both then kappahat = kappa+ =kappa- = -1, otherwise
        #*kappahat is between 0 and -1 and is straddled by kappa+ and kappa-.
        #*No tests performed. For the record  kappahat = {kappahat}, kappa+ = {kappaplus}, kappa- = {kappaminus}
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Perfect disagreement (some rating pairs are "present/absent", all others are "absent/present").</td></tr>'
        return_string = return_string + '<tr><td>If there are equal numbers of both then kappahat = kappa+ = kappa- = -1, otherwise</td></tr>'
        return_string = return_string + '<tr><td>kappahat is between 0 and -1 and is straddled by kappa+ and kappa-.</td></tr></table>'
        return_string = return_string + '<tr><td>No tests performed. For the record  kappahat = ' + str(
            kappahat)[:6] + ', kappa+ = ' + str(
                kappaplus)[:6] + ', kappa- = ' + str(
                    kappaminus)[:6] + '</td></tr>'
        return_string = return_string + '</table>'
        return return_string

#test kappa value make sure between 0 and 1
    if kappatest < 0 or kappatest >= 1:
        #Write
        #*Kappatest must be greater than or equal to zero and less than 1.
        #*Use the back button to go back to the input page to correct.
        return_string = '<table class="display_data"><tr><th>Info</th></tr><tr><td>Kappatest must be greater than or equal to zero and less than 1.</td></tr>'
        return_string = return_string + '<tr><td>Use the back button to go back to the input page to correct and try again</td></tr>'
        return_string = return_string + '</table>'
        return return_string


#Standard error for test of zero kappa (Fleiss)
    denom = (1. - pe) * math.sqrt(n)
    numer = math.sqrt(pe + pe**2 - p1 * p2 * (p1 + p2) - q1 * q2 * (q1 + q2))
    se0 = numer / denom
    #Standard error test of non zero kappa (Fleiss, eqs 12.15-13.18)
    capA = a * (1. - (p1 + p2) * (1. - k))**2 + d * (1. - (q1 + q2) *
                                                     (1. - k))**2
    capB = ((1. - k)**2) * (b * (p2 + q1)**2 + c * (p1 + q2)**2)
    capC = (k - pe * (1. - k))**2
    sek = (math.sqrt(capA + capB - capC)) / denom
    #Standard error test of non zero Kappa (Bishop et al 1975 eq 11.4-4,5,6)
    #theta3 = a * (p1 + p2) + d * (q1 + q2)
    #theta4 = a * (p1 + p2)**2 + b * (p2 + q1)**2 + c * (p1 + q2)**2 + d * (
    #    q1 + q2)**2
    #E = po * (1. - po)
    #F = 2. * (1 - po) * (2. * po * pe - theta3) / (1. - pe)
    #G = ((1. - po)**2) * (theta4 - 4. * pe**2) / (1. - pe)**2
    # sekB gives same result as sek, not used
    # sekB=math.sqrt((E+F+G))/denom

    #print 'n = ',n
    #print 'Npp = ',Npp
    #print 'Npa = ',Npa
    #print 'Nap = ',Nap
    #print 'Naa = ',Naa
    #print 'Kappahat = ',kappahat
    #print 'Kappaplus = ',kappaplus
    #print 'Kappaminus = ',kappaminus
    #print 'se0 = ',sezero
    #print 'sek = ',sek
    #print 'z = ',z
    #print 'p1 = ',p

    #write out results - write out all lines below that start with #*, items in {} are variables to be written

    #*RESULTS FOR 2x2 INTERRATER TABLE
    #*
    #*Rater A |       Rater B      |
    #*        | present    absent  |
    #*--------|--------------------|
    #*present |  {Npp}      {Npa}  |
    #*absent  |  {Nap}      {Naa}  |
    #*--------|--------------------|
    #*
    #*kappahat = {kappa},  (kappa+ = {kappaplus}. kappa- = {kappaminus}
    #*s.e.(0) = {se0},  s.e.(kappahat) = {sek}
    #*
    #*HYPOTHESIS TEST p-VALUES
    #*One-sided test, H0 is kappa =<0
    return_string = '<h2>Results for 2x2 Interrater table</h2>'
    return_string = return_string + '<table class="display_data"><tr><th>Rater A</th><th colspan="2">Rater B</th></tr>'
    return_string = return_string + '<tr><th></th><th>present</th><th>absent</th></tr>'
    return_string = return_string + '<tr><th>present</th><td>' + str(
        int(Npp)) + '</td><td>' + str(int(Npa)) + '</td></tr>'
    return_string = return_string + '<tr><th>absent</th><td>' + str(
        int(Nap)) + '</td><td>' + str(int(Naa)) + '</td></tr>'
    return_string = return_string + '</table>'

    return_string = return_string + '<table class="display_data"><tr><td>kappahat = ' + str(
        kappahat)[:6] + ',  (kappa+ = ' + str(
            kappaplus)[:6] + '. kappa- = ' + str(kappaminus)[:6] + ')</td></tr>'
    return_string = return_string + '<tr><td>s.e.(0) = ' + str(
        se0)[:6] + ',  s.e.(kappahat) = ' + str(sek)[:6] + '</td></tr>'
    return_string = return_string + '<tr><th>&nbsp;</th></tr>'
    return_string = return_string + '<tr><th>Hypothesis test p-values</th></tr>'
    return_string = return_string + '<tr><td>One-sided test, H0 is kappa =<0</td></tr>'

    z = kappahat / se0
    p = 1. - probn(z)
    if p < 0.0001:
        return_string = return_string + '<tr><td>p = Prob[>kappahat, given that kappa=0] < 0.0001</td></tr>'
    elif p > 0.9999:
        return_string = return_string + '<tr><td>p = Prob[>kappahat, given that kappa=0] > 0.9999</td></tr>'
    else:
        return_string = return_string + '<tr><td>p = Prob[>kappahat, given that kappa=0] = ' + str(
            p)[:6] + '</td></tr>'

    #*
    #*One-sided test, H0 is kappa =< {kappatest}
    return_string = return_string + '<tr><th>&nbsp;</th></tr><tr><td>One-sided test, H0 is kappa =< ' + str(
        kappatest)[:4] + '</td></tr>'
    z = (kappahat - kappatest) / sek
    p = 1 - probn(z)
    if p < 0.0001:
        return_string = return_string + '<tr><td>p = Prob[>kappahat, given that kappa= ' + str(
            kappatest)[:6] + '] < 0.0001</td></tr>'
    elif p > 0.9999:
        return_string = return_string + '<tr><td>p = Prob[>kappahat, given that kappa= ' + str(
            kappatest)[:6] + '] > 0.9999</td></tr>'
    else:
        return_string = return_string + '<tr><td>p = Prob[>kappahat, given that kappa= ' + str(
            kappatest)[:6] + '] = ' + str(p)[:6] + '</td></tr>'

    #*
    #*Two-sided test, H0 is kappa={kappatest}
    return_string = return_string + '<tr><th>&nbsp;</th></tr><tr><td>Two-sided test, H0 is kappa= ' + str(
        kappatest)[:6] + '</td></tr>'
    z = abs(kappahat - kappatest) / sek
    p = 2. * (1. - probn(z))
    if p < 0.0001:
        return_string = return_string + '<tr><td>p = Prob[>|kappahat-kappa|, given that kappa= ' + str(
            kappatest)[:6] + '] < 0.0001</td></tr>'
    elif p > 0.9999:
        return_string = return_string + '<tr><td>p = Prob[>|kappahat-kappa|, given that kappa= ' + str(
            kappatest)[:6] + '] > 0.9999</td></tr>'
    else:
        return_string = return_string + '<tr><td>p = Prob[>|kappahat-kappa|, given that kappa= ' + str(
            kappatest)[:6] + '] = ' + str(p)[:6] + '</td></tr>'
    return_string = return_string + '</table>'
    return return_string


def probn(z):
    w = abs(z) / math.sqrt(2.)
    y = 1. / (1. + 0.5 * w)
    erfcc = y * math.exp(-w * w - 1.26551223 + y * (1.00002368 + y * (
        0.37409196 + y * (0.09678418 + y *
                          (-0.18628806 + y *
                           (0.27886807 + y *
                            (-1.13520398 + y *
                             (1.48851587 + y *
                              (-0.82215223 + y * 0.17087277)))))))))

    if z < 0.0:
        erfcc = 2. - erfcc
    probn = 1.0 - 0.5 * erfcc
    return probn

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--npp", help="number of present/present ratings", type=float, required=True, metavar=0.0)
    parser.add_argument("--npa", help="number of present/absent ratings", type=float, required=True, metavar=0.0)
    parser.add_argument("--nap", help="number of absent/present ratings", type=float, required=True, metavar=0.0)
    parser.add_argument("--naa", help="number of absent/absent ratings", type=float, required=True, metavar=0.0)
    parser.add_argument("--kappatest", help="test value of kappa (must be >= 0 and < 1", type=float, required=True, metavar=0.0)
    args = parser.parse_args()
    kappa = calculate_kappa(args.npp, args.npa, args.nap, args.naa, args.kappatest)
    print(kappa)

if __name__ == '__main__':
    main()
