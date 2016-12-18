#!/usr/bin/python
# -*- coding: utf-8 -*-

#Library of common functions
import json, urllib2, re, time, datetime, sys, cgi, os, string, random, math
import locale
import base64
import hashlib
import sqlite3
from tempfile import TemporaryFile

# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

from werkzeug.security import generate_password_hash, \
                              check_password_hash

#to enable debugging
import cgitb
# cgitb.enable()


def fix_str_code(instring=''):
    #fixes the strings with non-ascii characters
    # Assumption that the incoming strings are UTF-8 coded.
    #  First decode the string and then return unicode.
    #   Problem is created because python does not know what is the coding 
    #   for the incoming string and python27 by default assumes that it is ascii.
    try:
        temp = instring.decode('UTF-8')
    except:
        temp = 'ERROR'
    
    return unicode(temp)
    
def str_unic(instring=''):
    # module that returns either the unicode or string of the instring.
    # needed in some functions where the incoming variable is unicode with non-ascii 
    # characters.  Str() does not work on those.  They need to be returned as unicode.
    temp = 'ERROR'
    try:
        temp = str(instring)
    except:
        temp = unicode(instring)
    
    return temp


def pretty_print_v2(mat_in=[],negpos='pos'):
    #assumes the first element of the matrix is a string and rest are numbers
    #assumes only one row
    locale.setlocale(locale.LC_NUMERIC, '')
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

    out_res = " "
    negposfactor = 1.0
    if negpos.upper()=='NEG': negposfactor = -1.0

    for x in range(0,len(mat_in)): 
        alignvar = "right"
        if x == 0: alignvar = "left"
        if is_number(mat_in[x]):
            temp = negposfactor * mat_in[x]
            if abs(temp)<100:
                num_str = locale.format("%.2f",temp,grouping=True)
                out_res = out_res + '<td align=' + alignvar + '><sm>' + num_str + '</sm></td>' 
            else:
                num_str = locale.format("%.0f",temp,grouping=True)
                out_res = out_res + '<td align=' + alignvar + '><sm>' + num_str + '</sm></td>' 
        else:
            try:
                out_res = out_res +  '<td align=' + alignvar + '><sm>' + str_unic(mat_in[x]) + '</sm></td>'
            except:
                out_res = out_res +  '<td align=' + alignvar + '><sm>' + 'ERROR: ' + str(x) + '</sm></td>'

    return out_res
            
def string_print_v2(mat_in=[]):
    #assumes all element of the matrix are string
    #assumes only one row
    temp = ''
    for x in range(0,len(mat_in)): 
        temp += '<td><sm>' + str_unic(mat_in[x]) + '</sm></td>'
    
    return temp
    
def blank_row_print_v2(msg_in='',nn_in=1):
    #prints a blank row with nn columns and the incoming msg
    nn_col = int(nn_in)
    temp =  '<tr style="w3-border-top"><td colspan='+ str_unic(nn_col) + '><sm>' + str(msg_in) + '</sm></td></tr>'

    return temp
       

def print_table_full_v2(intable):
    #module to print a table
    # intable is the table comes in a list format [ [row1], [row2] ]
    #
    a = '<table class="w3-table w3-small w3-bordered w3-border w3-striped" style="width:80%; display: block;">'
    b = ' '
    for arow in intable: 
        abc = ''
        negpos = 'pos'
        temp = pretty_print_v2(arow,negpos)
        b = b + ' <tr' + abc + '> ' + \
                str_unic(temp) + \
                ' </tr> '

    c = '</table>'
    d = '<p style=\"page-break-before: always\"> </p>'
    
    return a + b + c + d

def print_table_w_header(hrow=[],intable=[]):
    #module to print a table, header row is separate than the rest of the table
    # hrow - comes in a list format.
    # intable is the table comes in a list format [ [row1], [row2] ]
    #
    a = '<table class="w3-table w3-small w3-bordered w3-border w3-striped" style="width:80%; display: block;">'
    b = ' '

    negpos = 'pos'
    temp = pretty_print_v2(hrow,negpos)
    b = b + ' <tr> ' + \
            str_unic(temp) + \
            ' </tr> '

    # check if the incoming table is a list or unicode string
    if type(intable)==list:
        pass
    else:
        intable = eval(intable)
    
    for arow in intable: 
        abc = ''
        negpos = 'pos'
        try:
            temp = pretty_print_v2(arow,negpos)
        except:
            temp = 'ERROR'
        b = b + ' <tr' + abc + '> ' + \
                str_unic(temp) + \
                ' </tr> '

    c = '</table>'
    d = '<p style=\"page-break-before: always\"> </p>'
    
    return a + b + c + d
    
    

            
def print_table_rows_v2(intable):
    #module to print a table
    # intable is the table comes in a list format [ [0/1/2,rowlist,neg/pos], [0/1/2,rowlist,neg/pos] ]
    #   if the first item in the list is 1 - then shade, otherwise no shade
    #   if the first item in the list is 2 - then do not print the row.
    #   only table rows are printed... table start and end are not printed here.
    #
    ptrv2 = ''
    for arow in intable: 
        abc = ''
        if int(arow[0])==1: abc = ' class="w3-light-grey"'
        negpos = 'pos'
        try: arow[2]
        except KeyError:
            negpos='pos'
        else:
            if str(arow[2]).upper()=='NEG': negpos='neg'
        
        if int(arow[0])<=1: 
            ptrv2 = ptrv2 + '<tr' + abc + '>' + \
                    str(pretty_print_v2(arow[1],negpos)) + \
                    '</tr>'
            
    
    return ptrv2
    
       
def is_number(s=0):
    try:
        float(s)
        return True
    except ValueError:
        return False
   

    


def selection_choice(tempname='',invalue=1, a=1, b=1, c=1, d='', ml=0):
    #incoming variables - this creates a list of values from 'a' to 'b' with step = 'c'
    # a,b,c are integers
    locale.setlocale(locale.LC_NUMERIC, '')
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

    # process to deal with increments less than 1.
    inc_mult = 100
    a1=int(inc_mult*a)
    b1=int(inc_mult*b)
    c1=int(inc_mult*c)
    
    num_fmt = "%.0f"
    if c<1: num_fmt="%.2f"
    
    sc1 = '<select name=\"'+tempname+'\" >'
    for i1 in range(a1,b1,c1):
        if ( float(i1) == float(invalue*inc_mult) ):
            sc1 = sc1 + '\n <option value='+str(float(1.0*i1/inc_mult))+' selected>'+str(locale.format(num_fmt,float(1.0*i1/inc_mult),grouping=True))+' '+mt(str(d),ml)+' </option>'
        else:
            sc1 = sc1 + '\n <option value='+str(float(1.0*i1/inc_mult))+'>'+str(locale.format(num_fmt,float(1.0*i1/inc_mult),grouping=True))+' '+mt(str(d),ml)+' </option>'
    
    sc1 = sc1 + ' </select>\n'
    return sc1

def selection_list(tempname='',selected_val=0, inlist=[],ml=0):
    sc1 = '<select name=\"'+tempname+'\">'
    invalues = inlist[1]
    intext = inlist[2]
    for i1 in range(0,len(invalues)):
        if ( float(invalues[i1]) == float(selected_val) ):
            sc1 = sc1 + '\n <option value='+str(invalues[i1])+' selected>'+str(mt(intext[i1],ml))+' </option>'
        else:
            sc1 = sc1 + '\n <option value='+str(invalues[i1])+'>'+str(mt(intext[i1],ml))+' </option>'
    
    sc1 = sc1 + ' </select>\n'
    return sc1

def selection_list_text(tempname='', selected_val='', inlist=[],ml=0):
    sc1 = '<select name=\"'+tempname+'\">'
    invalues = inlist[1]
    intext = inlist[2]
    for i1 in range(0,len(invalues)):
        if ( str(intext[i1]) == str(selected_val) ):
            sc1 = sc1 + '\n <option value=\"'+str(intext[i1])+'\" selected>'+str(mt(intext[i1],ml))+' </option>'
        else:
            sc1 = sc1 + '\n <option value=\"'+str(intext[i1])+'\">'+str(mt(intext[i1],ml))+' </option>'
    
    sc1 = sc1 + ' </select>\n'
    return sc1

    
def selection_list_mult(tempname='',selected_val=0, inlist=[],ml=0):
    sc1 = '<select multiple name=\"'+tempname+'\">'
    invalues = inlist[1]
    intext = inlist[2]
    for i1 in range(0,len(invalues)):
        a = invalues[i1]
        b = selected_val
        if type(b) is list:
            # if the selected values are in a list then check if the invalue is in the list 
            if a in b or unicode(a) in b:
                sc1 = sc1 + '\n <option value='+str(invalues[i1])+' selected>'+str(mt(intext[i1],ml))+' </option>'
            else:
                sc1 = sc1 + '\n <option value='+str(invalues[i1])+'>'+str(mt(intext[i1],ml))+' </option>'         
        else:
            if ( float(a) == float(b) ):
                sc1 = sc1 + '\n <option value='+str(invalues[i1])+' selected>'+str(mt(intext[i1],ml))+' </option>'
            else:
                sc1 = sc1 + '\n <option value='+str(invalues[i1])+'>'+str(mt(intext[i1],ml))+' </option>'
    
    sc1 = sc1 + ' </select>\n'
    return sc1
    

def create_var_list_table_v2(inlist,ml,str_val,num_cols):
    #Module to create a table for a bunch of variables.
    #v1 is the variable list.  ml = language, str_val is the incoming list of variable values.
    
    cv1 = '<table class="w3-table w3-small w3-bordered w3-border" style="width: 80%; display: block;">'
    cv2 = '    '
    
    i=0
    for avar in inlist:
        if i%(num_cols/2)==0: 
            # a = ' <tr bgcolor=#f5f5f5><td><sm>'+ mt(avar[1],ml) + '</sm></td>'
            a = '\n <tr><td>'+ mt(avar[1],ml) + '</td>'
            e = '   '
        else:
            a = '       <td>'+ mt(avar[1],ml) + '</td>'
            e = ' </tr>'
        b = ' <td>'       
        if avar[2][0]=='open':
            c = ' <INPUT type=text size=\"12\" value=\"'+str(str_val[avar[0]])+'\"name=\"'+avar[0]+'\">'
        elif avar[2][0]=='closed':
            c = '&nbsp;'
        elif avar[2][0]=='sc':
            c = selection_choice(avar[0],float(str_val[avar[0]]),avar[2][1],avar[2][2],avar[2][3],avar[2][4],ml)
        elif avar[2][0]=='ls':
            c = selection_list(avar[0],float(str_val[avar[0]]),avar[2],ml)
        elif avar[2][0]=='ls_mult':
            c = selection_list_mult(avar[0],float(str_val[avar[0]]),avar[2],ml)
        else:
            c = '&nbsp'
        d = ' </td>\n'
        cv2 = cv2 + a+b+c+d+e
        i=i+1
                        
    cv3 = '     </table>\n'
    
    return cv1 + cv2 + cv3
    
 

def table_of_variables_v2(numrows,table_to_print,str_val,mlang):
    # module to create a full table of variables.
    # incoming - number of rows, table to print and initial values, language
    #           v2 --- fixes the issue with the first variable starting with _000 - which then does not get checked by formValidate().

    temp = list()
    
    temp.append('<div class="w3-responsive"><table class="w3-table w3-small w3-bordered w3-border" style="width:100%; display: block;">')
    
    # do the header row
    temp.append('<tr><thead class="w3-light-grey">')
    
    for i in range(0,len(table_to_print)): temp.append('<td>'+table_to_print[i][0]+'</td>')
    
    temp.append('</thead></tr>')
    
    # do the other rows
    for j in range(0,numrows):
        temp.append('\n<tr>')
        for i in range(0,len(table_to_print)): 
            row_data_type = table_to_print[i][2]
            if row_data_type =='text':
                t_val = table_to_print[i][0] + '-' + str(j+1)
                t_varname = table_to_print[i][1] + '%03d' %(j+1) + '_000'
            elif row_data_type =='date':
                t_val = '01/01/2000'
                t_varname = table_to_print[i][1] + '%03d' %(j+1) + '_000'            
            else:
                t_val = 0
                t_varname = table_to_print[i][1] + '_' + '%03d' %(j+1)

            try: str_val[t_varname]
            except KeyError:
                t_val = t_val
            else:
                t_val=str_val[t_varname]

            t_vt = table_to_print[i][3]
            b = '<td> '       
            if t_vt[0]=='open':
                if str(row_data_type)=='number':
                    c = '\n <INPUT type=\"number\" step=\"any\" size=\"12\" value=\"'+str_unic(t_val)+'\" name=\"'+t_varname+'\">'
                else:
                    try:
                        c = '\n <INPUT type='+str(row_data_type)+' size=\"12\" value=\"'+str_unic(t_val)+'\" name=\"'+t_varname+'\">'
                    except:
                        c = '\n <INPUT type='+str(row_data_type)+' size=\"12\" value=\"' + t_val.encode('utf-8') + '\" name=\"'+t_varname+'\">'
            elif t_vt[0]=='temp_closed':
                c = '\n <INPUT type=hidden value=\"'+str_unic(t_val)+'\" name=\"'+t_varname+'\">'
            elif t_vt[0]=='closed':
                c = '&nbsp;'
            elif t_vt[0]=='sc':
                c = selection_choice(t_varname,t_val,t_vt[1],t_vt[2],t_vt[3],t_vt[4],mlang)
            elif t_vt[0]=='ls':
                c = selection_list(t_varname,t_val,t_vt,mlang)
            elif t_vt[0]=='ls_mult':
                c = selection_list_mult(t_varname,t_val,t_vt,mlang)
            elif t_vt[0]=='ls_text':
                c = selection_list_text(t_varname,t_val,t_vt,mlang)
            else:
                c = table_to_print[i][0] + '&nbsp;' + str(j+1)
                
            d = ' </td>\n'
            try:
                bcd = b + c + d
            except:
                bcd = b + c.encode('utf-8') + d
                
            temp.append(bcd)
                
        temp.append('</tr>\n')
    
    
    temp.append('</table></div>\n')
    temp2 = ' '.join(temp)
    
    return temp2


    
