#!/usr/bin/python
# -*- coding: utf-8 -*-

#Library of common functions
import json, urllib2, re, time, datetime, sys, cgi, os, string, random, math

#to enable debugging
import cgitb
# cgitb.enable()


   
    
# ########################## ##################        
# ########################## ##################
#
#        Financial functions
#
# ########################## ##################        

    
def ff_xirr(cf=[],dt=[]):
    #module to estimate X_IRR
    # inputs are a cash flow list, datelist

    # Model parameters
    low_rate = 0.01
    high_rate = 0.75
    max_iter = 1000
    prec_req = 0.00000001
    
    num_flows = len(cf)
    #ptest(( cf,dt,num_flows))
    
    # Initialize values
    i = 0
    j = 0
    m = 0.0
    xold = 0.00
    xnew = 0.00
    old_guess_rate = low_rate
    new_guess_rate = low_rate
    guess_rate = low_rate
    low_guess_rate = low_rate
    high_guess_rate = high_rate
    npv = 0.0
    denom = 0.0
 
    for i in range(0, max_iter):
        npv = 0.00
        for j in range(0,num_flows):
            #denom = math.pow((1+guess_rate),j)
            if j==0:
                time_interval = 0
            else:
                time_interval = (dt[j]-dt[0]).days / 365.0
            denom = math.pow((1+guess_rate),time_interval)
            npv = npv + (cf[j]/denom)
            #print i,j,time_interval,denom,npv

        # Stop checking once the required precision is achieved
        if ((npv > 0) and (npv < prec_req)): break
        
        if (xold == 0):
            xold = npv
        else:
            xold = xnew
            xnew = npv
     
        if (i > 0):
            if(xold < xnew):
                if(xold < 0 and xnew < 0):
                    high_guess_rate = new_guess_rate
                else:
                    low_guess_rate = new_guess_rate
            else:
                if(xold > 0 and xnew > 0):
                    low_guess_rate = new_guess_rate
                else:
                    high_guess_rate = new_guess_rate
           
        old_guess_rate = guess_rate
        guess_rate = (low_guess_rate + high_guess_rate) / 2.0
        new_guess_rate = guess_rate
         
    return guess_rate
    
       
