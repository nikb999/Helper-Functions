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



 
# ########################## ##################        
# ########################## ##################
#
#        Google Chart functions
#
# ########################## ##################        
# ########################## ##################        


def color_palette():
    # define the color palette.  
    #   First 5 colors are shades of blue - starting from dark blue to very light blue.
    #   second set of 5 colors are shades of orange.
    temp = " [\'#094d74\',\'#758cd8\',\'#9cd9d1\',\'#cfdaec\',\'#eef0f6\',\'#f6c7b6\', \'#f3b49f\',  \'#ec8f6e\', \'#e6693e\', \'#e0440e\' ] "
    
    return str(temp)
 
def google_chart_1_column(cht_title,xdata,ydata1):
    #this routine will draw a bar chart with two bara
    #print '<p>DO NOT PRINT anaything inside chart modules except needed items</p>'
    a = '''
        <!--Load the AJAX API   google chart 1 column -->
        <script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>
        <script type=\"text/javascript\">

        google.load(\'visualization\', \'1.0\', {\'packages\':[\'corechart\']}); 
    
        google.setOnLoadCallback(drawChart);
        function drawChart() {  
            var data = new google.visualization.arrayToDataTable([  
    '''
    abc1 = str(ydata1[0])
    b_y_1 = abc1[:abc1.find('(')]

    a +=  "[   \'Screen Name\', \' " + b_y_1 + "\'  ],"
    
    b = ''
    for cdi in range(len(xdata)):
        if cdi>0:
            b += "  [ \'" + str(xdata[cdi]) + "\'," +  str(ydata1[cdi]) + " ], "

    c =  "   ]); "
    c += "var options = {\'title\':\'" + cht_title + "\',"
    c += '''
                       \'width\':800,  
                       \'height\':400, 
                      \'hAxis\' : {\"logScale\" : false},
        '''
        
    d = 'colors:' + color_palette()  + ',' 
    e = 'legend :\"top\" , \"backgroundColor\": { fill: \"none\" } };  '
    f = 'var chart = new google.visualization.ColumnChart(document.getElementById(\"'+cht_title+'DIV'+'\")); '
    
    g = '''
            function selectHandler() {  
          var selectedItem = chart.getSelection()[0];  
          if (selectedItem) {  
            var topping = data.getValue(selectedItem.row, 0);  
            alert(\'The user selected \' + topping);  
          }  
        }  
        google.visualization.events.addListener(chart, \'select\', selectHandler);      
        chart.draw(data, options);  
      }  

    </script>  
    <!--Div that will hold the chart-->  
    '''
    h = '<div id=\"'+cht_title+'DIV'+'\" style=\"width:600; height:400\"></div>  '
 
    return a+b+c+d+e+f+g+h
 
 
def google_chart_combo(cht_title,xdata,ydata1,ydata2):
    #this routine will draw a bar chart with two bars
    #print '<p>DO NOT PRINT anaything inside chart modules except needed items</p>'
    a = '''
            <!--Load the AJAX API-  google chart combo -->
            <script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>
            <script type=\"text/javascript\">

            google.load(\'visualization\', \'1.0\', {\'packages\':[\'corechart\']}); 

            google.setOnLoadCallback(drawChart);
            function drawChart() {  
            var data = new google.visualization.arrayToDataTable([  
    '''
    
    abc1 = str(ydata1[0])
    b_y_1 = abc1[:abc1.find('(')]
    abc2 = str(ydata2[0])
    b_y_2 = abc2[:abc2.find('(')]
    
    b = "    [   \'Screen Name\', \' " + b_y_1 + "\' ,    \'" + b_y_2 + "\' ],        "
    
    c = ''
    for cdi in range(len(xdata)):
        if cdi>0:
            c += "  [ \'" + str(xdata[cdi]) + "\'," + str(ydata1[cdi]) + "," + str(ydata2[cdi]) + " ], "

    d = '    ]);  '

    #Set chart options
    e =  "var options = {\'title\':\'" + cht_title + "\',  "
    
    f = '''
                   \'width\':800,  
                   \'height\':400, 
                   \'hAxis\' : {\"logScale\" : false}  ,
                    seriesType: \"bars\",
                    series: {1: {type: \"line\"}},      
        '''
    g = 'colors:' + color_palette()  + ','
    h = 'legend :\"top\" , \"backgroundColor\": { fill: \"none\" }   };  '

    # chart_bottom():
    # Instantiate and draw our chart, passing in some options.

    i = 'var chart = new google.visualization.ComboChart(document.getElementById(\"'+cht_title+'DIV'+'\"));  '
    
    j = ''' 
              function selectHandler() {  
              var selectedItem = chart.getSelection()[0];  
              if (selectedItem) {  
                var topping = data.getValue(selectedItem.row, 0);  
                alert(\'The user selected \' + topping);  
                }  
              }  

            google.visualization.events.addListener(chart, \'select\', selectHandler);      
            chart.draw(data, options);  
            }  
            </script>  
            <!--Div that will hold the chart-->  
        '''
    k = '<div id=\"' + cht_title + 'DIV'+'\" style=\"width:600; height:400\"></div>  '
 
    return a+b+c+d+e+f+g+h+i+j+k


def google_chart_3_line(cht_title,xdata,ydata1,ydata2,ydata3):
    #this routine will draw a bar chart with two bara
    #print '<p>DO NOT PRINT anaything inside chart modules except needed items</p>'
    a = '''
        <!--Load the AJAX API  google chart 3 lines -->
        <script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>
        <script type=\"text/javascript\">
          google.load(\'visualization\', \'1.0\', {\'packages\':[\'corechart\']}); 
          google.setOnLoadCallback(drawChart);
          function drawChart() {  
            var data = new google.visualization.arrayToDataTable([  
        '''
    abc1 = str(ydata1[0])
    b_y_1 = abc1[:abc1.find('(')]
    abc2 = str(ydata2[0])
    b_y_2 = abc2[:abc2.find('(')]
    abc3 = str(ydata3[0])
    b_y_3 = abc3[:abc3.find('(')]
        
    # b =  "[ \'Screen Name\', \'" +str(ydata1[0]) + "\' , \'" +str(ydata2[0])+ "\' , \'"+str(ydata3[0])+ "\' ],"
    b =  "[ \'Screen Name\', \'" + b_y_1 + "\' , \'" + b_y_2 + "\' , \'"+ b_y_3 + "\' ],"

    c = ''
    for cdi in range(len(xdata)):
        if cdi>0:
            c += "  [ \'"+str(xdata[cdi])+ "\',"+str(ydata1[cdi])+","+str(ydata2[cdi])+","+str(ydata3[cdi])+" ],"

    d = ']);  '

    #Set chart options
    e = "var options = {\'title\':\'" + cht_title + "\', "
    
    e += '''\'width\':800,  
                       \'height\':400, 
                       \'hAxis\' : {\"logScale\" : false}  ,
                         seriesType: \"line\",
        '''
    f = 'colors:' + color_palette()  + ',' 
    
    g = '''
                       legend :\"top\" , \"backgroundColor\": { fill: \"none\" } };  
        '''
     
    h = 'var chart = new google.visualization.LineChart(document.getElementById(\"' + cht_title + 'DIV'+'\"));  '

    i = '''
            function selectHandler() {  
              var selectedItem = chart.getSelection()[0];  
              if (selectedItem) {  
                var topping = data.getValue(selectedItem.row, 0);  
                alert(\'The user selected \' + topping);  
              }  
            }  

            google.visualization.events.addListener(chart, \'select\', selectHandler);      
            chart.draw(data, options);  
          }  

        </script>  
        <!--Div that will hold the chart-->  
    '''

    j = '<div id=\"' + cht_title + 'DIV'+'\" style=\"width:600; height:400\"></div>  '

    return a+b+c+d+e+f+g+h+i+j
    
    
def google_chart_3_stacked_cols(cht_title,xdata,ydata1,ydata2,ydata3):
    #this routine will draw a bar chart with two bara
    #print '<p>DO NOT PRINT anaything inside chart modules except needed items</p>'
    
    a = '''
        <!--Load the AJAX API  google chart 3 stacked cols -->
        <script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>
        <script type=\"text/javascript\">

        google.load(\'visualization\', \'1.0\', {\'packages\':[\'corechart\']}); 

        google.setOnLoadCallback(drawChart);
        function drawChart() {  
        var data = new google.visualization.arrayToDataTable([  
    '''
    abc1 = str(ydata1[0])
    b_y_1 = abc1[:abc1.find('(')]
    abc2 = str(ydata2[0])
    b_y_2 = abc2[:abc2.find('(')]
    abc3 = str(ydata3[0])
    b_y_3 = abc3[:abc3.find('(')]

    # b = "[ \'Screen Name\', \' "+str(ydata1[0])+ "\' ,  \'" +str(ydata2[0])+ "\' , \'" +str(ydata3[0])+ "\' ], "
    b = "[ \'Screen Name\', \' "+b_y_1+ "\' ,  \'" +b_y_2+ "\' , \'" +b_y_3+ "\' ], "
    
    c = ''
    for cdi in range(len(xdata)):
        if cdi>0:
            c += "[ \'" +str(xdata[cdi])+ "\',"+str(ydata1[cdi])+","+str(ydata2[cdi])+","+str(ydata3[cdi])+ "],"

    d = ' ]); '

    #Set chart options
    e = "var options = {\'title\':\'"+cht_title+"\',  "

    f = '''
                      width:800,  
                       height:400, 
                       hAxis : {\"logScale\" : false}  ,
                       isStacked: true, 
        '''
    g = 'colors:' + color_palette()  + ',' 

    h = ' legend :\"top\" , \"backgroundColor\": { fill: \"none\" } };  '

    # chart_bottom():
    # Instantiate and draw our chart, passing in some options.
    i = ' var chart = new google.visualization.ColumnChart(document.getElementById(\"'+cht_title+'DIV'+'\"));  '

    j = '''
       function selectHandler() {  
          var selectedItem = chart.getSelection()[0];  
          if (selectedItem) {  
            var topping = data.getValue(selectedItem.row, 0);  
            alert(\'The user selected \' + topping);  
          }  
        }  

        google.visualization.events.addListener(chart, \'select\', selectHandler);      
        chart.draw(data, options);  
      }  

    </script>  
    <!--Div that will hold the chart-->  
        '''
    k = '<div id=\"'+ cht_title + 'DIV'+'\" style=\"width:600; height:400\"></div>  '

    return a+b+c+d+e+f+g+h+i+j+k


def google_chart_multi_stacked_cols(cht_title,xdata,ydata):
    #this routine will draw a bar chart with multiple stacked columns
    #print '<p>DO NOT PRINT anaything inside chart modules except needed items</p>'
    a = '''
        <!--Load the AJAX API  google chart multi stacked cols -->
        <script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>
        <script type=\"text/javascript\">

        google.load('visualization', '1', {packages: ['corechart', 'bar']});
        google.setOnLoadCallback(drawStacked);
        
            function drawStacked() {  
            var data = new google.visualization.arrayToDataTable([  
        '''


    b = '["'+str(xdata[0])+'"'

    c = ''
    for i in range(0,len(ydata)): c += ',"' + str(ydata[i][0])[:str(ydata[i][0]).find('(')]  + '" '
    
    d = '],'
    
    e = ''
    for i in range(1,len(xdata)):
        e += '["' + str(xdata[i]) + '"'
        for j in range(0,len(ydata)): e += ',' + str(ydata[j][i]) + ''
        e += ']'
        if i<len(xdata)-1: e += ","

    f = '    ]);  '
    #Set chart options
    
    g = "    var options = {\'title\':\'" + cht_title + "\',  "

    h = '''
            width: 800,
            height: 400,
            legend: { position: 'top', maxLines: 3 },
            bar: { groupWidth: '75%' },
        '''

    i = 'colors:' + color_palette()  + ',' 
    j = '''
            isStacked: true,
          };
        '''
    
    k = '     var chart = new google.visualization.ColumnChart(document.getElementById(\"'+ cht_title + '\"));'
    
    l = '''
            chart.draw(data, options);
            }
        </script>  
        <!--Div that will hold the chart-->  
        '''
    m = '<div id=\"'+cht_title+'\" style=\"width:800; height:400\"></div>  '

    return a+b+c+d+e+f+g+h+i+j+k+l+m

    
    #data should be like this for the stacked bar chart
        # var data = google.visualization.arrayToDataTable([
          # ['Year', 'Sales', 'Expenses', 'Profit'],
          # ['2014', 1000, 400, 200],
          # ['2015', 1170, 460, 250],
          # ['2016', 660, 1120, 300],
          # ['2017', 1030, 540, 350]
        # ]);


def google_chart_draw_histogram(xdata):
    #module to create a google histogram
    
    cht_title = "Net Gain"
    
    a = '''
        <!--Load the AJAX API  google charts draw histogram -->
        <script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>
        <script type=\"text/javascript\">

        <!-- Load the Visualization API and the piechart package. -->
        google.load(\'visualization\', \'1\', {\'packages\':[\'corechart\']}); 

        <!-- Set a callback to run when the Google Visualization API is loaded.-->
        google.setOnLoadCallback(drawChart);

        <!-- Callback that creates and populates a data table, -->
        <!--# instantiates the pie chart, passes in the data and-->
        <!--# draws it.-->
        function drawChart() {  

        <!--# Create the data table.-->
        var data = new google.visualization.arrayToDataTable([  
        [  \'Iteration\' , \'Net Gain\'  ],        
        '''
    
    b = ''

    for cdi in range(len(xdata)):
        itercdi = "Iter"+str(cdi)
        b = b + "  [ \'" + itercdi + "\' , " + str(xdata[cdi]) + " ], "

    c = '    ]);  '

    #Set chart options
    d1a = "var options = {\'title\':\'" + cht_title 
    d1b = '''\',  \'width\':600,                 \'height\':400, 
                    legend :\'none\' , \'backgroundColor\': { fill: \'none\' }  
                    };  

            <!--# chart_bottom():-->
            <!--# Instantiate and draw our chart, passing in some options.-->
        '''
    
    d1 = d1a + d1b

    d2 = 'var chart = new google.visualization.Histogram(document.getElementById(\"' + \
            cht_title + 'DIV\"));'  
    
    d3 = '''
            chart.draw(data, options);  
            }  

            </script>  
            <!--Div that will hold the pie chart-->  
        '''
    e = '<div id=\"' + cht_title + 'DIV' +'\" style=\"width:600; height:400\"></div>  '

    temp = a + b + c + d1 + d2 + d3 + e
    
    return temp
  
def gc_scatter(cht_title,xdata,ydata,xlabel,ylabel):
    #module to create a google histogram
    
    a = '''
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
          google.charts.load('current', {'packages':['corechart']});
          google.charts.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = google.visualization.arrayToDataTable([
        '''
    
    b = " [\'" + str(xlabel) + "\',\'" + str(ylabel) + "\'],"

    for cdi in range(len(xdata)):
        b += "  [ " + str(xdata[cdi]) + " , " + str(ydata[cdi]) + " ], "

    c = '    ]);  '

    #Set chart options
    d1a = "var options = {\'title\':\'" + str(cht_title) + "\'," + \
            "  hAxis: {title: \'" + str(xlabel) + "\'}," + \
            "  vAxis: {title: \'" + str(ylabel) + "\'},"

    d1b = '''
                \'width\':600, \'height\':400, 
                \'pointSize\':1, colors:[\'red\',\'#004411\'], 
                legend :\'none\' , \'backgroundColor\': { fill: \'none\' }  
                };  

            <!--# chart_bottom():-->
            <!--# Instantiate and draw our chart, passing in some options.-->
        '''
    
    d1 = d1a + d1b

    d2 = 'var chart = new google.visualization.ScatterChart(document.getElementById(\"' + \
            cht_title + 'DIV\"));'  
    
    d3 = '''
            chart.draw(data, options);  
            }  

            </script>  
            <!--Div that will hold the scatter chart-->  
        '''
    e = '<div id=\"' + cht_title + 'DIV' +'\" style=\"width:600; height:400\"></div>  '

    temp = a + b + c + d1 + d2 + d3 + e
    
    return temp
    
    
