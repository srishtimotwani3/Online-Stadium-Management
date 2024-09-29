import csv
import re
import qrcode
import random
import smtplib
import imghdr
from email.message import EmailMessage
import mysql.connector as sqltor

mycon = sqltor.connect(host="localhost", user="root", password="root", database="crackosdb")
if mycon.is_connected() == True:
    print("connection is established")
cursor = mycon.cursor()
data1 = cursor.execute("SELECT*FROM user_details;")
dataDB = cursor.fetchall()
2

data = [
]
bookings = []
regex_dob = '^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$'
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
email_id = ""
random_menum = random.randint(103, 999) #member number
activity_ticket_price = []
count = 0
l, u, p, d = 0, 0, 0, 0

print(
    "\n                                                             Greetings Of The Day, Welcome To Crackos Coliseum!                                \n\n")

print("1.ADMIN\n2.USER")

user_or_admin = int(input("Enter Your Category choice: "))
if user_or_admin == 1:
    check = True
    while check:
        if user_or_admin == 1:  # admin
            admin_pass = input("Enter Admin Passcode: ")

            if admin_pass == ("Admin123"):
                print("Admin Authorised\n Welcome to admin controls")
                admin_choice = int(input(" 1.show database\n 2. edit database \n 3. Exit Admin Controls"))
                if admin_choice == 1:
                    print(dataDB)

                elif admin_choice == 2:
                    editorial_choice = int(input("welcome to editorial admin tool\n select the desired tool\n 1. adding tool "))
                    # while editorial_choice <=4:
                    # print("you have entered a wrong choice")
                    # editorial_choice=int(input("enter a valid choice: "))

                    if editorial_choice == 1:
                        print("Adding Tool")

                        menum = int(input("Enter menum: "))
                        name = input("Enter name: ")
                        password = input("Enter password: ")
                        email = input("Enter email: ")
                        dateofbirth = input("Enter DOB(YYYY/MM/DD): ")

                        mydb = sqltor.connect(host="localhost", user="root", password="root", database="crackosdb")

                        mycursor = mydb.cursor()

                        sql = "INSERT INTO user_details (MENUM,NAME,PASSWORD,EMAIL,DOB) VALUES (%s,%s,%s,%s,%s)"
                        val = (menum, name, password, email, dateofbirth)
                        mycursor.execute(sql, val)
                        mydb.commit()

                    else:
                        print("Invalid choice. Terminating program!")
                        exit()

                elif admin_choice == 3:
                    print("Signing out as an admin! Re-run the code to enter as User!")
                    check=False
                    exit()



                else:
                    print("Invalid choice. Terminating program!")
                    exit()



            else:  # if admin_pass wrong
                print("Unauthorised personnel")
                exit()




if user_or_admin == 2:  # user

    print("You want to Sign Up Or Sign In?\n")
    print("Enter 1 for Signing Up\nEnter 2 If You're Already a Part Of The Fam \n")
    sign_options = input("\nEnter your choice: ")

    # sign up FIRST TIME MAKING AN ACCOUNT
    if sign_options == "1":
        print("\nLet's get you started with the registration\n")
        name = input("Please Enter your full name: ")


        def check_dob(dob):
            if (re.search(regex_dob, dob)):
                print("Valid DOB")
            else:
                print("Invalid Date Format\n\n Re-Run The Code & Enter A Valid Date Format")
                exit()


        dob = input("Please Enter your Date Of Birth (DD/MM/YYYY): ")
        check_dob(dob)


        def check(email_id):
            if (re.search(regex, email_id)):
                print("Valid Email")
            else:
                print("Invalid Email\n\n Re-Run The Code & Enter A Valid Email ID")
                exit()


        email_id = input("\nEmail Suggestion : 'abc@email.com'\n\nPlease enter your Email ID: ")
        check(email_id)

        print("Suggestion: A Strong and Valid Password must contain: "
              "\n• At least 8 characters"
              "\n• An Uppercase"
              "\n• A Lowercase"
              "\n• A Number"
              "\n• And At Least One Special Character ('!', '@', '#', '$', '%', '&', '*' or '?'). ")

        password = input("\nEnter a password: \n")
        if (len(password) >= 8):
            for i in password:
                # counting lowercase alphabet

                if (i.islower()):
                    l += 1

                # counting uppercase alphabet
                if (i.isupper()):
                    u += 1

                # counting digits
                if (i.isdigit()):
                    d += 1

                # counting the mentioned special characters
                if (i == '!' or i == '@' or i == '#' or i == '$' or i == '%' or i == '&' or i == '*' or i == '?'):
                    p += 1

        if (l >= 1 and u >= 1 and p >= 1 and d >= 1 and l + p + u + d == len(password)):
            print("Valid Password")
            print(
                "--------------------------------------------------------------------------------------------------------")

        else:
            print("\nPassword does not match the set standards. ")
            print("\nRe-run the Enter a strong Password.\nTerminating Program!")
            exit()

        print("\nThank You for the details!\n")
        print("Here are the credentials you entered\n")
        print(" Name: ", name, "\n", "DOB: ", dob, "\n", "Email ID: ", email_id, "\n", "Password:", password)
        print("\nMenum is Member Number")

        random_menum = str(random_menum)

        print("Your menum is --- ", random_menum, " ---\n")
        print("Kindly login with your credentials: ")

        for i in range(1, 4):
            menum = input("\nEnter your Menum: ")
            password1 = input("Enter your Password:")
            print(
                "---------------------------------------------------------------------------------------------------------")

            if menum == random_menum and password1 == password:
                print("\nWelcome,", name, )
                print("\nLogged in successfully!")
                with open('C:/Users/srish/Downloads/final_database.csv', 'a+', newline='') as f:
                    writer = csv.writer(f)
                    user = [menum, name, password, email_id, dob]
                    data.append(user)
                    # write the data
                    writer.writerows(data)
                    f.close()
                break


            else:
                print("\nInvalid menum or password")
                print("This is your", i, "attempt out of 3")
                if i == 3:
                    print("\nYou've entered the wrong credentials three times.\n Terminating Program.")
                    exit()



    # Sign in ALREADY HAVE AN ACCOUNT

    elif sign_options == "2":
        # -------------------------------------------------------------------------
        login = False
        f = open('C:/Users/srish/Downloads/final_database.csv', 'r')
        reader = csv.reader(f)
        next(reader)

        menum = input("Enter your Menum: ")
        password = input("Enter your Password: ")
        email_id = input("Enter your Registered Email ID: ")

        for h_line in reader:
            if h_line[0] == menum and h_line[2] == password and h_line[3] == email_id:
                print("\nWelcome,", h_line[1])
                login = True
                break
            else:
                login = False

        if login == False:
            print(
                "You've entered the wrong credentials. Re-run and enter the valid credentials.\n Terminating Program.")
            exit()

        else:
            print("You are now logged in!")

        # -------------------------------------------------------------------------


    else:
        print("Terminating Program!\n Re-run and Please enter a valid Choice.")
        exit()

    r = 1
    while r != 0:
        print(
            "\n                                                  ⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬\n")
        print(
            "                                                                             ⌬  Welcome to the Home Page  ⌬")
        print(
            "\n                                                  ⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬⌬\n")
        print("Enter the respective serial number to select the desired option")
        print("\nChoose one of the following options:\n")
        print("1. Activities")
        print("2. My Cart")
        print("3. My Bookings")
        print("4. Customer support")
        print("5. Privacy policy")
        print("6. About Us")
        print("7. Exit\n")
        choice = input("Enter your choice: ")

        if choice == "1":
            a = 1
            while a != 0:

                print(
                    " \n\n------------------------------------Activities Available------------------------------------\n")
                print("Prices are inclusive of all taxes\n")
                print("Choose the respective serial number of the activity you are interested in : \n")
                print("1. Plays")
                print("2. Concerts")
                print("3. Sports")
                print("4. Talk shows")
                print("5. Lessons")
                print("6. Home Page\n")

                activity_choice = input("Enter your choice here: ""\n")
                # --------------------------------------------------------------------------------------------------------------------------------------------------------
                # VARIABLES
                # plays
                romeo_j = "Romeo & Juliet by William Shakespeare\n Price: INR 750 \n Date: 15/2/22 \n Time: 6:30 pm "
                ginny = "Who's Afraid of Virginia Woolf? by Edward Albee \n Price: INR 750 \n Date : 16/2/22 \n " \
                        "Time : 6:30 pm"

                # concerts
                one_d = "One Direction reunited & it feels so good \n Price: INR 750 \n Date: 17/2/22 \n Time: 6:00 pm "
                shawn = "Shawn Mendes in wonder \n Price: INR 750 \n Date : 18/02/22 \n Time: 6:00 pm"
                taytay = "Red by taylor swift \n Price: INR 750 \n Date : 19/02/22 \n Time: 6:00 pm"

                # sports
                # football
                psg_ManUN = "Paris Saint Germain VS Manchester United \n Price: INR 750 \n Date : 20/02/22 \n Time: 7:30 pm"
                liv_realmd = "Liverpool VS Real Madrid \n Price: INR 750 \n Date : 21/02/22 \n Time: 7:30 pm"
                # cricket
                ind_newz = "India VS New Zealand \n Price: INR 750 \n Date : 22/02/22 \n Time: 6:00 pm"
                sa_eng = "South Africa VS England \n Price: INR 750 \n Date : 23/02/22 \n Time: 6:00 pm"
                # droneracing
                drn_rcng = "RDR Corp. gravedigger vs oogabooga \n Price: INR 750 \n Date : 24/02/22 \n Time: 6:00 pm"

                # talkshows
                # Standup comedy
                kenny = "Best memories by Kenneth Sebastian \n Price: INR 750 \n Date : 25/02/22 \n Time: 5:00 pm"
                bassi = "Hostel by Anubhav Singh Bassi \n Price: INR 750 \n Date : 26/02/22 \n Time: 7:00 pm"
                # ted talks
                ted1 = "Think Fast, Talk Smart: Communication Techniques by Stanford Graduate School of Business \n Price: INR 750 \n Date : 27/02/22 \n Time: 6:00 pm"
                ted2 = "Who are you, really? The puzzle of personality | Brian Little \n Price: INR 750 \n Date : 28/02/22 \n Time: 6:00 pm"
                # poetry night
                open_mic = "Open Mic (Poetry Night) \n Price: INR 750 \n Date : 28/12/21 \n Time: 6:00 pm"
                # narration
                hamlet = "Book reading of The Hamlet by William Shakespeare read by Will Dozerman \n Price: INR 750 \n Date : 01/03/22 \n Time: 6:00 pm"
                hope = "“Hope” is the thing with feathers by Emily Dickinson read by chloe hutchins \n Price: INR 750 \n Date : 02/03/22 \n Time: 6:00 pm"
                sonnet = "Sonnet 18 by William Shakespeare read by Jake Peralta \n Price: INR 750 \n Date : 03/03/22 \n Time: 6:00 pm"
                # lessons
                martial = "Martial Arts Lessons\n Price: INR 750 \n Date : 04/03/22 \n Time: 5:00 pm"
                horse = "Horse Riding Lessons\n Price: INR 750 \n Date : 05/03/22 \n Time: 6:00 pm"
                # ---------------------------------------------------------------------------------------------------------------------------------------------------

                # PLAYS
                if activity_choice == "1":
                    print("\n\n----------------------Plays Available:----------------------\n")
                    print("\n1.", romeo_j)
                    print("\n2.", ginny)
                    plays_choice = input("\nEnter the desired serial number of the play you want to watch: \n")

                    if plays_choice == "1":
                        bookings.append(romeo_j)
                        activity_ticket_price.append(750)
                        print("Play chosen: \n", romeo_j)
                        print("The above mentioned play has been added to your cart. To check Your Cart,"
                              "Enter 2 on the Home page.")

                        print("Your seat number is:", random.randint(1, 999))
                        a = 0
                        break

                    elif plays_choice == "2":
                        bookings.append(ginny)
                        activity_ticket_price.append(750)
                        print("Plays chosen: \n", ginny)
                        print("The above mentioned play has been added to your cart. To check Your Cart,"
                              "Enter 2 on the Home page.")
                        print("Your seat number is:", random.randint(1, 999))
                        a = 0
                        break

                    else:
                        print("\nInvalid choice. The valid choices are 1 and 2.\nLeading back to the Home Page.")
                        a = 0
                        break

                # CONCERTS
                elif activity_choice == "2":
                    print("----------------------Concerts Available:----------------------")
                    print("\n1.", one_d)
                    print("\n2.", shawn)
                    print("\n3.", taytay)
                    concert_choice = input("\nEnter the desired serial number of the concert you want to attend: ")

                    if concert_choice == "1":
                        bookings.append(one_d)
                        activity_ticket_price.append(750)
                        print("Concert chosen: \n", one_d)
                        print("The above mentioned show has been added to your cart. To check Your Cart,"
                              "Enter 2 on the Home page.")
                        print("Your seat number is:", random.randint(1, 999))
                        a = 0
                        break

                    elif concert_choice == "2":
                        bookings.append(shawn)
                        activity_ticket_price.append(750)
                        print("Concert chosen: \n", shawn)
                        print("The above mentioned show has been added to your Cart. To check Your Cart,"
                              "Enter 2 on the Home page.")
                        print("Your seat number is:", random.randint(1, 999))
                        a = 0
                        break

                    elif concert_choice == "3":
                        bookings.append(taytay)
                        activity_ticket_price.append(750)
                        print("Concert chosen: \n", taytay)
                        print("The above mentioned show has been added to your Cart. To check Your Cart,"
                              "Enter 2 on the Home page.")
                        print("Your seat number is:", random.randint(1, 999))
                        a = 0
                        break

                    else:
                        print("\nInvalid choice. The valid choices are 1,2 and 3\nLeading back to the Home Page.")
                        a = 0
                        break

                # SPORTS
                elif activity_choice == "3":
                    print("\n\n----------------------Sports Available:----------------------\n\n")
                    print("\nChoose the respective serial number of the sport you are interested in : ")
                    print("\n1. Football")
                    print("\n2. Cricket")
                    print("\n3. Drone Racing")

                    sports_choice = input("\nEnter the desired serial number of the sport you want to watch: \n")

                    # FOOTBALL
                    if sports_choice == "1":
                        print("\n---------------Football matches Available:---------------\n")
                        print("\n1.", psg_ManUN)
                        print("\n2.", liv_realmd)
                        football_match = input(
                            "\nEnter the desired serial number of the football match you want to watch: ")

                        if football_match == "1":
                            bookings.append(psg_ManUN)
                            activity_ticket_price.append(750)
                            print("Football Match chosen: \n", psg_ManUN)
                            print("The above mentioned football match has been added to your Cart. To check Your Cart,"
                                  "Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        elif football_match == "2":
                            bookings.append(liv_realmd)
                            activity_ticket_price.append(750)
                            print("Sports chosen: \n", liv_realmd)
                            print("The above mentioned football match has been added to your Cart. To check Your Cart,"
                                  "Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        else:
                            print("\nInvalid choice. The valid choices are 1 and 2\nLeading back to the Home Page.")
                            a = 0
                            break

                    # CRICKET
                    elif sports_choice == "2":
                        print("\n---------------Cricket matches Available:---------------\n")
                        print("\n1.", ind_newz)
                        print("\n2.", sa_eng)
                        cricket_choice = input(
                            "\nEnter the desired serial number of the cricket match you want to watch: ")

                        if cricket_choice == "1":
                            bookings.append(ind_newz)
                            activity_ticket_price.append(750)
                            print("Cricket Match Chosen: \n", ind_newz)
                            print("\nThe above mentioned cricket match has been added to your Cart. To check Your Cart,"
                                  "Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        elif cricket_choice == "2":
                            bookings.append(sa_eng)
                            activity_ticket_price.append(750)
                            print("Cricket Match Chosen: \n", sa_eng)
                            print("\nThe above mentioned cricket match has been added to your Cart. To check Your Cart,"
                                  "Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        else:
                            print("\nInvalid choice. The valid choices are 1 and 2\nLeading back to the Home Page.")
                            a = 0
                            break

                    # DRONERACING
                    elif sports_choice == "3":
                        print("\n-----------------Drone Races Available:-----------------\n")
                        print("\n1.", drn_rcng)
                        drone_race = input("\nEnter the desired serial number of the drone race you want to watch: ")

                        if drone_race == "1":
                            bookings.append(drn_rcng)
                            activity_ticket_price.append(750)
                            print("Drone Race Chosen: \n", drn_rcng)
                            print("The above mentioned drone race has been added to your Cart. To check Your Cart,"
                                  "Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        else:
                            print("\nInvalid choice. The valid choice is 1\nLeading back to the Home Page.")
                            a = 0
                            break

                    else:
                        print("\nInvalid choice. The valid choices are 1,2and 3\nLeading back to the Home Page.")
                        a = 0
                        break

                # TALKSHOWS
                elif activity_choice == "4":
                    print(
                        "\n------------------------------------Talk Shows Available:------------------------------------\n")
                    print("\nChoose the respective serial number of the Talk Show you are interested in : ")
                    print("\n1. Stand Up comedy")
                    print("\n2. TED talks")
                    print("\n3. Poetry nights")
                    print("\n4. Narration")

                    talk_choice = input("\nEnter the desired serial number of the talk show you want to watch: ")

                    # STANDUPS
                    if talk_choice == "1":
                        print("\n---------------Stand Up Comedies Available:---------------\n")
                        print("\n1.", kenny)
                        print("\n2.", bassi)
                        standup = input("\nEnter the desired serial number of the Stand Up you want to watch: ")

                        if standup == "1":
                            bookings.append(kenny)
                            activity_ticket_price.append(750)
                            print("Stand Up Comedy chosen: \n", kenny)
                            print("The above mentioned Stand Up Comedy has been added to your Cart."
                                  "To check Your Cart, Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        elif standup == "2":
                            bookings.append(bassi)
                            activity_ticket_price.append(750)
                            print("Stand Up Comedy chosen: \n", bassi)
                            print("The above mentioned Stand Up Comedy has been added to your Cart."
                                  "To check Your Cart, Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        else:
                            print("\nInvalid choice. The valid choices are 1 and 2\nLeading back to the Home Page.")
                            a = 0
                            break


                    # TEDTALKS
                    elif talk_choice == "2":
                        print("\n---------------TED Talks Available:---------------\n")
                        print("\n1.", ted1)
                        print("\n2.", ted2)
                        ted_talk = input("\nEnter the desired serial number of the TED Talk you want to attend: ")

                        if ted_talk == "1":
                            bookings.append(ted1)
                            activity_ticket_price.append(750)
                            print("TED Talk Chosen: \n", ted1)
                            print("The above mentioned TED Talk has been added to your Cart."
                                  "To check Your Cart, Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        elif ted_talk == "2":
                            bookings.append(ted2)
                            activity_ticket_price.append(750)
                            print("TED Talk Chosen: \n", ted2)
                            print("The above mentioned TED talk has been added to your Cart."
                                  "To check Your Cart, Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        else:
                            print("\nInvalid choice. The valid choices are 1 and 2\nLeading back to the Home Page.")
                            a = 0
                            break

                    # POETRYNIGHTS
                    elif talk_choice == "3":
                        print("\n---------------Poetry Nights Available:---------------\n")
                        print("\n1.", open_mic)
                        poetry_nights = input(
                            "\nEnter the desired serial number of the poetry night you want to attend: ")

                        if poetry_nights == "1":
                            bookings.append(open_mic)
                            activity_ticket_price.append(750)
                            print("Poetry Night Chosen: \n", open_mic)
                            print("The above mentioned open mic has been added to your Cart."
                                  "To check Your Cart, Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        else:
                            print("\nInvalid choice. The valid choice is 1\nLeading back to the Home Page.")
                            a = 0
                            break

                    # Narration

                    elif talk_choice == "4":
                        print("\n---------------Narrations Available:---------------\n")
                        print("\n1.", hamlet)
                        print("\n2.", hope)
                        print("\n3.", sonnet)
                        narration = input("\nEnter the desired serial number of the Narration you want to attend: ")

                        if narration == "1":
                            bookings.append(hamlet)
                            activity_ticket_price.append(750)
                            print("Narration Chosen: \n", hamlet)
                            print("The above mentioned narration has been added to your Cart."
                                  "To check Your Cart, Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        elif narration == "2":
                            bookings.append(hope)
                            activity_ticket_price.append(750)
                            print("Narration Chosen: \n", hope)
                            print("The above mentioned narration has been added to your Cart."
                                  "To check Your Cart, Enter 2 on the Home page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        elif narration == "3":
                            bookings.append(sonnet)
                            activity_ticket_price.append(750)
                            print("Narration Chosen: \n", sonnet)
                            print("The above mentioned narration has been added to your Cart."
                                  "To check Your Cart, Enter 2 on the Home Page.")
                            print("Your seat number is:", random.randint(1, 999))
                            a = 0
                            break

                        else:
                            print("\nInvalid choice. The valid choices are 1,2and 3\nLeading back to the Home Page.")
                            a = 0
                            break

                    else:
                        print("\nInvalid choice. The valid choices are 1,2and 3\nLeading back to the Home Page.")
                        a = 0
                        break


                # LESSONS
                elif activity_choice == "5":
                    print("\n----------------------Lessons Available:----------------------\n")
                    print("\n1.", martial)
                    print("\n2.", horse)
                    lessons = input("\nEnter the desired serial number of the Lesson you want to attend: ")

                    if lessons == "1":
                        bookings.append(martial)
                        activity_ticket_price.append(750)
                        print("Lesson Chosen: \n", martial)
                        print("The above mentioned lesson has been added to your Cart."
                              "To check Your Cart, Enter 2 on the Home page.")
                        print("Your seat number is:", random.randint(1, 999))
                        a = 0
                        break

                    elif lessons == "2":
                        bookings.append(horse)
                        activity_ticket_price.append(750)
                        print("Lesson Chosen: \n", hope)
                        print("The above mentioned lesson has been added to your Cart."
                              "To check Your Cart, Enter 2 on the Home page.")
                        print("Your seat number is:", random.randint(1, 999))
                        a = 0
                        break


                    else:
                        print("\nInvalid choice. The valid choices are 1 and 2\nLeading back to the Home Page.")
                        a = 0
                        break

                elif activity_choice == "6":
                    print("Leading you back to Home Page")
                    a = 0


                else:
                    print("\nInvalid Choice!")
                    print("\nThe valid choices are 1, 2, 3, 4, 5, 6.")
                    print("Leading you back to the Home Page \n")
                    a = 0


        elif choice == "2":
            print("\n\n------------------------------------My Cart--------------------------------------\n")
            if count == 1:
                print("\nItems Booked:")
                print(*bookings, sep="\n\n")
                print("Your Ticket Has Been Confirmed. "
                      "Kindly check the email sent on the Registered Email ID, for your booking details and entry pass.\n\n "
                      "Thank You For Choosing Us. Enjoy your visit!\n")

            if bookings == []:
                print("Oops! You haven't added anything in your Cart till now. "
                      "Leading you back to the Home Page to let you add some Activities!")

            if bookings != [] and count == 0:
                print("These are the Activities you have in your Cart till now.\n")
                print(*bookings, sep="\n\n")
                print("Do you wish to pay for the added activties? \n ")
                print("1. Yes \n2. No, Lead me back to the Home Page")
                payment_1 = input("\nEnter your choice: ")

                if payment_1 == "1":
                    print("\nNumber of activities chosen: ", len(activity_ticket_price))
                    print("\nThese are the Activities you wish to pay for.\n")
                    print(*bookings, sep="\n\n")
                    activity_ticket_price = sum(activity_ticket_price)
                    print("Total amount to be paid: ", activity_ticket_price)
                    print("\nPayment Options Available:")
                    print("\n1.", "UPI")
                    print("2.", "EFT Card")
                    pay_option = int(input("\nEnter 1 for UPI or Enter 2 for paying with an EFT Card: "))

                    # ----------------------------------------------UPI------------------------------------------------------
                    if pay_option == 1:
                        print("\nPayment done with UPI.\n Ticket successfully booked.")

                        Sender_Email = "bunny.040345@gmail.com"
                        Reciever_Email = [email_id]
                        Password = "Dawn@345.."

                        newMessage = EmailMessage()  # creating an object of EmailMessage class
                        newMessage['Subject'] = "Booking Confirmation From Crackos Coliseum"  # Defining email subject
                        newMessage['From'] = Sender_Email  # Defining sender email
                        newMessage['To'] = Reciever_Email  # Defining reciever email
                        newMessage.set_content("Hey, Your Ticket Has Been Confirmed. Kindly check the attachment "
                                               "for your booking details and entry pass.\n\n"
                                               "Thank You For Choosing Us. Enjoy your visit!")
                        # Defining email body

                        img = qrcode.make(bookings)

                        img.save("C:/Users/srish/PycharmProjects/pythonProject1/TicketDetails.png")

                        with open('TicketDetails.png', 'rb') as f:
                            image_data = f.read()
                            image_type = imghdr.what(f.name)
                            image_name = f.name
                        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                            smtp.login(Sender_Email, Password)  # Login to SMTP server
                            smtp.send_message(
                                newMessage)  # Sending email using send_message method by passing EmailMessage object

                        print("The ticket details have been sent to the Email ID provided by you. \nEnjoy your visit!")
                        count += 1

                    # ---------------------------------------------EFT-----------------------------------------------------
                    elif pay_option == 2:
                        print("Payment done with EFT Card.\n\n Ticket successfully booked!\n\n")

                        Sender_Email = "bunny.040305@gmail.com"
                        Reciever_Email = [email_id]
                        Password = 'Dawn@345..'

                        newMessage = EmailMessage()  # creating an object of EmailMessage class
                        newMessage['Subject'] = "Booking Confirmation From Crackos Coliseum"  # Defining email subject
                        newMessage['From'] = Sender_Email  # Defining sender email
                        newMessage['To'] = Reciever_Email  # Defining reciever email
                        newMessage.set_content("Hey, Your Ticket Has Been Confirmed. Kindly check the attachment "
                                               "for your booking details and entry pass.\n\n"
                                               "Thank You For Choosing Us. Enjoy your visit!")
                        # Defining email body
                        import qrcode

                        img = qrcode.make(bookings)

                        img.save("C:/Users/srish/PycharmProjects/pythonProject1/TicketDetails.png")

                        with open('TicketDetails.png', 'rb') as f:
                            image_data = f.read()
                            image_type = imghdr.what(f.name)
                            image_name = f.name
                        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                            smtp.login(Sender_Email, Password)  # Login to SMTP server
                            smtp.send_message(
                                newMessage)  # Sending email using send_message method by passing EmailMessage object

                        print("The Ticket Details Have Been Sent To The Registered Email ID.\nEnjoy your visit:)")
                        count += 1

                    else:
                        print("Oops! Invalid option. Terminating Program!")
                        exit()

                elif payment_1 == "2":
                    print("Leading you back to the Home Page.")

                else:
                    print("\nInvalid choice. The valid choices are 1 and 2\nLeading back to the Home Page.")
                    break


        elif choice == "3":
            print("\n\n------------------------------------My Bookings------------------------------------\n\n")
            if count == 1:
                print("\nItems Booked:")
                print("Your Ticket Has Been Confirmed. "
                      "Kindly check the email sent on the Registered Email ID, for your booking details and entry pass.\n\n "
                      "Thank You For Choosing Us. Enjoy your visit!\n")
                print(*bookings, sep="\n\n")

            if bookings == []:
                print("\nOops! You haven't added anything in your Cart till now."
                      "Leading you back to the Home Page to let you book some Activities!")

            if bookings != [] and count == 0:
                print(
                    "\nYou have not paid for the activties you added in the cart. \nLeading you back to the Home Page.")


        elif choice == "4":
            print("\n\n------------------------------------Customer Support------------------------------------\n")
            print("""         If you have any questions, complaints, or suggestions, feel free to reach out to our customer care 
            associates through the information provided below;
            Upon receiving your request, we will contact you within 12 hours.

            Crackos Coliseum Office
            Jumbi-Jumba Road,
            Mumbai, Maharashtra, 696969.

            Crackos Coliseum Customer Care
            Phone:  [022] 1234 5678 / 79 / 80
            Email: crackoscoliseum@gmail.com

            \n\n\nFAQs 

            ~What is the age limit to enter?
            The entry is permitted for 3 years & above with a valid ticket.

            ~Is the parking available?
            Unfortunately, the parking area is unavailable.

            ~Am I supposed to be vaccinated or is the negative report fine?
            Only fully vaccinated individuals will be permitted entry.

            ~Can I cancel/modify/refund my confirmed booking?
            We're am afraid that we'd be unable to cancel/modify/refund your booking details as these 
            tickets are already reserved.\n\n
            """)


        elif choice == "5":
            print("\n\n------------------------------------Privacy Policy------------------------------------\n")
            print("""     Welcome to Crackos Coliseum, a Web-based software toolset operated by INgen operations.
        Providers and all other related entities respect users’ privacy and value their trust and confidence. 
        This privacy policy (the “Privacy Policy”) applies to the Services that link to or post this Privacy Policy, and 
        explains how Providers collect, use, and disclose information through the Services. This Privacy Policy incorporates by
        reference Homepage’s General Terms of Use Agreement which can be viewed here. By using the Services, you agree to the
        terms of this Privacy Policy.

        1. Information Collection.

        You generally are not required to provide information about yourself when you visit the Services. The following 
        information is provided accordingly:-
        Contact information, such as name, e-mail address, Date Of Birth;
        Unique identifiers, such as a user name or password;
        Demographic information, such as device type, operating system version and mobile carrier.
        Financial information, such as credit card or other payment information.

        2.Geolocation information;

        Device Information,It also collects device carrier, operating system type and version; This is to help Provider ensure
        you have the best browsing experience possible.
        Communications preferences;
        Search queries;
        Comments and other information posted in the Homepage’s interactive online forums;
        Process employment applications and inquiries
        Correspondence and other information that you send to Provider; and
        Additional information as otherwise described to you at the point of collection or pursuant to your consent.
        Homepage may also collect certain information automatically when you visit the Services, including:
        Your Internet Protocol address, which is the number automatically assigned to your computer whenever you access the 
        Internet and that can sometimes be used to derive your general geographic area;
        Other unique identifiers, including mobile device identification numbers;
        Information collected through cookies, web beacons, Local Shared Objects, and other technologies;
        Information about your interactions with e-mail messages, such as the links clicked on and whether the messages web 
        received, opened, or forwarded; and
        Standard Server Log Information


        3. Use of Information.


        Homepage may use information that it collects through the Services for a variety of purposes, including to:
        Provide you with the products, promotions, services, newsletters, and information you request and respond to
        correspondence that it receive from you;
        Contact you via email and otherwise about your account, products, services, contests, and events that it thinks might be 
        of interest to you;
        Send you promotional material or special offers on Provider’s behalf or on behalf of Provider’s marketing partners and/
        or their respective affiliates and subsidiaries and other third parties;
        Maintain or administer the Services, perform business analyses, or for other internal purposes to improve the quality of 
        Provider’s business, the Services, and other products and services it offers;
        Process employment applications and inquiries;
        Customize and personalize your use of the Services; and
        As otherwise described to you at the point of collection or pursuant to your consent.


        4. Sharing of Information.


        This Page is committed to maintain your trust, and it wants you to understand when and with whom it may share the 
        information it collects.""")


        elif choice == "6":
            print("\n Let's Talk About Us\n")
            print("""         Crackos Coliseum is the Asia’a largest stadium and it has hosted the world’s Biggest concerts on the 
             World’s Biggest Stage. It was established in 1977 by Croix Mosnire in Mumbai. 
             The area of three lakh twenty thousand square foot was constructed with a neutral backdrop, 
             allowing the Stadium to hold huge events professionally. 
             Our stadium houses for about hundred thousand seats in total.
             We believe there is nothing quite like being there.
             We’re committed to getting you to the events that you love and desire more easily and more often. 
             We truly believe in the power of shared experiences to connect people with one another. 
             We’re relentless about finding ways to make your event revelation and ticket purchase facile, fun and 
             exhilarating helping in making it more discoverable and user-friendly. 
             Crackos Coliseum uses the latest technology and security to deliver the best tickets at the best 
             prices 100% securely.
                             """)



        elif choice == "7":
            print("\nExiting Program!")
            r = 0
            if count == 1:
                print("\nEnjoy your visit!")
                exit()
            else:
                print("\nWe are sorry to see you go without booking anything!!")
                exit()

        else:
            print("\nThe valid choices are 1, 2, 3, 4, 5, 6, 7.")
            print("Leading you back to the Home Page \n")




else:
    print("Invalid choice! Terminating program!")
    exit()