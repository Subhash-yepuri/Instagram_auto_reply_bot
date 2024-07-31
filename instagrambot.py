from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import subhash
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from genai1 import reply


options=webdriver.ChromeOptions()
options.add_experimental_option('detach',True)

# service=Service(ChromeDriverManager().install())     --> this stopped working because of a bug
service=Service('/Users/yepurisubhash/Desktop/selenium/chromedriver')
driver=webdriver.Chrome(service=service,options=options)
driver.implicitly_wait(5)
driver.get('https://www.instagram.com/direct/inbox/')

actionchain=ActionChains(driver)


def login(username,password):
    driver.find_element(By.NAME,'username').send_keys(username)
    driver.find_element(By.NAME,'password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR,'#loginForm > div > div:nth-child(3) > button').click()
    try:
        element = (driver.find_element(By.CSS_SELECTOR,'#loginForm > span > div'))
        print('Sorry, your password was incorrect. Please double-check your password.')
        exit()
    except NoSuchElementException:
        print("\n*** logged in ***\n") 

    try:       
        remove_messages_afterLogin()   
    except:
        print('Some Problem in clearing the NotNows')     

def remove_messages_afterLogin():
    time.sleep(7)
    first_notnow='/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/div/div/div'
    driver.find_element(By.XPATH,first_notnow).click()
    time.sleep(5)
    second_notnow='body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div._a9-z > button._a9--._ap36._a9_1'
    driver.find_element(By.CSS_SELECTOR,second_notnow).click()
    print('*** Stage1 - cleared *** \n')

def list_Of_All():
    print('LIST OF PEOPLE :')
    path1='div[role=listitem] > div > div:nth-child(2) > div >div >span>span'
    people= driver.find_elements(By.CSS_SELECTOR,path1)
    for i in range(len(people)):
        print(i+1,'.',people[i].text)    


def check_unseen_messages():
    message_check='div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x1v4esvl.x8vgawa > section > main > section > div > div > div > div.xjp7ctv > div > div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x2lah0s.x193iq5w.xeuugli.xvbhtw8 > div > div.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.x10wlt62.x1n2onr6 > div > div > div > div > div:nth-child(2) > div > div > div > div >div > div > div:nth-child(3) > div > div >span'
    unseen_dots=driver.find_elements(By.CSS_SELECTOR,message_check)
    unseen_msgs_list=[]
    for i in range(len(unseen_dots)):
        a=unseen_dots[i].find_element(By.XPATH,'./ancestor::div[4]')
        b=a.find_element(By.XPATH,'./div[2]/div/div/span/span')
        unseen_msgs_list.append(b)
    return unseen_msgs_list    

def read_chat():

    sender_msgs=driver.find_elements(By.CSS_SELECTOR,'span[class="x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u"]>div')
    total_msgs=driver.find_elements(By.CSS_SELECTOR,"div[role='button']>div>div>div>div>div>span>div")

    if len(sender_msgs)>100:
        sender_msgs=sender_msgs[-100:]

    lengthOfTotalMsgs = len(total_msgs)  

    if lengthOfTotalMsgs >100:        
        total_msgs=total_msgs[-100:]


    person1=[]
    person1_nums=[]
    person2=[]
    person2_nums=[]
    j=0    
    print('total:',[i.text for i in total_msgs])
    print('sender:',[i.text for i in sender_msgs])
    for i in range(lengthOfTotalMsgs):
        if j<len(sender_msgs) and total_msgs[i]==sender_msgs[j]:
            person1_nums.append(i)
            person1.append(total_msgs[i].text )  
            j+=1
        else:
            person2_nums.append(i)
            person2.append(total_msgs[i].text)
    # print(person1_nums)   
    # print('person1:',person1)
    # print(person2_nums)
    # print('person2',person2)
    with open('chat.txt','w') as fil :     
        j=k=0
        for i in range(lengthOfTotalMsgs):
            if i in person1_nums:
                fil.write('person1:'+person1[j]+'\n')
                j+=1
            elif i in person2_nums:
                fil.write('person2:'+person2[k]+'\n')            
                k+=1
    return sender_msgs[-1].text            
    
        
        


if __name__=='__main__':

    try :
        login(subhash.username,subhash.password)  
    except:
        print('Some problem Logging in')
        exit()    
    
    
    try:  
        list_Of_All()
    except:
        print('Some problem in detecting all people') 
    
    while(1):
        unseen_msgs_list=check_unseen_messages() 
        if unseen_msgs_list:
            print("\nUnseen Messages List:")
            for i in range(len(unseen_msgs_list)):
                print(i+1,'.',unseen_msgs_list[i].text)
            print(len(unseen_msgs_list)+1,'.','EXIT')
            n=int(input('\nEnter The Number You Want To Reply To:'))
            if n==len(unseen_msgs_list)+1:
                exit()
            for i in range(len(unseen_msgs_list)):
                if i+1==n:
                    a=time.time()
                    person=unseen_msgs_list[i]
                    person.click()
                    time.sleep(10)
                    message1=read_chat()  
                    time.sleep(2)
                    reply_message1=reply(message1)
                    driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/p').send_keys(reply_message1)
                    time.sleep(2)
                    actionchain.send_keys(Keys.ENTER).perform()
                    # driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[3]').click()
                    sent_msg_selector='div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x1v4esvl.x8vgawa > section > main > section > div > div > div > div.xjp7ctv > div > div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k > div > div > div.x1ja2u2z.x9f619.x78zum5.xdt5ytf.x193iq5w.x1l7klhg.x1iyjqo2.xs83m0k.x2lwn1j.xcrg951.x6prxxf.x6ikm8r.x10wlt62.x1n2onr6.xh8yej3 > div > div > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div.x78zum5.x1r8uery.xdt5ytf.x1iyjqo2.xmz0i5r.x6ikm8r.x10wlt62.x1n2onr6 > div > div > div > div > div > div > div:nth-child(3) > div>div:nth-last-child(2)'
                    time.sleep(2)
                    true_sent_message=driver.find_element(By.CSS_SELECTOR,sent_msg_selector)
                    while True:
                        print('entered while')
                        time.sleep(2)
                        assumed_sent_message=driver.find_element(By.CSS_SELECTOR,sent_msg_selector)
                        if 299<time.time()-a<301 and assumed_sent_message==true_sent_message:
                            break
                        elif assumed_sent_message!=true_sent_message:
                            to_reply_message='div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x1v4esvl.x8vgawa > section > main > section > div > div > div > div.xjp7ctv > div > div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k > div > div > div.x1ja2u2z.x9f619.x78zum5.xdt5ytf.x193iq5w.x1l7klhg.x1iyjqo2.xs83m0k.x2lwn1j.xcrg951.x6prxxf.x6ikm8r.x10wlt62.x1n2onr6.xh8yej3 > div > div > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div.x78zum5.x1r8uery.xdt5ytf.x1iyjqo2.xmz0i5r.x6ikm8r.x10wlt62.x1n2onr6 > div > div > div > div > div > div > div:nth-child(3) > div>div:nth-last-child(2)>div>div>div>div>div>div>div:nth-child(2)>div>div:first-child>div:first-child>div>div>div>span>div'
                            reply2=reply((driver.find_element(By.CSS_SELECTOR,to_reply_message)).text)   
                            driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/p').send_keys(reply2)
                            driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[3]').click()
                            a=time.time()
                            true_sent_message=assumed_sent_message
                                

        else:
            print('\n!!! All the messages are read !!!') 


            
        break           









      

    

