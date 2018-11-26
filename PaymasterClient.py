from pad4pi import rpi_gpio
import time
import I2C_LCD_driver
import RPi.GPIO as GPIO
import MFRC522
import signal
import pymysql

mylcd = I2C_LCD_driver.lcd()

GPIO.setwarnings(False)


KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
]

add=0
total=0
useramt=0
flag=0

COL_PINS= [17, 15, 14, 4]
ROW_PINS= [23, 24, 27, 18]
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
conn= pymysql.connect(host='192.168.1.125',user='mumbai',password='metro',db='event')
a=conn.cursor()
uid=[]
def printKey(key):
  
  global total
  global useramt
  global x
  global flag
  global flag1
  global uid
  global clientid
  
  
  if (key=="A"):
    #TO READ THE RFID CARD
    flag=1
    mylcd.lcd_clear()
    #mylcd.lcd_display_string(key, 1)  
    print("A")
    MIFAREReader = MFRC522.MFRC522()

    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print("Card detected")
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        print(uid)
    print(uid)
    if uid==[]:
        print("No card placed")
        time.sleep(1)
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Enter the amount",1)
        print("Enter the amount")
    else:
        print(uid[0])
        print(uid[1])
        print(uid[2])
        print(uid[3])
        print(uid[4])
        sql='SELECT * FROM `user` WHERE carduid0=%s AND carduid1=%s AND carduid2=%s AND carduid3=%s AND carduid4=%s;'%(uid[0],uid[1],uid[2],uid[3],uid[4])
        a.execute(sql)
        data=a.fetchall()
        print(data)
        useramt=data[0][6]
        print(useramt)
        tu=str(useramt)
        mylcd.lcd_display_string("User has:"+tu,1)
        time.sleep(3)
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Enter the amount",1)
        print("Enter the amount")
    
  elif (key=="B"):
      #TO SEE CLIENT AMOUNT
    print("B")
    mylcd.lcd_clear()
    if clientid == 0:
        print("Nothing here")
    else:
        sql='SELECT * FROM `client` WHERE id=%s;'%(clientid)
    a.execute(sql)
    bata=a.fetchall()
    print(bata[0][1])
    print(bata[0][4])
    u=str(bata[0][1])
    v=str(bata[0][4])
    mylcd.lcd_display_string("Co.:"+u, 1)
    mylcd.lcd_display_string("Amount:"+v, 2)
    
    
  elif (key=="C"):
    #FOR BACKSPACE WHEN ENTERING AMOUNT
    if total==0:
        print("Nothing to display here")
    else:
        mylcd.lcd_clear()
        print("C")
        #mylcd.lcd_display_string(key, 1)
        total = total/10
        print(total)
        totalstr=str(total)
        mylcd.lcd_display_string("Enter the amount",1)
        mylcd.lcd_display_string(totalstr, 2)
    
  elif (key=="D"):
    #FOR UPDATING FINAL VALUES
    mylcd.lcd_clear()
    print("D")
    print(total)
    #mylcd.lcd_display_string(key, 1)
    if uid==[]:
        print("Cannot be updated right now")
        mylcd.lcd_display_string("  Cannot  be ",1)
        mylcd.lcd_display_string("    updated",2)
        time.sleep(2)
        mylcd.lcd_clear()
        mylcd.lcd_display_string("  Place  card",1)
        mylcd.lcd_display_string("   on reader",2)
    else:
        if flag1==0:
            print("No updates happen now")
        else:
       #ADD THIS AT THE START OF THE LOOP     
            #finaluser=useramt-total
            print(useramt)
            print(total)
            #print(finaluser)
            if useramt<total:
                print("User does not have the required amount")
                mylcd.lcd_clear()
                mylcd.lcd_display_string("  Insufficent",1)
                mylcd.lcd_display_string("    balance",2)
                flag=0
                total=0
                useramt=0
                finaluser=0
                finalclient=0
                time.sleep(2)
                mylcd.lcd_clear()
                mylcd.lcd_display_string("  Place  card",1)
                mylcd.lcd_display_string("   on reader",2)
            else:
                finaluser=useramt-total
                print(useramt)
                print(total)
                print(finaluser)
                zoom=str(finaluser)
                sql='UPDATE user SET amount=%s WHERE carduid0=%s AND carduid1=%s AND carduid2=%s AND carduid3=%s AND carduid4=%s;'%(finaluser,uid[0],uid[1],uid[2],uid[3],uid[4])
                a.execute(sql)
                conn.commit()
                print("User updated")
                flag=0
                total=0
                useramt=0
                finaluser=0
                finalclient=0
                time.sleep(2)
                flag1=0
                sql='SELECT * FROM `client` WHERE id=%s;'%(clientid)
                a.execute(sql)
                rata=a.fetchall()
                print(rata)
                print(rata[0][4])
                finalclient=rata[0][4]+total
                print(total)
                print(rata[0][4])
                print(finalclient)
                flash=str(finalclient)
                mylcd.lcd_display_string("Client:"+flash, 1)
                mylcd.lcd_display_string("Cust:"+zoom, 2)
                sql="UPDATE `client` SET amount=%s WHERE id=%s"%(finalclient,clientid)
                a.execute(sql)
                conn.commit()
                print("Client updated")
                time.sleep(2)
                mylcd.lcd_clear()
                mylcd.lcd_display_string("  Place  card",1)
                mylcd.lcd_display_string("   on reader",2)
    
  elif (key=="1" or key=="2" or key=="3" or key=="4" or key=="5" or key=="6" or key=="7" or key=="8" or key=="9" or key=="0"):
    u=int(key)
    bo=payment(u)
    print(type(bo))
    flag1=1

  elif (key=="*"):
    #RESET ALL THE VALUES HERE
    mylcd.lcd_clear()
    mylcd.lcd_display_string("     Cancel",1)
    print("Restart process")
    flag=0
    flag1=0
    total=0
    useramt=0
    finaluser=0
    rata=0
    finalclient=0
    time.sleep(2)
    mylcd.lcd_clear()
    mylcd.lcd_display_string("  Place  card",1)
    mylcd.lcd_display_string("   on reader",2)
    
    
def payment(num):
  print("Function called")
  global add
  global total
  global flag

  if flag==0:
      print("")
  elif flag==1:
    add=num
    int(add)
    print(type(add))
    print(add)
    total = (total*10) + add
    print(total)
    numtotal=str(total)
    mylcd.lcd_display_string(numtotal,2)
    return total


mylcd.lcd_clear()
mylcd.lcd_display_string("  Welcome  To",1)
mylcd.lcd_display_string("   PayMaster",2)
time.sleep(2)
mylcd.lcd_clear()
mylcd.lcd_display_string("  Enter   the ",1)
mylcd.lcd_display_string("   Password",2)
passingtheword="ally"
takeit=raw_input("Enter the password!\n")
if passingtheword==takeit:
    mylcd.lcd_clear()
    print("Password is correct")
    mylcd.lcd_display_string(" Password  is ",1)
    mylcd.lcd_display_string("    Correct ",2)
time.sleep(1)
mylcd.lcd_clear()
mylcd.lcd_display_string("Enter client ID",1)
clientid=int(input("Enter the client ID\n"))
print(clientid)
mylcd.lcd_clear()
mylcd.lcd_display_string("The ClientID is",1)
clientiddisplay=str(clientid)
mylcd.lcd_display_string("       "+clientiddisplay,2)
time.sleep(3)
mylcd.lcd_clear()
mylcd.lcd_display_string("  Place  card",1)
mylcd.lcd_display_string("   on reader",2)


keypad.registerKeyPressHandler(printKey)


try:
  while(True):
    time.sleep(0.2)
except:
  keypad.cleanup()

