import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os 
import random
import psycopg2
import sys

"""
 VARIABLES
"""
email = "asd@asd.com"
myString = "aaa"



conn = psycopg2.connect(host="asd.com", port="15432" ,database="safari", \
    user="safari", password="asd")
db = conn.cursor()

#def insert_account()



f_email, l_email = email.split('@',)
driver = webdriver.Firefox(executable_path='./driver/geckodriver64.exe')

with open('./resources/randomnames','r') as f:
    names = f.read().splitlines()

# TEMP - GET random NAME -  print names[random.randint(1,50)]

#driver.get("https://learning.oreilly.com/register")
#assert "Safari" in driver.title
time.sleep(5)



"""
 FUNCTIONS 
"""
def createAccount():
    fname = names[random.randint(1,50)]
    lname = names[random.randint(1,50)]

    fname_box = driver.find_element_by_id('id_first_name')
    lname_box = driver.find_element_by_id('id_last_name')
    usr_box = driver.find_element_by_xpath("//*[@id='id_email']")
    pass_box = driver.find_element_by_css_selector("#id_password1")
#    submit_box = driver.find_element_by_id("trial-button")



    fname_box.send_keys(fname + Keys.ENTER)
    lname_box.send_keys(lname + Keys.ENTER)
    usr_box.send_keys('test@test.com')
    pass_box.send_keys('asd')
    time.sleep(5)

def testAccount(myAccount):
    driver.get("https://www.oreilly.com/member/login")
    assert "Sign In" in driver.title
    time.sleep(5)

    usr_box =  driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/form/div[1]/input") 
    pass_box = driver.find_element_by_css_selector("div.src-Input-input-field-wrapper:nth-child(3) > input:nth-child(2)")
    signin_box = driver.find_element_by_css_selector(".src-Button-button")

    usr_box.send_keys(myAccount)
    time.sleep(2)
    pass_box.send_keys("Parola4Safari")
    time.sleep(2)

    signin_box.click()
    time.sleep(5)
    print (driver.title)
    time.sleep(5)


def increment_char(myChar):
    """
    Increments a character, return 'a' if 'z' is given
    """
    return chr(ord(myChar) + 1) if myChar != 'z' else 'a'

def increment_string(myString):
    """ 
    Increments string. Example: aaa, aab, aac ... zzy, zzz ... aaaa
    """
    lpart = myString.rstrip('z')
    if not lpart: # myString contains only 'z'
        new_string = 'a' * (len(myString) + 1)
    else:
        num_replacements = len(myString) - len(lpart)
        new_string = lpart[:-1] + increment_char(lpart[-1])
        new_string += 'a' * num_replacements
    return new_string

def get_suffix(RndEmail):
    """
    Grabs the suffix of the mail to be incremented. Example: john.doe+abc@gmail.com => string "abc"
    """
    new_string1 = RndEmail.split("+")[1]
    new_string2 = new_string1.split("@")[0]
    return new_string2

def increment_email(RndEmail):
    """ 
    It returns next generated email. Example: input john.doe+abc@gmail.com output john.doe+abd@gmail.com
    """
    old_suffix = get_suffix(RndEmail)
    new_suffix = increment_string(old_suffix)
    new_Email = RndEmail.replace("+" + old_suffix, "+" + new_suffix)
    return new_Email


def initiate_generation(myEmail):
    """
    This will trigger if the email is not yet generated. Example john.doe@gmail  => john.doe+a@gmail.com
    """
    first_part = myEmail.split("@")[0]
    second_part = myEmail.split("@")[1]
    new_mail = first_part+"+a"+"@"+second_part
    return new_mail

def get_last_email(RndEmail):
    """ 
    This will get the last email from the database
    """
    db_last_email = conn.cursor()
    conn.rollback()
    table_name = RndEmail.split("+")[0]
    sql = "SELECT username FROM " + table_name + " ORDER BY expires DESC LIMIT 1"
    last_email = db_last_email.execute(sql)
    db_last_email.close()
    return last_email 

# DATABASE FUNCTIONS
def create_table(RndEmail):
    """ create tables in the PostgreSQL database for the email specified"""
    table_name = RndEmail.split("+")[0]
    sql = "CREATE TABLE " + table_name + """ (
            username VARCHAR(255) PRIMARY KEY,
            active BOOLEAN DEFAULT FALSE,
            last_check DATE,
            expires DATE );"""
    # conn.rollback()  # in case it fails to commit 
    db.execute(sql)
    conn.commit()


db.close()
driver.close()