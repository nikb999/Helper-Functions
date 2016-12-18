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
#        LOGIN and ACCT Maintenance Functions
#
# ########################## ##################        
# ########################## ##################        

def generate_session():
    return base64.b32encode(os.urandom(16))[0:22]

def generate_regcode():
    return base64.b32encode(os.urandom(4))[0:6]

def login_hash_pswd(key_string):
    #key_string has the password that comes in.
    salt='someTHINGrandomHERE'
    hash=hashlib.md5(salt+key_string).hexdigest()
    #print "%s : %s" % (salt, hash) 
    return hash
    
# Define function to generate HTML form.
def login_login_form_big(action_file):
    # Assumes that HTML and FORM have already started.
    print '<table class="w3-table w3-small"  style="width:50%; display: block;">'

    print '<TR><thead><Td align=left>Username</TD><Td align=left>Password</TD></thead></tr>'
    print '<tr>'
    print '<TD><INPUT TYPE = text NAME = \"login_user_000\"></TD>'
    print '<TD><INPUT TYPE = password NAME = \"login_pass_000\"></TD>'
    print '</tr>'
    print "</TABLE>"
    print '<INPUT TYPE = submit NAME = \"form_action_000\" VALUE = \"LogIN\" >'
    print 'Press <a href="./acct_tools.py">here</a> here if you do not have an account or if you forgot your password.'
    print '<p><hr></p>'

def login_login_form(action_file):
    # Assumes that HTML and FORM have already started.
    #print '<a href="./acct_tools.py"><span style=\"color:white;"\> Register </span></a></span>'
    print '<a class="w3-btn w3-white w3-round" href="./acct_tools.py">Register</a></span>'
    print '&nbsp; &nbsp;'
    print '<INPUT class=\"w3-white w3-round\" TYPE = text size="20" placeholder=\"Username\" NAME = \"login_user_000\">'
    print '<INPUT class=\"w3-white w3-round\" TYPE = password size = "20" placeholder=\"Password\" NAME = \"login_pass_000\">'
    print '&nbsp; &nbsp;'
    print '<INPUT class="w3-btn w3-white w3-round" TYPE = submit NAME = \"form_action_000\" VALUE = \"LogIN\" >'

def login_login_form_v2(action_file):
    # Assumes that HTML and FORM have already started.
    #print '<a href="./acct_tools.py"><span style=\"color:white;"\> Register </span></a></span>'
    print '''
            <a  class="w3-wide" onclick="document.getElementById('login_modal_id').style.display='block'">SIGN IN</a>

            <div id="login_modal_id" class="w3-modal">
                <div class="w3-modal-content w3-card-8">
                    <div class="w3-container w3-theme-l2  w3-padding-24"> 
                        <span onclick="document.getElementById('login_modal_id').style.display='none'" class="w3-closebtn">×</span>
                        <h2>Sign In</h2>
                    </div>
                    <div class="w3-container w3-padding-24"> 
                        <div class="w3-white">
                            <div class="w3-input-group">      
                                <input class="w3-input w3-border" style="width:50%;" id="login_user_000_id" name="login_user_000" type="text">
                                <label class="w3-label w3-validate">Email</label>
                            </div>
                            <div class="w3-input-group">      
                                <input class="w3-input w3-border" style="width:50%;" id="login_pass_000_id" name="login_pass_000"  type="password">
                                <label class="w3-label w3-validate">Password</label>
                            </div>
                            <input type="submit" class="w3-btn w3-theme" NAME = "form_action_000" value="LogIn">
                        </div>
                    </div>
                    <div class="w3-container w3-theme-l2 w3-padding-24">
                        <a href="./acct_tools.py">Register | Forgot Password</a>
                    </div>
                </div>
            </div>  
        '''
        
     
    
# Define function to generate registration form.
def login_registration_form_v2():
    #
    temp = ''' 
            <div class="w3-card-4 w3-padding-jumbo w3-white" style="width:75%">
            <table class="w3-table w3-small w3-bordered" style="display: block;">
            <TR>
            <TD align=left>Email</TD>
            <TD><INPUT TYPE = email size=50 NAME = \"reg_user_000\"></TD>
            </TR>
            <TR>
            <TD align=left>Password</TD>
            <TD><INPUT TYPE = password  size=50 NAME = \"reg_pass_000\"></TD>
            </TR>
            <TR>
            <TD align=left>Password (again)</TD>
            <TD><INPUT TYPE = password size=50 NAME = \"reg_pass2_000\"></TD>
            </TR>
            <TR>
            </TABLE>
            <br><INPUT class="w3-btn w3-white w3-border w3-large w3-round-large" TYPE = submit NAME = \"form_action_000\" VALUE = \"Register\" >
            <br><br>
            </div>
        '''

    return temp



    
def send_email(se1,se2,se3):
    #se1 --- email of receipient
    #se2 --- topic
    #se3 --- msg 

    #em_sender = "myfinmodel@gmail.com"
    em_sender = "sender@yourdomain.com"
    em_cc = ['sender@yourdomain.com']
    em_bcc = ['"sender@yourdomain.com']
    em_user = se1
    em_topic = se2
    em_msg = se3
   
    try:
        try:
            msg = MIMEText(em_msg)
            msg['Subject'] = em_topic
            msg['From'] = em_sender
            msg['To'] = em_user
            msg['Cc'] = 'sender@yourdomain.com'
            msg['Bcc'] = 'sender@yourdomain.com'
        except:
            return False
            
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        try:
            # Settings for AWS
            a_host = "....................amazonaws.com"
            a_user = ".................."
            a_pswd = ".................."
            s = smtplib.SMTP(a_host)
            s.starttls()
            try:
                s.login(a_user,a_pswd)
            except:
                return False
        except:
            return False

        try:
            to_addr = [em_user] + em_cc + em_bcc
            s.sendmail(em_sender, to_addr, msg.as_string())
        except:
            return False

        try:
            s.quit()
            return True
        except:
            return False
    except:
        return False
    
def login_registration_process(pr_f):
    #module to process registration
    #check if the passwords match
    #generate a code
    #send email to user and ask them to plug in the code to validate
    user = pr_f['login_user_000']
    pswd1 = login_hash_pswd(pr_f['login_pass_000'])
    pswd2 = login_hash_pswd(pr_f['login_pass2_000'])
    #em_user = pr_f['login_email_000']
    em_user = user

    result = 'Error:'
    #html_start()

    #check passwords
    pass_ok = False
    user_ok = False
    if ((pswd1 == pswd2) and len(pswd1)>0): pass_ok = True

    try:
        db_user_data = sql_get_userinfo(user)
        if len(db_user_data) == 0: 
            user_ok = True
        else:
            user_ok = False
    except:
        user_ok = False
        result = result + 'Problem getting user data. \n'

    if (pass_ok and user_ok):
        #send email to user
       
        em_reg_code = generate_regcode()
        em_topic = "MyFinModel Registration code"
        em_msg = "Thanks for starting the registration process. \n\nYour registration code is "+em_reg_code+" \n\n Please use this to finish the registration process. \n\nThank you. \n\nFinancial Modeling Team \ninfo@railcalc.com"

        #Now send the msg.
        try:
            # Before sending the message stick the info of the user in the datebase
            try:
                sql_add_user([user,pswd1,em_user,em_reg_code])
            except:
				result = result + ' Error adding user. \n'
				
            send_email(em_user,em_topic,em_msg)
            #
        except:
            result = result + ' Email not sent. \n'
    else:
        if not pass_ok: result = result + ' Passwords do not match. \n'
        if not user_ok: result = result + ' Username exists - please use a different username. \n'        
    
    
    if result.strip() == 'Error:': 
        return True
    else:
        return result
    
    
def login_checkregcode_form_v2():
    #ask for the same reg code
    #then check if the reg code is correct --- maybe in a different module
    temp =  '''
            <p><sm>Please check your email to get the registration code.</sm></p>

            <div class="w3-card-4 w3-padding-jumbo w3-white" style="width:75%">
            <table class="w3-table w3-small w3-bordered" style="display: block;">
            <TR>
            <TD align=left>Email</TD>
            <TD><INPUT TYPE = email size=50 NAME = \"chkregcode_user_000\"></TD>
            </TR>
            <TR>
            <TD align=left>Registration Code</TD>
            <TD><INPUT TYPE = text size=50 NAME = \"reg_code_000\"></TD>
            </TR>
            </TABLE>
            <br><INPUT class="w3-btn w3-white w3-border w3-large w3-round-large" 
			TYPE = submit NAME = \"form_action_000\" VALUE = \"Confirm Code\" >
            <br><br></div>
        '''
        
    return temp
    

def login_checkregcode_process(cr1):
    #module to check the registrtion code
    #html_start()
    #Go to database, and update the user's registration code.
    db_user_data = sql_get_userinfo(cr1['login_user_000'])
    if len(db_user_data) == 0: 
        #No user exists with this user email
		return False
    elif len(db_user_data) == 1:
        user_entered_code = cr1['reg_code_000']
        code_in_db = db_user_data[0][3]
        if (user_entered_code == code_in_db):
            cr2 = []
            cr2.append(cr1['login_user_000'])
            cr2.append('basic')
            try:
                sql_update_registration(cr2)
                return True
            except:
                return False
        else:
            return False
    else:
        return False



# Define function to test the password.
def login_testidpswd(id, passwd):
    #test to see if the id and pswd combo are correct.
    try:
        db_user_data = sql_get_userinfo(id)
    except:
        return "Problem connecting with database"
        
    if len(db_user_data) == 0: 
        er_code = "No user exists with this email: "+id
        return er_code
    elif len(db_user_data) == 1:
        user_entered_pswd = login_hash_pswd(passwd)
        pswd_in_db = db_user_data[0][1]
        if (user_entered_pswd == pswd_in_db):
            return "passed"
        else:
            er_code = "Password not correct."
            return er_code
    else:
        er_code = "More than 1 user with this email."
        return er_code

    
    
# Define function to create a session.
def login_create_session(id):
    # In practice, use the random module for key value.
    session_key = generate_session()
    s_f_name = "./sessions/s_"+str(session_key)+".txt"
    session_file = open(s_f_name, 'w')
    session_file.write(session_key+":"+id)
    session_file.close()
    return session_key

# Define a function to return username.
def login_fetch_username(skey):
    s_f_name = "./sessions/s_"+str(skey)+".txt"
    session_file = open(s_f_name, 'r')
    # In practice, search file for correct key.
    line = session_file.readline()
    session_file.close()
    pair = string.split(line, ":")
    return pair[1]

# Define function to delete a session.
def login_delete_session(skey):
    s_f_name = "./sessions/s_"+str(skey)+".txt"
    session_file = open(s_f_name, 'w')
    # In practice, search the file for the correct key.
    # In our example, we just erase the only line in the file.
    session_file.write(" ")
    session_file.close()
    os.remove(s_f_name)
    return True
    
# Define function display_page.
def login_display_page(action_file,result, id, session_key = 0):
    if (result == "passed"):
        #html_start()
        print '<h4>DISPLAY_PAGE</h4>'
        if (session_key == 0):
            session_key = login_create_session(id)
            print '<p>',id, ' you are logged in with key:', session_key
            #print form_start("f1",action_file,'')
            print '<INPUT TYPE = \"hidden\" NAME = \"session_key_000\" VALUE ='+str(session_key)+'>'
            print '<INPUT TYPE = \"submit\" NAME = \"form_action_000\" VALUE = \"Stay Logged In.\">'
            print logout_button()
            #print form_end()
        else: 
            print '<p>',id,' .. we really do not know what to do now ...Session key:',session_key,'<p>'
            #print form_start("f1",action_file,'')
            print logout_button()
            #print form_end()
        #html_end()
    else:
        login_login_form(action_file)
         
def logout_button():
    return '<input type="submit" class="w3-theme-d4 w3-border-0 w3-wide" NAME = "form_action_000" value="SIGN OUT">'

def login_forgotpassword_form_v2():
    #page to resend password
    temp = '''
            <div class="w3-card-4 w3-padding-jumbo w3-white" style="width:75%">
            <table class="w3-table w3-small w3-bordered" style="display: block;">
            <TR>
            <Td align=left>Email</TD>
            <TD><INPUT TYPE = email size=50 NAME = \"forgotpswd_user_000\"></TD>
            </tr>
            </TABLE>
            <br><INPUT class="w3-btn w3-white w3-border w3-large w3-round-large" TYPE = submit NAME = \"form_action_000\" VALUE = \"Email New Password\" >
            <br><br></div>
        '''
    return temp
    
    
def login_forgotpassword_process(id):
    #module to send a new password to the user.
    
    em_user = id
    em_new_pswd = generate_regcode()
    em_topic = "Account info"
    em_msg = "Hello "+em_user+"\n\nYour new password is "+em_new_pswd+".  Please use this to update your password. \n\nThank you."
    
    
    #find the email address of the user
    db_user_data = sql_get_userinfo(id)

    er_code = False
    
    if len(db_user_data) == 0: 
        er_code = "No user exists with this username: "+id
    elif len(db_user_data) == 1:
        email_in_db = db_user_data[0][2]
        er_code = True
    else:
        er_code = "More than 1 user with this username."
    
    
    #send the msg now
    if (er_code==True): 
        #se_result = send_email(em_user,em_topic,em_msg)
        se_result = send_email(email_in_db,em_topic,em_msg)
        if se_result: 
            uup_res = sql_update_password([em_user,login_hash_pswd(em_new_pswd)])
            if uup_res: 
                return True
            else:
                return False
        else:
            return False
    else:
        return False
    


def login_changepassword_form_v2():
    #page to resend password
    temp = '''
            <div class="w3-card-4  w3-padding-jumbo w3-white" style="width:75%">
            <table class="w3-table w3-small w3-bordered" style="display: block;">
            <TR>
            <Td align=left>Email</TD>
            <TD><INPUT TYPE = text size=50 NAME = \"chngpswd_user_000\"></TD>
            </tr>
            <TR>
            <Td align=left>Old Password</TD>
            <TD><INPUT TYPE = password size=50 NAME = \"chngpswd_pswd0_000\"></TD>
            </tr>
            <TR>
            <Td align=left>New Password</TD>
            <TD><INPUT TYPE = password size=50 NAME = \"chngpswd_pswd1_000\"></TD>
            </tr>
            <TR>
            <Td align=left>New Password (again)</TD>
            <TD><INPUT TYPE = password size=50 NAME = \"chngpswd_pswd2_000\"></TD>
            </tr>
            </TABLE>
            <br><INPUT class="w3-btn w3-white w3-border w3-large w3-round-large" TYPE = submit NAME = \"form_action_000\" VALUE = \"Change Password\" >
            <br><br></div>    
        '''
    return temp
    
def login_changepassword_process(pcp):
    #module to process change password for the user.
    #data needed - in a dictionary format
    
    userid = pcp['login_user_000']
    oldpswd = login_hash_pswd(pcp['login_pswd0_000'])
    newpswd1 = login_hash_pswd(pcp['login_pswd1_000'])
    newpswd2 = login_hash_pswd(pcp['login_pswd2_000'])

    #check passwords
    pass_ok = False
    user_ok = False
    if (oldpswd == newpswd1):
        pass_ok = False
    elif ((newpswd1 == newpswd2) and len(newpswd1)>0): 
        pass_ok = True
    else:
        pass_ok = False

    db_user_data = sql_get_userinfo(userid)
    if len(db_user_data) == 0: 
        user_ok = "No user exists with this username: "+userid
    elif len(db_user_data) == 1:
        if (userid == db_user_data[0][0] and oldpswd == db_user_data[0][1]): user_ok = True
    else:
        user_ok = "More than 1 user with this username."
    
    #update the new password
    if (user_ok==True and pass_ok==True): 
        sql_update_password([userid,newpswd1])
        return True
    else:
        return False
 
 
     
