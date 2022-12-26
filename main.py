###########################
### Importing libraries ###
###########################

# Importing tkinter library for creating the GUI and setting the reference as 'tk'
import tkinter as tk
# Importing tkinter messagebox
from tkinter import messagebox
# Importing ttk from tkinter to display tables
from tkinter import ttk
# Importing MySQL for the online database
import mysql.connector
# Importing hashlib to hash passwords
import hashlib
# Importing SQLite for the local flat file result table
import sqlite3
# Importing speedtest module to carry out network speed tests
import speedtest
# Importing socket to get the name of the current device
import socket
# Importing threading to prevent GUI being frozen due to waiting for other code to finish executing
import threading
# Importing getmac to get the MAC address of the device this program is running on
import getmac
# Importing datetime to manipulate date and time formats and get the current time
import datetime
# Importing schedule to schedule speed tests
import schedule
# Importing time to help loop the schedule task
import time
# Importing pyplot and dates from matplotlib to plot the graphs
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
# Importing and calling load_dotenv from dotenv to load environment variables
from dotenv import load_dotenv
load_dotenv()
# Importing os to get environment variables
import os

##################################
### Application Window Classes ###
##################################

# Class for the main menu window
class MainMenu:

    # Setting constructor attribute values
    def __init__(self, mainMenuObject):

        # Allows us to use tkinter mainMenu functions within my own window class by taking the tkinter object as an
        # argument which I can then copy to my own attribute object variable that will ALSO be able to have other #
        # attribute variables (which I will use for, for example, widgets etc.). Otherwise, 'self.mainMenuObject' would
        # just be a variable attribute with no access to methods like '.title'.
        self.mainMenuObject = mainMenuObject

        # Saving screen size to variables
        global screenWidth
        global screenHeight
        screenWidth = self.mainMenuObject.winfo_screenwidth()
        screenHeight = self.mainMenuObject.winfo_screenheight()

        # Setting main menu window properties
        self.mainMenuObject.title("Main Menu")
        self.mainMenuObject.resizable(False, False)
        self.mainMenuObject.width = 250
        self.mainMenuObject.height = 104
        # Defining size and placement of the main menu
        self.mainMenuObject.geometry(
            f"{self.mainMenuObject.width}x{self.mainMenuObject.height}"
            f"+{center_x(self.mainMenuObject.width)}+{center_y(self.mainMenuObject.height)}"
        )

        # Creating widgets
        self.mainMenuObject.btnReg = tk.Button(mainMenuObject, text="Register", command=MainMenu.createRegWindow)
        self.mainMenuObject.btnSignIn = tk.Button(mainMenuObject, text="Sign-In", command=MainMenu.createSignInWindow)
        self.mainMenuObject.btnContWithoutAcc = tk.Button(mainMenuObject, text="Continue Without an Account",
                                                          command=MainMenu.createMasterWindow)

        # Loading widgets
        self.mainMenuObject.btnReg.pack(padx=5, pady=5)
        self.mainMenuObject.btnSignIn.pack(padx=10, pady=2.5)
        self.mainMenuObject.btnContWithoutAcc.pack(padx=10, pady=2.5)

        # Calling the exit function if user clicks the default, top-right windows exit button
        self.mainMenuObject.protocol("WM_DELETE_WINDOW", MainMenu.exitConfirm)

    # Static method to create a registration window by instantiating a 'RegWindow' object from the class below
    @staticmethod
    def createRegWindow():
        global regWindow
        regWindow = tk.Toplevel()
        regWindow = RegWindow(regWindow)

    # Static method to create a sign-in window by instantiating a 'SignIn' object from the class below
    @staticmethod
    def createSignInWindow():
        global signInWindow
        signInWindow = tk.Toplevel()
        signInWindow = SignIn(signInWindow)

    # Static method to hide the main menu window and create a master window instance
    @staticmethod
    def createMasterWindow():
        mainMenu.mainMenuObject.withdraw()
        # Creating the master window
        global masterWindow
        masterWindow = tk.Toplevel()
        masterWindow = MasterWindow(masterWindow)

    # Static method to confirm whether the user wants to exit the program if they have open windows
    @staticmethod
    def exitConfirm():

        # The 'try' blocks run their code under the assumption that the respective object variable exists for either of
        # the windows (which would occur if a sign-in or registration window has been opened before).
        # It checks whether these windows are currently open and, if the object variables do not exist yet (which would
        # happen if a sign in or registration window was not clicked on yet), a 'NameError' exception is raised and the
        # value of regWindowExists or signInWindowExists is set to 0 (meaning that it doesn't exist).
        # Otherwise, the values of regWindowExists and signInWindowExists is set by '.winfo_exists()' to be 1 or 0
        # according to if the window is open or not.
        try:
            regWindowExists = regWindow.regWindowObject.winfo_exists()
        except NameError:
            regWindowExists = 0
        try:
            signInWindowExists = signInWindow.signInObject.winfo_exists()
        except NameError:
            signInWindowExists = 0
        if regWindowExists == 1 or signInWindowExists == 1:
            exitWindowResponse = messagebox.askyesno("Warning",
                                                     "You have windows open. Are you sure you want to close?")
            if exitWindowResponse == 1:
                mainMenu.mainMenuObject.destroy()
        else:
            mainMenu.mainMenuObject.destroy()


# Class for the registration window
class RegWindow:

    # Setting constructor attribute values
    def __init__(self, regWindowObject):
        self.regWindowObject = regWindowObject

        # Setting registration window properties
        self.regWindowObject.title("Registration")
        self.regWindowObject.resizable(False, False)
        self.regWindowObject.width = 400
        self.regWindowObject.height = 270
        self.regWindowObject.geometry(
            f"{self.regWindowObject.width}x{self.regWindowObject.height}"
            f"+{center_x(self.regWindowObject.width)}+{center_y(self.regWindowObject.height)}"
        )

        # Creating widgets
        self.regWindowObject.lblFirstName = tk.Label(regWindowObject, text="First Name: ")
        self.regWindowObject.entFirstName = tk.Entry(regWindowObject, width=30)
        self.regWindowObject.lblLastName = tk.Label(regWindowObject, text="Last Name: ")
        self.regWindowObject.entLastName = tk.Entry(regWindowObject, width=30)
        self.regWindowObject.lblEmail = tk.Label(regWindowObject, text="E-Mail: ")
        self.regWindowObject.entEmail = tk.Entry(regWindowObject, width=30)
        self.regWindowObject.lblUsername = tk.Label(regWindowObject, text="Username: ")
        self.regWindowObject.entUsername = tk.Entry(regWindowObject, width=30)
        self.regWindowObject.lblPassword = tk.Label(regWindowObject, text="Password: ")
        self.regWindowObject.entPassword = tk.Entry(regWindowObject, width=30, show="*")
        self.regWindowObject.btnReg = tk.Button(regWindowObject, text="Register", command=self.register)
        # Creating the warning labels
        self.regWindowObject.lblSpecialChar = tk.Label(self.regWindowObject,
                                                       text=("Please do not use any of the following special "
                                                             """characters:\n'[!"#$%^=+`¬;,£%'&*()<>?/\|}{~:]'"""))
        self.regWindowObject.lblEmpty = tk.Label(regWindowObject, text="Please do not leave any fields blank")
        self.regWindowObject.lblWhitespace = tk.Label(self.regWindowObject,
                                                      text="Please do not use any spaces in your register details")

        # Loading widgets
        self.regWindowObject.lblFirstName.grid(row=0, column=0, padx=(66, 0), pady=(10, 0))
        self.regWindowObject.entFirstName.grid(row=0, column=1, pady=(10, 0))
        self.regWindowObject.lblLastName.grid(row=1, column=0, padx=(67, 0), pady=(5, 0))
        self.regWindowObject.entLastName.grid(row=1, column=1, pady=(5, 0))
        self.regWindowObject.lblEmail.grid(row=2, column=0, padx=(89, 0), pady=(5, 0))
        self.regWindowObject.entEmail.grid(row=2, column=1, pady=(5, 0))
        self.regWindowObject.lblUsername.grid(row=3, column=0, padx=(70, 0), pady=(5, 0))
        self.regWindowObject.entUsername.grid(row=3, column=1, pady=(5, 0))
        self.regWindowObject.lblPassword.grid(row=4, column=0, padx=(73, 0), pady=(5, 0))
        self.regWindowObject.entPassword.grid(row=4, column=1, pady=(5, 0))
        self.regWindowObject.btnReg.place(relx=0.5, rely=0.57, anchor="center")
        self.regWindowObject.lblSpecialChar.place(relx=0.5, rely=0.7, anchor="center")
        self.regWindowObject.lblEmpty.place(relx=0.5, rely=0.82, anchor="center")
        self.regWindowObject.lblWhitespace.place(relx=0.5, rely=0.91, anchor="center")

        # Disabling buttons to prevent unlimited windows
        mainMenu.mainMenuObject.btnReg["state"] = "disabled"
        mainMenu.mainMenuObject.btnSignIn["state"] = "disabled"
        mainMenu.mainMenuObject.btnContWithoutAcc["state"] = "disabled"

        # Using the delete protocol as a trigger to run 'closeAndEnableButtons'
        self.regWindowObject.protocol("WM_DELETE_WINDOW", self.closeAndEnableButtons)

    # Method to close the registration window and re-enable the buttons on the main menu
    def closeAndEnableButtons(self):
        self.regWindowObject.destroy()
        mainMenu.mainMenuObject.btnReg["state"] = "normal"
        mainMenu.mainMenuObject.btnSignIn["state"] = "normal"
        mainMenu.mainMenuObject.btnContWithoutAcc["state"] = "normal"

    # Method to register the user by taking in their inputs from the text boxes
    def register(self):

        # Storing the values of the text boxes into variables and removing any leading or trailing whitespace or tabs
        firstName = self.regWindowObject.entFirstName.get().strip()
        lastName = self.regWindowObject.entLastName.get().strip()
        email = self.regWindowObject.entEmail.get().strip()
        username = self.regWindowObject.entUsername.get().strip()
        password = self.regWindowObject.entPassword.get().strip()

        # Checking if there are any remaining whitespace between characters in any fields
        fields = [firstName, lastName, email, username, password]
        whitespace = False
        for field in fields:
            for char in field:
                if char == " ":
                    whitespace = True
                    break

        # Checking if there are any special characters in any fields
        hasSpecialChars = False
        for field in fields:
            if any(char in specialCharacters for char in field):
                hasSpecialChars = True
                break

        # Highlights special character warning label if there are special character(s)
        if hasSpecialChars:
            self.regWindowObject.lblSpecialChar.config(fg="red")
        else:
            self.regWindowObject.lblSpecialChar.config(fg="black")

        # Highlights empty field label if there are empty field(s)
        if 0 in {len(firstName), len(lastName), len(email), len(username), len(password)}:
            self.regWindowObject.lblEmpty.config(fg="red")
        else:
            self.regWindowObject.lblEmpty.config(fg="black")

        # Highlights whitespace warning label if there is whitespace in field(s)
        if whitespace:
            self.regWindowObject.lblWhitespace.config(fg="red")
        else:
            self.regWindowObject.lblWhitespace.config(fg="black")

        # Otherwise, proceeds with the registration process
        if (not hasSpecialChars) and (not (0 in {
            len(firstName),
            len(lastName),
            len(email),
            len(username),
            len(password)
        })) and (not whitespace):
            # Encoding the password string into bytes
            encodedPass = password.encode('utf-8')
            # Creating a sha256 password hash object
            passHashObject = hashlib.sha256()
            # Feeding the hash object the encoded password
            passHashObject.update(encodedPass)
            # Converting the encoded password data in the hash object into hexadecimal format
            passHash = passHashObject.hexdigest()
            # Trying to connect to the database and inserting values into the 'User' table
            try:
                # Connecting to the database
                with mysql.connector.connect(
                        host=os.getenv("MYSQL_HOST"),
                        user=os.getenv("MYSQL_USER"),
                        passwd=os.getenv("MYSQL_PASSWD"),
                        database=os.getenv("MYSQL_DATABASE")
                ) as onlineAccountDb:
                    # Creating a cursor to manipulate the database
                    with onlineAccountDb.cursor() as onlineAccountDbCursor:
                        # Attempting to query for any rows in the 'User' table that have the same username as the one
                        # the user has input
                        onlineAccountDbCursor.execute("SELECT * FROM User WHERE username = %s", (username,))
                        # If no results come back this must mean that the username is unique
                        if onlineAccountDbCursor.fetchone() is None:
                            isUniqueUser = True
                        # Otherwise, the username must already exist
                        else:
                            isUniqueUser = False
                        # Attempting to query for any rows in the 'User' table that have the same e-mail as the one the
                        # user has input
                        onlineAccountDbCursor.execute("SELECT * FROM User WHERE email = %s", (email,))
                        # If no results come back this must mean that the e-mail is unique
                        if onlineAccountDbCursor.fetchone() is None:
                            isUniqueEmail = True
                        # Otherwise, the email must already exist
                        else:
                            isUniqueEmail = False
                        # Proceeds to register the user if their username and email are both unique
                        if isUniqueUser and isUniqueEmail:
                            # Inserting the values into the database
                            onlineAccountDbCursor.execute("INSERT INTO User "
                                                          "(firstName, lastName, email, username, passHash)"
                                                          " VALUES (%s, %s, %s, %s, %s)",
                                                          (firstName, lastName, email, username, passHash))
                            # Closing the cursor
                            onlineAccountDbCursor.close()
                            # Committing the database changes
                            onlineAccountDb.commit()
                            # Closing the database connection
                            onlineAccountDb.close()
                            # A notification message appears to notify successful registration of the user
                            messagebox.showinfo("Registration Success",
                                                "You have successfully registered an account!")
                        # If, out of the username and email, the username is not unique, an error message appears which
                        # explains that this username has already been taken
                        elif (not isUniqueUser) and isUniqueEmail:
                            messagebox.showerror("Registration Failure",
                                                 "That username has already been taken.")
                        # If, out of the username and email, the e-mail is not unique, an error message appears which
                        # explains that this e-mail has already been taken
                        elif isUniqueUser and (not isUniqueEmail):
                            messagebox.showerror("Registration Failure",
                                                 "That e-mail has already been taken.")
                        # If both the username and e-mail are not unique, an error message appears which explains that
                        # both the username and e-mail have already been taken
                        elif (not isUniqueUser) and (not isUniqueEmail):
                            messagebox.showerror("Registration Failure",
                                                 "That username and e-mail has already been taken.")

            # Otherwise, shows an error message with the database connection and asking to check internet connection
            except:
                messagebox.showerror("Connection Error",
                                     "There has been an error connecting to the database. "
                                     "Please check internet connection.")


# Class for the sign-in window
class SignIn:

    # Setting constructor attribute values
    def __init__(self, signInObject):
        self.signInObject = signInObject

        # Setting sign-in window properties
        self.signInObject.title("Sign-In")
        self.signInObject.resizable(False, False)
        self.signInObject.width = 400
        self.signInObject.height = 100
        self.signInObject.geometry(
            f"{self.signInObject.width}x{self.signInObject.height}"
            f"+{center_x(self.signInObject.width)}+{center_y(self.signInObject.height)}")

        # Creating widgets
        self.signInObject.lblUsername = tk.Label(signInObject, text="Username: ")
        self.signInObject.entUsername = tk.Entry(signInObject, width=30)
        self.signInObject.lblPassword = tk.Label(signInObject, text="Password: ")
        self.signInObject.entPassword = tk.Entry(signInObject, width=30, show="*")
        self.signInObject.btnSignIn = tk.Button(signInObject, text="Sign-In", command=self.login)

        # Loading widgets
        self.signInObject.lblUsername.grid(row=2, column=0, padx=(73, 0), pady=(5, 0))
        self.signInObject.entUsername.grid(row=2, column=1, pady=(5, 0))
        self.signInObject.lblPassword.grid(row=4, column=0, padx=(76, 0), pady=(5, 0))
        self.signInObject.entPassword.grid(row=4, column=1, pady=(5, 0))
        self.signInObject.btnSignIn.place(relx=0.5, rely=0.75, anchor="center")

        # Disabling buttons to prevent unlimited windows
        mainMenu.mainMenuObject.btnReg["state"] = "disabled"
        mainMenu.mainMenuObject.btnSignIn["state"] = "disabled"
        mainMenu.mainMenuObject.btnContWithoutAcc["state"] = "disabled"

        # Using the delete protocol as a trigger to run 'closeAndEnableButtons'
        self.signInObject.protocol("WM_DELETE_WINDOW", self.closeAndEnableButtons)

    # Method to close the sign-in window and re-enable the buttons on the main menu    
    def closeAndEnableButtons(self):
        self.signInObject.destroy()
        mainMenu.mainMenuObject.btnReg["state"] = "normal"
        mainMenu.mainMenuObject.btnSignIn["state"] = "normal"
        mainMenu.mainMenuObject.btnContWithoutAcc["state"] = "normal"

    def login(self):

        # Storing the values of the text boxes into variables and removing any leading or trailing whitespace or tabs
        username = self.signInObject.entUsername.get().strip()
        password = self.signInObject.entPassword.get().strip()

        # Checking if there is any remaining whitespace between characters in any of the fields
        fields = [username, password]
        for field in fields:
            for char in field:
                if char == " ":
                    messagebox.showerror("Login Failure",
                                         "Username and password cannot have whitespace between characters.")
                    return

        # Checking if there are any special characters in any fields
        for field in fields:
            if any(char in specialCharacters for char in field):
                messagebox.showerror("Login Failure",
                                     "Username and password cannot have any of the following special characters:\n"
                                     """[!"#$%^=+-`¬;,£%'&*()<>?/\|}{~:]""")
                return

        # Encoding the password string into bytes
        encodedPass = password.encode('utf-8')
        # Creating a sha256 password hash object
        passHashObject = hashlib.sha256()
        # Feeding the hash object the encoded password
        passHashObject.update(encodedPass)
        # Converting the encoded password data in the hash object into hexadecimal format
        passHash = passHashObject.hexdigest()
        # Trying to connect to the database and inserting values into the 'User' table
        try:
            # Connecting to the database
            with mysql.connector.connect(
                    host=os.getenv("MYSQL_HOST"),
                    user=os.getenv("MYSQL_USER"),
                    passwd=os.getenv("MYSQL_PASSWD"),
                    database=os.getenv("MYSQL_DATABASE")
            ) as onlineAccountDb:
                # Creating a cursor to manipulate the database
                with onlineAccountDb.cursor() as onlineAccountDbCursor:
                    # Attempting to query for any rows in the 'User' table that have the same username and password as
                    # the ones the user has input
                    onlineAccountDbCursor.execute("SELECT * FROM User WHERE username = %s AND passHash = %s",
                                                  (username, passHash))
                    # Showing a login failure if no results show up, indicating no registered account with those details
                    if onlineAccountDbCursor.fetchone() is None:
                        messagebox.showerror("Login Failure",
                                             "Incorrect username or password.")
                    # Otherwise, shows a message notifying that logging in was successful, closes the sign-in window,
                    # hides the main menu, and runs an instance of the main program master window, passing the username
                    # used to log in as a parameter so that the main program master window can use it to save and fetch
                    # results to and from the account with that username.
                    else:
                        messagebox.showinfo("Login Success",
                                            "You have logged in successfully!")
                        # Closing sign-in window
                        signInWindow.signInObject.destroy()
                        # Hiding main menu window
                        mainMenu.mainMenuObject.withdraw()
                        # Creating the master window
                        global masterWindow
                        masterWindow = tk.Toplevel()
                        masterWindow = MasterWindow(masterWindow, username)

        # Otherwise, shows an error message with the database connection and asking to check internet connection
        except:
            messagebox.showerror("Connection Error",
                                 "There has been an error connecting to the database. "
                                 "Please check internet connection.")


# Class for the 'master' window
class MasterWindow:

    # Setting constructor attribute values
    def __init__(self, masterWindowObject, username=None):
        self.masterWindowObject = masterWindowObject

        # Setting master window properties
        self.masterWindowObject.title("Master Window")
        self.masterWindowObject.resizable(False, False)
        self.masterWindowObject.width = 867
        self.masterWindowObject.height = 200
        # Saving the username as an attribute
        self.masterWindowObject.username = username
        self.masterWindowObject.geometry(
            f"{self.masterWindowObject.width}x{self.masterWindowObject.height}"
            f"+{center_x(self.masterWindowObject.width)}+{center_y(self.masterWindowObject.height)}")

        # Creating buttons and labels

        # If a username is not given to the constructor (this would happen when the user uses the program without an
        # account) then the welcome label will have its text default to 'user' when referring to the user instead of any
        # username
        if username is None:
            self.masterWindowObject.lblHello = tk.Label(masterWindowObject, text="Hello user!", font=(None, 13))
        # Otherwise, the welcome label text defaults to the user's username (that was used to sign in)
        else:
            self.masterWindowObject.lblHello = tk.Label(masterWindowObject, text=f"Hello {username}!", font=(None, 13))
        # Threads are being utilised with a lambda function so that the main tkinter GUI is not hanged up by the speed
        # test or scheduled tests being conducted - lambda function ensures a new thread is started every time as old
        # threads cannot be restarted.
        self.masterWindowObject.btnSpeedTest = tk.Button(masterWindowObject, text="Speed\nTest", font=(None, 30),
                                                         command=lambda:
                                                         threading.Thread(target=self.createSpeedTestWindow).start())
        self.masterWindowObject.btnScheduleTests = tk.Button(masterWindowObject, text="Schedule\nTests",
                                                             font=(None, 30),
                                                             command=lambda:
                                                             threading.Thread(target=MasterWindow.createScheduleWindow)
                                                             .start())
        self.masterWindowObject.btnResultHistory = tk.Button(masterWindowObject, text="Result\nHistory",
                                                             font=(None, 30),
                                                             command=MasterWindow.createResultHistoryWindow)
        self.masterWindowObject.btnNetworkPacketMonitoring = tk.Button(masterWindowObject,
                                                                       text="Network Packet\nMonitoring",
                                                                       font=(None, 30))
        # Loading widgets
        self.masterWindowObject.lblHello.place(relx=0.015, rely=0.06)
        self.masterWindowObject.btnSpeedTest.grid(row=1, column=0, padx=(10, 0), pady=(44, 0))
        self.masterWindowObject.btnScheduleTests.grid(row=1, column=1, padx=(10, 0), pady=(44, 0))
        self.masterWindowObject.btnResultHistory.grid(row=1, column=2, padx=(10, 0), pady=(44, 0))
        self.masterWindowObject.btnNetworkPacketMonitoring.grid(row=1, column=3, padx=(10, 0), pady=(44, 0))

        # Initiate exit method if user attempts to close the master window
        self.masterWindowObject.protocol("WM_DELETE_WINDOW", self.exit)

    # Method to close the master window, and reveal the initial main menu window
    def exit(self):
        self.masterWindowObject.destroy()
        mainMenu.mainMenuObject.deiconify()
        # Re-enabling the buttons on the main menu
        mainMenu.mainMenuObject.btnReg["state"] = "normal"
        mainMenu.mainMenuObject.btnSignIn["state"] = "normal"
        mainMenu.mainMenuObject.btnContWithoutAcc["state"] = "normal"

    # Creating the speed test results window
    def createSpeedTestWindow(self):
        # Disabling other buttons to prevent spamming windows during the test
        self.masterWindowObject.btnSpeedTest["state"] = "disabled"

        # A label is created and placed at the bottom of the master window to explain that a speed test is being
        # conducted
        masterWindow.masterWindowObject.lblConductingSpeedTest = tk.Label(self.masterWindowObject,
                                                                          text="Testing speed. Please wait...")
        masterWindow.masterWindowObject.lblConductingSpeedTest.place(relx=0.5, rely=0.92, anchor="center")

        # Trying to conduct a speed test and display a speed test window
        try:
            # Creating a speed test object to do the test
            speedtestObject = speedtest.Speedtest()
            # Dividing by 10^6 in order to give download and upload results in megabits per second, and then rounding
            # all results to 2 decimal places
            downloadResult = round(speedtestObject.download() / (10 ** 6), 2)
            uploadResult = round(speedtestObject.upload() / (10 ** 6), 2)
            pingResult = round(speedtestObject.results.ping, 2)

            # Tries to connect to the 'LocalResults.db' database (or automatically creates one if it doesn't yet exist)
            # with the definitions outlined in the design phase
            try:
                localResultDb = sqlite3.connect("LocalResults.db")
                localResultDbCursor = localResultDb.cursor()
                localResultDbCursor.execute(
                    """CREATE TABLE IF NOT EXISTS LocalResults (
                    resultID INTEGER PRIMARY KEY,
                    download REAL NOT NULL,
                    upload REAL NOT NULL,
                    ping REAL NOT NULL,
                    date_time TEXT NOT NULL
                    )"""
                )
                # Inserting the calculated speed test values into the database
                localResultDbCursor.execute("INSERT INTO LocalResults (download, upload, ping, date_time) "
                                            "VALUES (?, ?, ?, datetime('now', 'localtime'))",
                                            (downloadResult, uploadResult, pingResult))
                # Committing the transaction
                localResultDb.commit()
            # If an exception occurs, the program will throw an error window explaining an error in connecting to the
            # database
            except:
                messagebox.showerror("Connection Error",
                                     "There has been an error connection to the local database.")
            # Always closes the cursor and database connection at the end
            finally:
                localResultDbCursor.close()
                localResultDb.close()

            # Trying to connect to the online database and insert the results if the user is logged in with a username
            if self.masterWindowObject.username is not None:
                try:
                    # Connecting to the database
                    with mysql.connector.connect(
                            host=os.getenv("MYSQL_HOST"),
                            user=os.getenv("MYSQL_USER"),
                            passwd=os.getenv("MYSQL_PASSWD"),
                            database=os.getenv("MYSQL_DATABASE")
                    ) as onlineAccountDb:
                        # Creating a cursor to manipulate the database
                        with onlineAccountDb.cursor() as onlineAccountDbCursor:
                            # Retrieving the correct userID of the logged-in user using their username
                            onlineAccountDbCursor.execute("SELECT userID FROM User WHERE username = %s",
                                                          (masterWindow.masterWindowObject.username,))
                            userID = onlineAccountDbCursor.fetchone()[0]
                            # Finding the MAC address of this machine
                            macAddress = getmac.get_mac_address()
                            # Finding the current date and time
                            currentDateTime = datetime.datetime.now()
                            # Formatting the current date and time into MySQL DATETIME format
                            currentDateTime = currentDateTime.strftime("%Y-%m-%d %H:%M:%S")
                            # Finding the name of the current device
                            deviceName = socket.gethostname()
                            # Checking if the device is already registered
                            onlineAccountDbCursor.execute("SELECT * From Device WHERE deviceMAC = %s",
                                                          (macAddress,))
                            # Registering the current device on the 'Device' table only if it isn't already registered
                            if onlineAccountDbCursor.fetchone() is None:
                                onlineAccountDbCursor.execute("INSERT INTO Device (deviceMAC, deviceName) "
                                                              "VALUES (%s, %s)", (macAddress, deviceName))
                                # Committing the transaction
                                onlineAccountDb.commit()
                            # Checking if an entry already exists in the 'User-Device Link' table
                            onlineAccountDbCursor.execute("SELECT * From UserDeviceLink WHERE "
                                                          "userID = %s AND deviceMAC = %s", (userID, macAddress))
                            # Inserting a row into the 'User-Device Link' table (to indicate which user uses/has used
                            # which device) only if there is no existing row already
                            if onlineAccountDbCursor.fetchone() is None:
                                onlineAccountDbCursor.execute("INSERT INTO UserDeviceLink (userID, deviceMAC) "
                                                              "VALUES (%s, %s)", (userID, macAddress))
                                # Committing the transaction
                                onlineAccountDb.commit()
                            # Inserting the result data into the Result table
                            onlineAccountDbCursor.execute(
                                """INSERT INTO Result (userID, deviceMAC, download, upload, ping, date_time) 
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                                (userID, macAddress, downloadResult, uploadResult,
                                 pingResult, currentDateTime))
                            # Committing the transaction
                            onlineAccountDb.commit()
                # Otherwise, shows an error message with the database connection and asking to check internet connection
                except:
                    messagebox.showerror("Connection Error",
                                         "There has been an error connecting to the database. "
                                         "Please check internet connection.")

            # Instantiating the speed test result window
            global speedTestWindow
            speedTestWindow = tk.Toplevel()
            speedTestWindow = SpeedTest(speedTestWindow, downloadResult, uploadResult, pingResult)
        except:
            self.masterWindowObject.lblConductingSpeedTest.destroy()
            self.masterWindowObject.btnSpeedTest["state"] = "normal"
            messagebox.showerror("Connection Error",
                                 "There has been an error connecting to the speedtest servers. Please check internet "
                                 "connection.")

    # Method to create a schedule window
    @staticmethod
    def createScheduleWindow():
        masterWindow.masterWindowObject.btnSpeedTest["state"] = "disabled"
        masterWindow.masterWindowObject.btnScheduleTests["state"] = "disabled"
        global scheduleWindow
        scheduleWindow = tk.Toplevel()
        scheduleWindow = Schedule(scheduleWindow)

    # Method to create a result history window
    @staticmethod
    def createResultHistoryWindow():
        masterWindow.masterWindowObject.btnResultHistory.config(state="disabled")
        global resultHistoryWindow
        resultHistoryWindow = tk.Toplevel()
        resultHistoryWindow = ResultHistory(resultHistoryWindow)

# Class for the speed test window
class SpeedTest:

    # Setting constructor attribute values
    def __init__(self, speedTestWindowObject, download, upload, ping):
        self.speedTestWindowObject = speedTestWindowObject

        # Setting speed test window properties
        self.speedTestWindowObject.title("Speed Test")
        self.speedTestWindowObject.resizable(False, False)
        self.speedTestWindowObject.width = 275
        self.speedTestWindowObject.height = 60
        self.speedTestWindowObject.geometry(
            f"{self.speedTestWindowObject.width}x{self.speedTestWindowObject.height}"
            f"+{center_x(self.speedTestWindowObject.width)}+{center_y(self.speedTestWindowObject.height)}")

        # Creating and placing the result label on the window
        self.speedTestWindowObject.lblResults = tk.Label(speedTestWindowObject,
                                                         text=f"Download speed: {download} Mbps\nUpload speed: "
                                                              f"{upload} Mbps\nPing: {ping} ms")
        self.speedTestWindowObject.lblResults.place(relx=0.5, rely=0.5, anchor="center")

        # Removing the 'conducting speed test' label as the test is now complete
        masterWindow.masterWindowObject.lblConductingSpeedTest.destroy()

        # Method to close the speed test result window and re-enable the buttons on the master window
        self.speedTestWindowObject.protocol("WM_DELETE_WINDOW", self.exit)

    # Method to close the speed test result window and attempt to re-enable the speed test button on the master window
    def exit(self):
        self.speedTestWindowObject.destroy()
        try:
            masterWindow.masterWindowObject.btnSpeedTest["state"] = "normal"
        except:
            pass


# Class for schedule window
class Schedule:

    # Setting constructor attribute values
    def __init__(self, scheduleWindowObject):
        self.scheduleWindowObject = scheduleWindowObject

        # Setting schedule window properties
        self.scheduleWindowObject.title("Schedule Tests")
        self.scheduleWindowObject.resizable(False, False)
        self.scheduleWindowObject.width = 500
        self.scheduleWindowObject.height = 260
        self.scheduleWindowObject.geometry(
            f"{self.scheduleWindowObject.width}x{self.scheduleWindowObject.height}"
            f"+{center_x(self.scheduleWindowObject.width)}+{center_y(self.scheduleWindowObject.height)}")

        # Creating tkinter radio button/check button variables to access their associated button's "state"
        self.scheduleWindowObject.primaryChoice = tk.IntVar()
        self.scheduleWindowObject.monChoice = tk.IntVar()
        self.scheduleWindowObject.tuesChoice = tk.IntVar()
        self.scheduleWindowObject.wedChoice = tk.IntVar()
        self.scheduleWindowObject.thurChoice = tk.IntVar()
        self.scheduleWindowObject.friChoice = tk.IntVar()
        self.scheduleWindowObject.satChoice = tk.IntVar()
        self.scheduleWindowObject.sunChoice = tk.IntVar()
        self.scheduleWindowObject.unitChoice = tk.IntVar()

        # Creating the widgets for scheduling tests for repeated days of the week at a specified time
        self.scheduleWindowObject.rbRepeatOnDaysAndTime = tk.Radiobutton(scheduleWindowObject,
                                                                         text="Repeat on specific days and time:",
                                                                         variable=
                                                                         self.scheduleWindowObject.primaryChoice,
                                                                         value=1, command=self.repeatOnDaysAndTime)
        self.scheduleWindowObject.entRepeatOnDaysAndTime = tk.Entry(scheduleWindowObject, width=19)
        self.scheduleWindowObject.lblRepeatOnDaysAndTimeFormat = tk.Label(scheduleWindowObject,
                                                                          text="Please select the day and enter the "
                                                                               "time in the format of "
                                                                               "HH:MM (24hr time)")
        self.scheduleWindowObject.cbMonday = tk.Checkbutton(scheduleWindowObject, text="Mon",
                                                            variable=self.scheduleWindowObject.monChoice)
        self.scheduleWindowObject.cbTues = tk.Checkbutton(scheduleWindowObject, text="Tues",
                                                          variable=self.scheduleWindowObject.tuesChoice)
        self.scheduleWindowObject.cbWed = tk.Checkbutton(scheduleWindowObject, text="Wed",
                                                         variable=self.scheduleWindowObject.wedChoice)
        self.scheduleWindowObject.cbThur = tk.Checkbutton(scheduleWindowObject, text="Thur",
                                                          variable=self.scheduleWindowObject.thurChoice)
        self.scheduleWindowObject.cbFri = tk.Checkbutton(scheduleWindowObject, text="Fri",
                                                         variable=self.scheduleWindowObject.friChoice)
        self.scheduleWindowObject.cbSat = tk.Checkbutton(scheduleWindowObject, text="Sat",
                                                         variable=self.scheduleWindowObject.satChoice)
        self.scheduleWindowObject.cbSun = tk.Checkbutton(scheduleWindowObject, text="Sun",
                                                         variable=self.scheduleWindowObject.sunChoice)

        # Creating the widgets for scheduling tests for repeated periods of a specified time interval
        self.scheduleWindowObject.rbRepeatAfterPeriod = tk.Radiobutton(scheduleWindowObject,
                                                                       text="Repeat after a period of time:",
                                                                       variable=self.scheduleWindowObject.primaryChoice,
                                                                       value=2, command=self.repeatAfterPeriod)
        self.scheduleWindowObject.entRepeatAfterPeriod = tk.Entry(scheduleWindowObject, width=19)
        self.scheduleWindowObject.lblRepeatAfterPeriodFormat = tk.Label(scheduleWindowObject,
                                                                        text="Please enter a time period that is "
                                                                             "greater than or equal to 2 minutes")
        self.scheduleWindowObject.rbMins = tk.Radiobutton(scheduleWindowObject, text="Minutes",
                                                          variable=self.scheduleWindowObject.unitChoice, value=1)
        self.scheduleWindowObject.rbHrs = tk.Radiobutton(scheduleWindowObject, text="Hours",
                                                         variable=self.scheduleWindowObject.unitChoice, value=2)
        self.scheduleWindowObject.rbDays = tk.Radiobutton(scheduleWindowObject, text="Days",
                                                          variable=self.scheduleWindowObject.unitChoice, value=3)

        # Creating the confirm selection button and making it start a new thread to call the 'confirmSelection' method
        # to start the scheduled tests upon clicking
        self.scheduleWindowObject.btnConfirm = tk.Button(scheduleWindowObject, text="Confirm Selection",
                                                         command=lambda:
                                                         threading.Thread(target=self.confirmSelection).start())
        # Creating the 'scheduled tests in progress' label
        self.scheduleWindowObject.lblScheduledTestsInProgress = tk.Label(scheduleWindowObject,
                                                                         text="Scheduled tests in progress... Close "
                                                                              "the window to cancel the tests at any"
                                                                              " time")

        # Placing the widgets for scheduling tests for repeated days of the week at a specified time
        self.scheduleWindowObject.rbRepeatOnDaysAndTime.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=(5, 0))
        self.scheduleWindowObject.lblRepeatOnDaysAndTimeFormat.grid(row=1, column=0, sticky="w", padx=(30, 0))
        self.scheduleWindowObject.entRepeatOnDaysAndTime.grid(row=2, column=0, sticky="w", padx=(34, 0), pady=(5, 0))
        self.scheduleWindowObject.cbMonday.grid(row=3, column=0, sticky="w", padx=(29, 0), pady=(5, 0))
        self.scheduleWindowObject.cbTues.grid(row=3, column=0, sticky="w", padx=(80, 0), pady=(5, 0))
        self.scheduleWindowObject.cbWed.grid(row=3, column=0, sticky="w", padx=(131, 0), pady=(5, 0))
        self.scheduleWindowObject.cbThur.grid(row=3, column=0, sticky="w", padx=(182, 0), pady=(5, 0))
        self.scheduleWindowObject.cbFri.grid(row=3, column=0, sticky="w", padx=(233, 0), pady=(5, 0))
        self.scheduleWindowObject.cbSat.grid(row=3, column=0, sticky="w", padx=(284, 0), pady=(5, 0))
        self.scheduleWindowObject.cbSun.grid(row=3, column=0, sticky="w", padx=(335, 0), pady=(5, 0))

        # Placing the widgets for scheduling tests for repeated periods of a specified time interval
        self.scheduleWindowObject.rbRepeatAfterPeriod.grid(row=4, column=0, sticky="w", padx=(10, 0))
        self.scheduleWindowObject.lblRepeatAfterPeriodFormat.grid(row=5, column=0, sticky="w", padx=(30, 0))
        self.scheduleWindowObject.entRepeatAfterPeriod.grid(row=6, column=0, sticky="w", padx=(34, 0), pady=(5, 0))
        self.scheduleWindowObject.rbMins.grid(row=7, column=0, sticky="w", padx=(29, 0), pady=(5, 0))
        self.scheduleWindowObject.rbHrs.grid(row=7, column=0, sticky="w", padx=(97, 0), pady=(5, 0))
        self.scheduleWindowObject.rbDays.grid(row=7, column=0, sticky="w", padx=(165, 0), pady=(5, 0))

        # Placing the confirm selection button
        self.scheduleWindowObject.btnConfirm.place(relx=0.5, rely=0.85, anchor="center")

        # Disabling buttons upon schedule window opening
        self.scheduleWindowObject.entRepeatOnDaysAndTime.config(state="disabled")
        self.scheduleWindowObject.lblRepeatOnDaysAndTimeFormat.config(state="disabled")
        self.scheduleWindowObject.cbMonday.config(state="disabled")
        self.scheduleWindowObject.cbTues.config(state="disabled")
        self.scheduleWindowObject.cbWed.config(state="disabled")
        self.scheduleWindowObject.cbThur.config(state="disabled")
        self.scheduleWindowObject.cbFri.config(state="disabled")
        self.scheduleWindowObject.cbSat.config(state="disabled")
        self.scheduleWindowObject.cbSun.config(state="disabled")

        self.scheduleWindowObject.entRepeatAfterPeriod.config(state="disabled")
        self.scheduleWindowObject.lblRepeatAfterPeriodFormat.config(state="disabled")
        self.scheduleWindowObject.rbMins.config(state="disabled")
        self.scheduleWindowObject.rbHrs.config(state="disabled")
        self.scheduleWindowObject.rbDays.config(state="disabled")
        self.scheduleWindowObject.btnConfirm.config(state="disabled")

        # Calling the method to close the schedule window and re-enable the 'speed test' and 'schedule tests' buttons on
        # the master window when an attempt is made to close the schedule window
        self.scheduleWindowObject.protocol("WM_DELETE_WINDOW", self.exit)

        # Creating a 'stop' event variable to help terminate the thread once the schedule window is destroyed during a
        # scheduled test
        global stopEvent
        stopEvent = threading.Event()

    # Method to close the schedule window, set the 'stopEvent to be "set" in order to let the thread terminate, and
    # attempt to re-enable the 'speed test' and 'schedule tests' buttons on the master window
    def exit(self):
        stopEvent.set()
        self.scheduleWindowObject.destroy()
        try:
            masterWindow.masterWindowObject.btnSpeedTest["state"] = "normal"
            masterWindow.masterWindowObject.btnScheduleTests["state"] = "normal"
        except:
            pass

    # Method to disable all other labels (apart from the primary radio buttons) and re-enable the 'confirm selection'
    # button when the first ('repeatOnDaysAndTime') radio button is clicked
    def repeatOnDaysAndTime(self):
        self.scheduleWindowObject.entRepeatOnDaysAndTime.config(state="normal")
        self.scheduleWindowObject.lblRepeatOnDaysAndTimeFormat.config(state="normal")
        self.scheduleWindowObject.cbMonday.config(state="normal")
        self.scheduleWindowObject.cbTues.config(state="normal")
        self.scheduleWindowObject.cbWed.config(state="normal")
        self.scheduleWindowObject.cbThur.config(state="normal")
        self.scheduleWindowObject.cbFri.config(state="normal")
        self.scheduleWindowObject.cbSat.config(state="normal")
        self.scheduleWindowObject.cbSun.config(state="normal")

        self.scheduleWindowObject.entRepeatAfterPeriod.config(state="disabled")
        self.scheduleWindowObject.lblRepeatAfterPeriodFormat.config(state="disabled")
        self.scheduleWindowObject.rbMins.config(state="disabled")
        self.scheduleWindowObject.rbHrs.config(state="disabled")
        self.scheduleWindowObject.rbDays.config(state="disabled")

        self.scheduleWindowObject.btnConfirm.config(state="normal")

    # Method to disable all other labels (apart from the primary radio buttons) and re-enable the 'confirm selection'
    # button when the first ('repeatAfterPeriod') radio button is clicked
    def repeatAfterPeriod(self):
        self.scheduleWindowObject.entRepeatOnDaysAndTime.config(state="disabled")
        self.scheduleWindowObject.lblRepeatOnDaysAndTimeFormat.config(state="disabled")
        self.scheduleWindowObject.cbMonday.config(state="disabled")
        self.scheduleWindowObject.cbTues.config(state="disabled")
        self.scheduleWindowObject.cbWed.config(state="disabled")
        self.scheduleWindowObject.cbThur.config(state="disabled")
        self.scheduleWindowObject.cbFri.config(state="disabled")
        self.scheduleWindowObject.cbSat.config(state="disabled")
        self.scheduleWindowObject.cbSun.config(state="disabled")

        self.scheduleWindowObject.entRepeatAfterPeriod.config(state="normal")
        self.scheduleWindowObject.lblRepeatAfterPeriodFormat.config(state="normal")
        self.scheduleWindowObject.rbMins.config(state="normal")
        self.scheduleWindowObject.rbHrs.config(state="normal")
        self.scheduleWindowObject.rbDays.config(state="normal")

        self.scheduleWindowObject.btnConfirm.config(state="normal")

    # Method to disable all buttons on the schedule window
    def disableAllScheduleWidgets(self):
        self.scheduleWindowObject.rbRepeatOnDaysAndTime.config(state="disabled")
        self.scheduleWindowObject.rbRepeatAfterPeriod.config(state="disabled")
        self.scheduleWindowObject.entRepeatOnDaysAndTime.config(state="disabled")
        self.scheduleWindowObject.lblRepeatOnDaysAndTimeFormat.config(state="disabled")
        self.scheduleWindowObject.cbMonday.config(state="disabled")
        self.scheduleWindowObject.cbTues.config(state="disabled")
        self.scheduleWindowObject.cbWed.config(state="disabled")
        self.scheduleWindowObject.cbThur.config(state="disabled")
        self.scheduleWindowObject.cbFri.config(state="disabled")
        self.scheduleWindowObject.cbSat.config(state="disabled")
        self.scheduleWindowObject.cbSun.config(state="disabled")

        self.scheduleWindowObject.entRepeatAfterPeriod.config(state="disabled")
        self.scheduleWindowObject.lblRepeatAfterPeriodFormat.config(state="disabled")
        self.scheduleWindowObject.rbMins.config(state="disabled")
        self.scheduleWindowObject.rbHrs.config(state="disabled")
        self.scheduleWindowObject.rbDays.config(state="disabled")
        self.scheduleWindowObject.btnConfirm.config(state="disabled")

    # Method to run the scheduled tests
    def confirmSelection(self):

        # Inner function to run a test
        def testOnDayAndTime():
            # Trying to conduct a speed test and a result window
            try:
                # Conducting the speed test
                speedtestObject = speedtest.Speedtest()
                # Dividing by 10^6 in order to give download and upload results in megabits per second, and then
                # rounding all results to 2 decimal places
                downloadResult = round(speedtestObject.download() / (10 ** 6), 2)
                uploadResult = round(speedtestObject.upload() / (10 ** 6), 2)
                pingResult = round(speedtestObject.results.ping, 2)

                # Tries to connect to the 'LocalResults.db' database (or automatically creates one if it doesn't yet
                # exist) with the definitions outlined in the design phase
                try:
                    localResultDb = sqlite3.connect("LocalResults.db")
                    localResultDbCursor = localResultDb.cursor()
                    localResultDbCursor.execute(
                        """CREATE TABLE IF NOT EXISTS LocalResults (
                        resultID INTEGER PRIMARY KEY,
                        download REAL NOT NULL,
                        upload REAL NOT NULL,
                        ping REAL NOT NULL,
                        date_time TEXT NOT NULL
                        )"""
                    )
                    # Inserting the calculated speed test values into the database
                    localResultDbCursor.execute("INSERT INTO LocalResults (download, upload, ping, date_time) "
                                                "VALUES (?, ?, ?, datetime('now', 'localtime'))",
                                                (downloadResult, uploadResult, pingResult))
                    # Committing the transaction
                    localResultDb.commit()
                # If an exception occurs, the program will throw an error window explaining an error in connecting to
                # the database
                except:
                    # Destroys the schedule window
                    self.scheduleWindowObject.destroy()
                    # Re-enables the 'speed test' and 'schedule tests' buttons on the master window
                    masterWindow.masterWindowObject.btnSpeedTest["state"] = "normal"
                    masterWindow.masterWindowObject.btnScheduleTests["state"] = "normal"
                    messagebox.showerror("Connection Error",
                                         "There has been an error connecting to the local database.")
                    # Returns out of the function so that schedule can be ended
                    return

                # Always closes the cursor and database connection at the end
                finally:
                    localResultDbCursor.close()
                    localResultDb.close()

                # Trying to connect to the online database and insert the results if the user is logged in with a
                # username
                if masterWindow.masterWindowObject.username is not None:
                    try:
                        # Connecting to the database
                        with mysql.connector.connect(
                                host=os.getenv("MYSQL_HOST"),
                                user=os.getenv("MYSQL_USER"),
                                passwd=os.getenv("MYSQL_PASSWD"),
                                database=os.getenv("MYSQL_DATABASE")
                        ) as onlineAccountDb:
                            # Creating a cursor to manipulate the database
                            with onlineAccountDb.cursor() as onlineAccountDbCursor:
                                # Retrieving the correct userID of the logged-in user using their username
                                onlineAccountDbCursor.execute("SELECT userID FROM User WHERE username = %s",
                                                              (masterWindow.masterWindowObject.username,))
                                userID = onlineAccountDbCursor.fetchone()[0]
                                # Finding the MAC address of this machine
                                macAddress = getmac.get_mac_address()
                                # Finding the current date and time
                                currentDateTime = datetime.datetime.now()
                                # Formatting the current date and time into MySQL DATETIME format
                                currentDateTime = currentDateTime.strftime("%Y-%m-%d %H:%M:%S")
                                # Finding the name of the current device
                                deviceName = socket.gethostname()
                                # Checking if the device is already registered
                                onlineAccountDbCursor.execute("SELECT * From Device WHERE deviceMAC = %s",
                                                              (macAddress,))
                                # Registering the current device on the 'Device' table only if it isn't already
                                # registered
                                if onlineAccountDbCursor.fetchone() is None:
                                    onlineAccountDbCursor.execute("INSERT INTO Device (deviceMAC, deviceName) "
                                                                  "VALUES (%s, %s)", (macAddress, deviceName))
                                    # Committing the transaction
                                    onlineAccountDb.commit()
                                # Checking if an entry already exists in the 'User-Device Link' table
                                onlineAccountDbCursor.execute("SELECT * From UserDeviceLink WHERE "
                                                              "userID = %s AND deviceMAC = %s", (userID, macAddress))
                                # Inserting a row into the 'User-Device Link' table (to indicate which user uses/has
                                # used which device) only if there is no existing row already
                                if onlineAccountDbCursor.fetchone() is None:
                                    onlineAccountDbCursor.execute("INSERT INTO UserDeviceLink (userID, deviceMAC) "
                                                                  "VALUES (%s, %s)", (userID, macAddress))
                                    # Committing the transaction
                                    onlineAccountDb.commit()
                                # Inserting the result data into the Result table
                                onlineAccountDbCursor.execute(
                                    """INSERT INTO Result (userID, deviceMAC, download, upload, ping, date_time) 
                                    VALUES (%s, %s, %s, %s, %s, %s)""", (userID, macAddress, downloadResult,
                                                                         uploadResult, pingResult, currentDateTime))
                                # Committing the transaction
                                onlineAccountDb.commit()
                    # Otherwise, shows an error message with the database connection and asking to check internet
                    # connection
                    except:
                        # Destroys the schedule window
                        self.scheduleWindowObject.destroy()
                        # Displays a connection error
                        # Re-enables the 'speed test' and 'schedule tests' buttons on the master window
                        masterWindow.masterWindowObject.btnSpeedTest["state"] = "normal"
                        masterWindow.masterWindowObject.btnScheduleTests["state"] = "normal"
                        messagebox.showerror("Connection Error",
                                             "There has been an error connecting to the database. "
                                             "Please check internet connection.")
                        # Returns out of the function so that schedule can be ended
                        return
            # Otherwise, shows an error message with speedtest server connection and asking to check internet connection
            except:
                # Destroys the schedule window
                self.scheduleWindowObject.destroy()
                # Displays a connection error
                # Re-enables the 'speed test' and 'schedule tests' buttons on the master window
                masterWindow.masterWindowObject.btnSpeedTest["state"] = "normal"
                masterWindow.masterWindowObject.btnScheduleTests["state"] = "normal"
                messagebox.showerror("Connection Error",
                                     "There has been an error connecting to the speedtest servers. "
                                     "Please check internet connection.")
                # Returns out of the function so that schedule can be ended
                return

        # Defines a small interval error window
        def errorWindow():
            messagebox.showerror("Interval too small",
                                 "The time interval input is too small. Please input a bigger time interval.")

        # Tries to run the schedule process
        try:
            # Checks whether any of the day choices have been selected if the first option has been selected and also
            # gets the time entered by the user
            # and attempts to make a schedule on that day
            if self.scheduleWindowObject.primaryChoice.get() == 1:
                inputTime = self.scheduleWindowObject.entRepeatOnDaysAndTime.get()
                if self.scheduleWindowObject.monChoice.get() == 1:
                    schedule.every().monday.at(inputTime).do(testOnDayAndTime)
                if self.scheduleWindowObject.tuesChoice.get() == 1:
                    schedule.every().tuesday.at(inputTime).do(testOnDayAndTime)
                if self.scheduleWindowObject.wedChoice.get() == 1:
                    schedule.every().wednesday.at(inputTime).do(testOnDayAndTime)
                if self.scheduleWindowObject.thurChoice.get() == 1:
                    schedule.every().thursday.at(inputTime).do(testOnDayAndTime)
                if self.scheduleWindowObject.friChoice.get() == 1:
                    schedule.every().friday.at(inputTime).do(testOnDayAndTime)
                if self.scheduleWindowObject.satChoice.get() == 1:
                    schedule.every().saturday.at(inputTime).do(testOnDayAndTime)
                if self.scheduleWindowObject.sunChoice.get() == 1:
                    schedule.every().sunday.at(inputTime).do(testOnDayAndTime)
                # Displays an error if none of the options have been selected from the first option
                if not (1 in {self.scheduleWindowObject.monChoice.get(),
                              self.scheduleWindowObject.tuesChoice.get(),
                              self.scheduleWindowObject.wedChoice.get(),
                              self.scheduleWindowObject.thurChoice.get(),
                              self.scheduleWindowObject.friChoice.get(),
                              self.scheduleWindowObject.satChoice.get(),
                              self.scheduleWindowObject.sunChoice.get()}):
                    messagebox.showerror("Empty Selection",
                                         "Please select at least 1 day of the week.")
                    return
                # If choice data has been successfully taken, all widgets on the schedule window will be disabled
                self.disableAllScheduleWidgets()
                # Placing the 'scheduled tests in progress' label
                self.scheduleWindowObject.lblScheduledTestsInProgress.place(relx=0.5, rely=0.95, anchor="center")
                # Continuously checks and runs any pending jobs - if the stopEvent is "set" then the loop is broken and
                # the thread + window is destroyed
                while True:
                    if stopEvent.is_set():
                        break
                    schedule.run_pending()
                    time.sleep(1)
            # Checks whether any of the unit of time options have been selected if the second option has been selected
            # and attempts to get the numerical value
            # entered by the user
            elif self.scheduleWindowObject.primaryChoice.get() == 2:
                numericalInterval = int(self.scheduleWindowObject.entRepeatAfterPeriod.get())
                # Displays the defined error window if the 'minute' option is selected and the value input is <1.
                # Otherwise, creates a schedule for that time interval
                if self.scheduleWindowObject.unitChoice.get() == 1:
                    if numericalInterval < 2:
                        errorWindow()
                    else:
                        schedule.every(numericalInterval).minutes.do(testOnDayAndTime)
                # Displays the defined error window if the 'hour' option is selected and the value input is <1.
                # Otherwise, creates a schedule for that time interval
                elif self.scheduleWindowObject.unitChoice.get() == 2:
                    if numericalInterval < 1:
                        errorWindow()
                    else:
                        schedule.every(numericalInterval).hours.do(testOnDayAndTime)
                # Displays the defined error window if the 'day' option is selected and the value input is <1.
                # Otherwise, creates a schedule for that time interval
                elif self.scheduleWindowObject.unitChoice.get() == 3:
                    if numericalInterval < 1:
                        errorWindow()
                    else:
                        schedule.every(numericalInterval).days.do(testOnDayAndTime)
                # Otherwise, Displays an error if none of the time unit options have been selected
                else:
                    messagebox.showerror("Empty Selection",
                                         "Please select one of the units of time provided.")
                    return
                # If choice data has been successfully taken, all widgets on the schedule window will be disabled
                self.disableAllScheduleWidgets()
                # Placing the 'scheduled tests in progress' label
                self.scheduleWindowObject.lblScheduledTestsInProgress.place(relx=0.5, rely=0.95, anchor="center")
                # Continuously checks and runs any pending jobs - if the stopEvent is "set" then the loop is broken and
                # the thread + window is destroyed
                while True:
                    if stopEvent.is_set():
                        break
                    schedule.run_pending()
                    time.sleep(1)
        # Otherwise, displays an error message (which can only occur here if none of the options are selected)
        except:
            messagebox.showerror("Invalid Input",
                                 "Please enter a valid input.")


# Class for the result history window
class ResultHistory:

    # Setting constructor attribute values
    def __init__(self, resultHistoryWindowObject):
        self.resultHistoryWindowObject = resultHistoryWindowObject

        # Setting result history window properties
        self.resultHistoryWindowObject.title("Result History")
        self.resultHistoryWindowObject.resizable(False, False)
        self.resultHistoryWindowObject.width = 267
        self.resultHistoryWindowObject.height = 40
        self.resultHistoryWindowObject.geometry(
            f"{self.resultHistoryWindowObject.width}x{self.resultHistoryWindowObject.height}"
            f"+{center_x(self.resultHistoryWindowObject.width)}+{center_y(self.resultHistoryWindowObject.height)}")

        # Creating the local and online log buttons
        self.resultHistoryWindowObject.btnLocal = tk.Button(resultHistoryWindowObject, text="Local Device History",
                                                            command=self.createLocalHistoryWindow)
        self.resultHistoryWindowObject.btnOnline = tk.Button(resultHistoryWindowObject, text="Online Database Logs",
                                                             command=self.createOnlineDeviceChoice)

        # Placing the local and online buttons
        self.resultHistoryWindowObject.btnLocal.grid(row=0, column=0, padx=(10, 0), pady=(7, 0))
        self.resultHistoryWindowObject.btnOnline.grid(row=0, column=1, padx=(5, 0), pady=(7, 0))

        # Runs the exit method when the user attempts to close the result window
        self.resultHistoryWindowObject.protocol("WM_DELETE_WINDOW", self.exit)

    # Method to exit the window and attempt to re-enable the result history button on master window
    def exit(self):
        self.resultHistoryWindowObject.destroy()
        try:
            masterWindow.masterWindowObject.btnResultHistory.config(state="normal")
        except:
            pass

    # Method to create an instance of the local history window class
    def createLocalHistoryWindow(self):
        self.resultHistoryWindowObject.destroy()
        global localHistoryWindow
        localHistoryWindow = tk.Toplevel()
        localHistoryWindow = LocalHistory(localHistoryWindow)

    # Method to create an instance of the online database device choice window if the user is signed in
    def createOnlineDeviceChoice(self):
        # Shows an error if the user is not signed in, asking them to sign in to be able to view online database speed
        # test records for an account
        if masterWindow.masterWindowObject.username is None:
            messagebox.showerror("Not Signed In",
                                 "You are not signed in with an account. To view the online database speed test "
                                 "records for an account, please sign in.")
        # Otherwise, creates an instance of the online database device choice window
        else:
            self.resultHistoryWindowObject.destroy()
            global onlineDeviceChoiceWindow
            onlineDeviceChoiceWindow = tk.Toplevel()
            onlineDeviceChoiceWindow = OnlineDeviceChoice(onlineDeviceChoiceWindow)


# Class for the local result history window
class LocalHistory:

    # Setting constructor attribute properties
    def __init__(self, localHistoryWindowObject):
        self.localHistoryWindowObject = localHistoryWindowObject

        # Setting local history window properties
        self.localHistoryWindowObject.title("Local History")
        self.localHistoryWindowObject.resizable(False, False)
        self.localHistoryWindowObject.width = 625
        self.localHistoryWindowObject.height = 272
        self.localHistoryWindowObject.geometry(
            f"{self.localHistoryWindowObject.width}x{self.localHistoryWindowObject.height}"
            f"+{center_x(self.localHistoryWindowObject.width)}+{center_y(self.localHistoryWindowObject.height)}")

        # Creating and placing a frame to put the table of results in
        self.localHistoryWindowObject.tableFrame = tk.Frame(localHistoryWindowObject)
        self.localHistoryWindowObject.tableFrame.grid(row=0, column=0)
        # Creating and placing the scroll bar for the table
        self.localHistoryWindowObject.tableScrollbar = ttk.Scrollbar(self.localHistoryWindowObject.tableFrame)
        self.localHistoryWindowObject.tableScrollbar.grid(row=0, column=1, sticky="ns")
        # Creating and placing the refresh button on the window
        self.localHistoryWindowObject.btnRefreshTableAndGraphs = tk.Button(localHistoryWindowObject,
                                                                           text="Refresh table and graphs",
                                                                           command=self.refresh)
        self.localHistoryWindowObject.btnRefreshTableAndGraphs.grid(row=1, column=0, pady=(10, 0))

        # Creating table and setting the scroll bar to be in control of scrolling up and down the table
        self.localHistoryWindowObject.table = ttk.Treeview(self.localHistoryWindowObject.tableFrame,
                                                           yscrollcommand=
                                                           self.localHistoryWindowObject.tableScrollbar.set)

        # Setting the table columns
        self.localHistoryWindowObject.table["columns"] = ("resultID", "download", "upload", "ping", "datetime")
        # Formatting the defined columns
        self.localHistoryWindowObject.table.column("#0", width=0, stretch=False)
        self.localHistoryWindowObject.table.column("resultID", minwidth=25, width=60)
        self.localHistoryWindowObject.table.column("download", minwidth=25, width=140)
        self.localHistoryWindowObject.table.column("upload", minwidth=25, width=125)
        self.localHistoryWindowObject.table.column("ping", minwidth=25, width=60)
        self.localHistoryWindowObject.table.column("datetime", minwidth=25, width=220)
        # Create table headings
        self.localHistoryWindowObject.table.heading("#0", text="")
        self.localHistoryWindowObject.table.heading("resultID", text="Result ID", anchor="w")
        self.localHistoryWindowObject.table.heading("download", text="Download Speed (Mbps)", anchor="w")
        self.localHistoryWindowObject.table.heading("upload", text="Upload Speed (Mbps)", anchor="w")
        self.localHistoryWindowObject.table.heading("ping", text="Ping (ms)", anchor="w")
        self.localHistoryWindowObject.table.heading("datetime", text="Date and Time (YYYY-mm-dd HH:MM)", anchor="w")

        # Calling the exit method if the user attempts to close the local result window
        self.localHistoryWindowObject.protocol("WM_DELETE_WINDOW", self.exit)

        # Attempting to connect to the database/create table if it doesn't already exist
        try:
            localResultDb = sqlite3.connect("LocalResults.db")
            localResultDbCursor = localResultDb.cursor()
            localResultDbCursor.execute(
                """CREATE TABLE IF NOT EXISTS LocalResults (
                resultID INTEGER PRIMARY KEY,
                download REAL NOT NULL,
                upload REAL NOT NULL,
                ping REAL NOT NULL,
                date_time TEXT NOT NULL
                )"""
            )
            # Fetches all the rows in the local database
            localResultDbCursor.execute("SELECT * FROM LocalResults")
            results = localResultDbCursor.fetchall()
            # if no results are found, the exit method is called and an error message appears which explains that they
            # need to conduct a speed test before they are able to view local database history
            if not results:
                self.exit()
                messagebox.showerror("No Speed Test Data",
                                     "You have not yet conducted a speed test on this machine.  "
                                     "Please conduct a speed test before attempting to view local database history.")
                return
        # Otherwise, calls the exit method and displays a connection error
        except:
            self.exit()
            messagebox.showerror("Connection Error",
                                 "There has been an error connecting to the database.")
            return

        # Creating the data lists for the values that will be used to plot the graphs
        times = []
        downloadVals = []
        uploadVals = []
        pingVals = []
        # Inserts all fetched results into the tkinter table and the data lists from before
        for row in results:
            self.localHistoryWindowObject.table.insert(parent="", index="end", iid=row[0], text="", values=row)
            times.append(datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"))
            downloadVals.append(row[1])
            uploadVals.append(row[2])
            pingVals.append(row[3])

        # Placing the table
        self.localHistoryWindowObject.table.grid(row=0, column=0)
        # Enabling the scroll bar to scroll through the table results
        self.localHistoryWindowObject.tableScrollbar.config(command=self.localHistoryWindowObject.table.yview)

        # Creating the download speed vs date-time graph
        plt.figure("Download Speed vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, downloadVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Download Speed (Mbps)")
        plt.suptitle("Download Speed vs Date-Time")

        # Creating the upload speed vs date-time graph
        plt.figure("Upload Speed vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, uploadVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Upload Speed (Mbps)")
        plt.suptitle("Upload Speed vs Date-Time")

        # Creating the ping vs date-time graph
        plt.figure("Ping vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, pingVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Ping (ms)")
        plt.suptitle("Ping vs Date-Time")

        # Displaying the graphs
        plt.show(block=False)

    # Method to exit the local result window and attempt tp re-enable the result history button on the master window
    def exit(self):
        self.localHistoryWindowObject.destroy()
        try:
            masterWindow.masterWindowObject.btnResultHistory.config(state="normal")
        except:
            pass

    # Method to refresh the data in the table and the graphs
    def refresh(self):
        # Attempting to connect to the database/create table if it doesn't already exist
        try:
            localResultDb = sqlite3.connect("LocalResults.db")
            localResultDbCursor = localResultDb.cursor()
            localResultDbCursor.execute(
                """CREATE TABLE IF NOT EXISTS LocalResults (
                resultID INTEGER PRIMARY KEY,
                download REAL NOT NULL,
                upload REAL NOT NULL,
                ping REAL NOT NULL,
                date_time TEXT NOT NULL
                )"""
            )
            # Fetches all the rows in the local database
            localResultDbCursor.execute("SELECT * FROM LocalResults")
            results = localResultDbCursor.fetchall()
            # if no results are found, the exit method is called and an error message appears which explains that they
            # need to conduct a speed test before they are able to view local database history
            if not results:
                self.exit()
                messagebox.showerror("No Speed Test Data",
                                     "You have not yet conducted a speed test on this machine.  "
                                     "Please conduct a speed test before attempting to view local database history.")
                return
        # Otherwise, calls the exit method and displays a connection error
        except:
            self.exit()
            messagebox.showerror("Connection Error",
                                 "There has been an error connecting to the database.")
            return
        # Deletes all current items in the tkinter table
        for item in self.localHistoryWindowObject.table.get_children():
            self.localHistoryWindowObject.table.delete(item)

        # Creating the data lists for the values that will be used to plot the graphs
        times = []
        downloadVals = []
        uploadVals = []
        pingVals = []
        # Inserts all fetched results into the tkinter table and the data lists from before
        for row in results:
            self.localHistoryWindowObject.table.insert(parent="", index="end", iid=row[0], text="", values=row)
            times.append(datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"))
            downloadVals.append(row[1])
            uploadVals.append(row[2])
            pingVals.append(row[3])

        # Deletes all the current graphs
        plt.close()
        # Creating the download speed vs date-time graph
        plt.figure("Download Speed vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, downloadVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Download Speed (Mbps)")
        plt.suptitle("Download Speed vs Date-Time")

        # Creating the upload speed vs date-time graph
        plt.figure("Upload Speed vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, uploadVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Upload Speed (Mbps)")
        plt.suptitle("Upload Speed vs Date-Time")

        # Creating the ping vs date-time graph
        plt.figure("Ping vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, pingVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Ping (ms)")
        plt.suptitle("Ping vs Date-Time")

        # Displaying the graphs
        plt.show(block=False)

# Class for the online database device choice window
class OnlineDeviceChoice:
    # Setting constructor attribute properties
    def __init__(self, onlineDeviceChoiceWindowObject):
        self.onlineDeviceChoiceWindowObject = onlineDeviceChoiceWindowObject

        # Setting online database device choice window properties
        self.onlineDeviceChoiceWindowObject.title("Online Database Device History Choice")
        self.onlineDeviceChoiceWindowObject.resizable(False, False)
        self.onlineDeviceChoiceWindowObject.width = 400
        self.onlineDeviceChoiceWindowObject.height = 135
        self.onlineDeviceChoiceWindowObject.geometry(
            f"{self.onlineDeviceChoiceWindowObject.width}x{self.onlineDeviceChoiceWindowObject.height}"
            f"+{center_x(self.onlineDeviceChoiceWindowObject.width)}+"
            f"{center_y(self.onlineDeviceChoiceWindowObject.height)}")

        # Creating the devices list
        self.onlineDeviceChoiceWindowObject.devices = []

        # Trying to get the list of devices that speed tests have been done on with the current signed-in account
        try:
            # Connecting to the online database
            with mysql.connector.connect(
                    host=os.getenv("MYSQL_HOST"),
                    user=os.getenv("MYSQL_USER"),
                    passwd=os.getenv("MYSQL_PASSWD"),
                    database=os.getenv("MYSQL_DATABASE")
            ) as onlineAccountDb:
                # Creating a cursor to manipulate the database
                with onlineAccountDb.cursor() as onlineAccountDbCursor:
                    # Getting the userID of the user
                    onlineAccountDbCursor.execute("SELECT userID FROM User WHERE username = %s",
                                                  (masterWindow.masterWindowObject.username,))
                    userID = onlineAccountDbCursor.fetchone()[0]
                    # Getting a list of MAC addresses of all the devices that speed tests have been done on with the
                    # current signed-in account
                    onlineAccountDbCursor.execute("SELECT deviceMAC FROM UserDeviceLink WHERE userID = %s",
                                                  (userID,))
                    self.onlineDeviceChoiceWindowObject.deviceMACs = onlineAccountDbCursor.fetchall()
                    # Checks if the list of account-associated device MAC addresses is empty which would mean that the
                    # user has not conducted a speed test with the account yet
                    if not self.onlineDeviceChoiceWindowObject.deviceMACs:
                        # If it is, the window exit function is called
                        self.exit()
                        # An error message appears which explains that they need to conduct a speed test before they are
                        # able to view online database logs
                        messagebox.showerror("No Speed Test Data",
                                             "You have not yet conducted a speed test with this account.  "
                                             "Please conduct a speed test before attempting to view online database "
                                             "logs.")
                        return
                    # Adding the combination of the fetched device names and their MAC addresses to the devices list
                    for i in range(len(self.onlineDeviceChoiceWindowObject.deviceMACs)):
                        # Fetching the name of the device with the MAC address
                        onlineAccountDbCursor.execute("SELECT deviceName FROM Device WHERE deviceMAC = %s",
                                                      (self.onlineDeviceChoiceWindowObject.deviceMACs[i][0],))
                        deviceName = onlineAccountDbCursor.fetchone()[0]
                        # Adding the combination of the device name and its MAC address to the devices list
                        self.onlineDeviceChoiceWindowObject.devices.append(
                            f"{deviceName} ({self.onlineDeviceChoiceWindowObject.deviceMACs[i][0]})"
                        )

        # Otherwise, calls the exit method and shows an error message with the database connection, asking to check
        # internet connection
        except:
            self.exit()
            # Displays a connection error
            messagebox.showerror("Connection Error",
                                 "There has been an error connecting to the database. "
                                 "Please check internet connection.")
            return

        # Creating the label to ask the user to select a device
        self.onlineDeviceChoiceWindowObject.lblSelect = tk.Label(onlineDeviceChoiceWindowObject,
                                                                 text="Please select a device from the dropdown "
                                                                      "selection.\n(if no devices appear then you have "
                                                                      "not yet\nconducted a speed test with this "
                                                                      "account.)")

        # Creating the variable to store the device selected
        self.onlineDeviceChoiceWindowObject.selection = tk.StringVar()
        # Creating the drop-down menu which will display the devices
        self.onlineDeviceChoiceWindowObject.dropdownDeviceSelect = tk.OptionMenu(
            onlineDeviceChoiceWindowObject, self.onlineDeviceChoiceWindowObject.selection,
            *self.onlineDeviceChoiceWindowObject.devices
        )

        # Creating the confirm selection button
        self.onlineDeviceChoiceWindowObject.btnConfirmSelection = tk.Button(onlineDeviceChoiceWindowObject,
                                                                            text="Confirm Selection",
                                                                            command=self.confirmSelection)

        # Placing the label, drop-down menu, and button
        self.onlineDeviceChoiceWindowObject.lblSelect.pack(pady=(5, 0))
        self.onlineDeviceChoiceWindowObject.dropdownDeviceSelect.pack(pady=(5, 0))
        self.onlineDeviceChoiceWindowObject.btnConfirmSelection.pack(pady=(5, 0))

        # Calling the exit function if the user clicks the default, top-right windows exit button to attempt to close
        # the window
        self.onlineDeviceChoiceWindowObject.protocol("WM_DELETE_WINDOW", self.exit)

    # Method to exit the window and attempt tp re-enable the result history button on master window
    def exit(self):
        self.onlineDeviceChoiceWindowObject.destroy()
        try:
            masterWindow.masterWindowObject.btnResultHistory.config(state="normal")
        except:
            pass

    def confirmSelection(self):
        chosenDevice = self.onlineDeviceChoiceWindowObject.selection.get()
        try:
            indexOfChosenDeviceInDeviceList = self.onlineDeviceChoiceWindowObject.devices.index(chosenDevice)
            chosenDeviceMAC = self.onlineDeviceChoiceWindowObject.deviceMACs[indexOfChosenDeviceInDeviceList][0]
            self.onlineDeviceChoiceWindowObject.destroy()
            global onlineHistoryWindow
            onlineHistoryWindow = tk.Toplevel()
            onlineHistoryWindow = OnlineHistory(onlineHistoryWindow, chosenDevice, chosenDeviceMAC)
        except:
            pass


# Class for the online result history window
class OnlineHistory:

    # Setting constructor attribute properties
    def __init__(self, onlineHistoryWindowObject, chosenDevice, chosenDeviceMAC):
        self.onlineHistoryWindowObject = onlineHistoryWindowObject
        self.onlineHistoryWindowObject.chosenDeviceMAC = chosenDeviceMAC

        # Setting online history window properties
        self.onlineHistoryWindowObject.title(f"{chosenDevice} Online Database Result History")
        self.onlineHistoryWindowObject.resizable(False, False)
        self.onlineHistoryWindowObject.width = 625
        self.onlineHistoryWindowObject.height = 272
        self.onlineHistoryWindowObject.geometry(
            f"{self.onlineHistoryWindowObject.width}x{self.onlineHistoryWindowObject.height}"
            f"+{center_x(self.onlineHistoryWindowObject.width)}+{center_y(self.onlineHistoryWindowObject.height)}")

        # Creating and placing a frame to put the table of results in
        self.onlineHistoryWindowObject.tableFrame = tk.Frame(onlineHistoryWindowObject)
        self.onlineHistoryWindowObject.tableFrame.grid(row=0, column=0)
        # Creating and placing the scroll bar for the table
        self.onlineHistoryWindowObject.tableScrollbar = ttk.Scrollbar(self.onlineHistoryWindowObject.tableFrame)
        self.onlineHistoryWindowObject.tableScrollbar.grid(row=0, column=1, sticky="ns")
        # Creating and placing the refresh button on the window
        self.onlineHistoryWindowObject.btnRefreshTableAndGraphs = tk.Button(onlineHistoryWindowObject,
                                                                            text="Refresh table and graphs",
                                                                            command=self.refresh)
        self.onlineHistoryWindowObject.btnRefreshTableAndGraphs.grid(row=1, column=0, pady=(10, 0))

        # Creating table and setting the scroll bar to be in control of scrolling up and down the table
        self.onlineHistoryWindowObject.table = ttk.Treeview(self.onlineHistoryWindowObject.tableFrame,
                                                            yscrollcommand=
                                                            self.onlineHistoryWindowObject.tableScrollbar.set)

        # Setting the table columns
        self.onlineHistoryWindowObject.table["columns"] = ("resultID", "download", "upload", "ping", "datetime")
        # Formatting the defined columns
        self.onlineHistoryWindowObject.table.column("#0", width=0, stretch=False)
        self.onlineHistoryWindowObject.table.column("resultID", minwidth=25, width=60)
        self.onlineHistoryWindowObject.table.column("download", minwidth=25, width=140)
        self.onlineHistoryWindowObject.table.column("upload", minwidth=25, width=125)
        self.onlineHistoryWindowObject.table.column("ping", minwidth=25, width=60)
        self.onlineHistoryWindowObject.table.column("datetime", minwidth=25, width=220)
        # Create table headings
        self.onlineHistoryWindowObject.table.heading("#0", text="")
        self.onlineHistoryWindowObject.table.heading("resultID", text="Result ID", anchor="w")
        self.onlineHistoryWindowObject.table.heading("download", text="Download Speed (Mbps)", anchor="w")
        self.onlineHistoryWindowObject.table.heading("upload", text="Upload Speed (Mbps)", anchor="w")
        self.onlineHistoryWindowObject.table.heading("ping", text="Ping (ms)", anchor="w")
        self.onlineHistoryWindowObject.table.heading("datetime", text="Date and Time (YYYY-mm-dd HH:MM)", anchor="w")

        # Calling the exit method if the user attempts to close the online database result window
        self.onlineHistoryWindowObject.protocol("WM_DELETE_WINDOW", self.exit)

        # Attempting to connect to the online database
        try:
            # Connecting to the online database
            with mysql.connector.connect(
                    host=os.getenv("MYSQL_HOST"),
                    user=os.getenv("MYSQL_USER"),
                    passwd=os.getenv("MYSQL_PASSWD"),
                    database=os.getenv("MYSQL_DATABASE")
            ) as onlineAccountDb:
                # Creating a cursor to manipulate the database
                with onlineAccountDb.cursor() as onlineAccountDbCursor:
                    # Getting the userID of the user
                    onlineAccountDbCursor.execute("SELECT userID FROM User WHERE username = %s",
                                                  (masterWindow.masterWindowObject.username,))
                    userID = onlineAccountDbCursor.fetchone()[0]
                    # Fetches the result rows from the Result table
                    onlineAccountDbCursor.execute("SELECT resultID, download, upload, ping, date_time FROM Result "
                                                  "WHERE userID = %s AND deviceMAC = %s",
                                                  (userID, self.onlineHistoryWindowObject.chosenDeviceMAC))
                    results = onlineAccountDbCursor.fetchall()
        # Otherwise, outputs a connection error if an error was encountered when attempting to connect to/interact with
        # the online database
        except:
            self.exit()
            messagebox.showerror("Connection Error",
                                 "There has been an error connecting to the database. "
                                 "Please check internet connection.")
            return
        # Creating the data lists for the values that will be used to plot the graphs
        times = []
        downloadVals = []
        uploadVals = []
        pingVals = []
        # Inserts all fetched results into the tkinter table and the data lists from before
        for row in results:
            # Converting the download, upload, and ping data into python floats and converting the date-times into
            # Python strings
            row = [row[0], float(row[1]), float(row[2]), float(row[3]), datetime.datetime.strftime(row[4],
                                                                                                   "%Y-%m-%d %H:%M:%S")]
            self.onlineHistoryWindowObject.table.insert(parent="", index="end", iid=row[0], text="", values=row)
            times.append(datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"))
            downloadVals.append(row[1])
            uploadVals.append(row[2])
            pingVals.append(row[3])

        # Placing the table
        self.onlineHistoryWindowObject.table.grid(row=0, column=0)
        # Enabling the scroll bar to scroll through the table results
        self.onlineHistoryWindowObject.tableScrollbar.config(command=self.onlineHistoryWindowObject.table.yview)

        # Creating the download speed vs date-time graph
        plt.figure("Download Speed vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, downloadVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Download Speed (Mbps)")
        plt.suptitle("Download Speed vs Date-Time")

        # Creating the upload speed vs date-time graph
        plt.figure("Upload Speed vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, uploadVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Upload Speed (Mbps)")
        plt.suptitle("Upload Speed vs Date-Time")

        # Creating the ping vs date-time graph
        plt.figure("Ping vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, pingVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Ping (ms)")
        plt.suptitle("Ping vs Date-Time")

        # Displaying the graphs
        plt.show(block=False)

    # Method to exit the online database result window and attempt to re-enable the result history button on the master
    # window
    def exit(self):
        self.onlineHistoryWindowObject.destroy()
        try:
            masterWindow.masterWindowObject.btnResultHistory.config(state="normal")
        except:
            pass

    # Method to refresh the data in the table and the graphs
    def refresh(self):
        # Attempting to connect to the online database
        try:
            # Connecting to the online database
            with mysql.connector.connect(
                    host=os.getenv("MYSQL_HOST"),
                    user=os.getenv("MYSQL_USER"),
                    passwd=os.getenv("MYSQL_PASSWD"),
                    database=os.getenv("MYSQL_DATABASE")
            ) as onlineAccountDb:
                # Creating a cursor to manipulate the database
                with onlineAccountDb.cursor() as onlineAccountDbCursor:
                    # Getting the userID of the user
                    onlineAccountDbCursor.execute("SELECT userID FROM User WHERE username = %s",
                                                  (masterWindow.masterWindowObject.username,))
                    userID = onlineAccountDbCursor.fetchone()[0]
                    # Fetches the result rows from the Result table
                    onlineAccountDbCursor.execute("SELECT resultID, download, upload, ping, date_time FROM Result "
                                                  "WHERE userID = %s AND deviceMAC = %s",
                                                  (userID, self.onlineHistoryWindowObject.chosenDeviceMAC))
                    results = onlineAccountDbCursor.fetchall()
        # Otherwise, outputs a connection error if an error was encountered when attempting to connect to/interact with
        # the online database
        except:
            messagebox.showerror("Connection Error",
                                 "There has been an error connecting to the database. "
                                 "Please check internet connection and refresh the window.")
            return
        # Deletes all current items in the tkinter table
        for item in self.onlineHistoryWindowObject.table.get_children():
            self.onlineHistoryWindowObject.table.delete(item)

        # Creating the data lists for the values that will be used to plot the graphs
        times = []
        downloadVals = []
        uploadVals = []
        pingVals = []
        # Inserts all fetched results into the tkinter table and the data lists from before
        for row in results:
            # Converting the download, upload, and ping data into python floats and converting the date-times into
            # Python strings
            row = [row[0], float(row[1]), float(row[2]), float(row[3]), datetime.datetime.strftime(row[4],
                                                                                                   "%Y-%m-%d %H:%M:%S")]
            self.onlineHistoryWindowObject.table.insert(parent="", index="end", iid=row[0], text="", values=row)
            times.append(datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"))
            downloadVals.append(row[1])
            uploadVals.append(row[2])
            pingVals.append(row[3])

        # Deletes all the current graphs
        plt.close()
        # Creating the download speed vs date-time graph
        plt.figure("Download Speed vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, downloadVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Download Speed (Mbps)")
        plt.suptitle("Download Speed vs Date-Time")

        # Creating the upload speed vs date-time graph
        plt.figure("Upload Speed vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, uploadVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Upload Speed (Mbps)")
        plt.suptitle("Upload Speed vs Date-Time")

        # Creating the ping vs date-time graph
        plt.figure("Ping vs Date-Time", figsize=(14, 8))
        plt.plot_date(times, pingVals)
        # Setting the x-axis to format the dates and times in a more user-friendly way
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter("%d/%m/%Y %H:%M:%S"))
        # Formatting the dates slightly to reduce clutter on the date-time axis
        plt.gcf().autofmt_xdate()
        # Setting the axis labels and title of the graph
        plt.xlabel("Date-Time")
        plt.ylabel("Ping (ms)")
        plt.suptitle("Ping vs Date-Time")

        # Displaying the graphs
        plt.show(block=False)


###########################################################
### Functions used by all the different window classes: ###
###########################################################

# Calculates appropriate x-coord for centering the window
def center_x(appWidth):
    return int(((screenWidth / 2) - (appWidth / 2)))

# Calculates appropriate y-coord for centering the window (taking into account Windows' title bar thickness)
def center_y(appHeight):
    return int(((screenHeight / 2) - (appHeight / 2) - 25))


####################
### Main Program ###
####################

def main():

    # Defining special characters
    global specialCharacters
    specialCharacters = """[!"#$%^=+-`¬;,£%'&*()<>?/\|}{~:]"""

    # Instantiating main menu window and globalising it as it is in a function and needs to be accessible to the whole
    # program
    global mainMenu
    mainMenu = tk.Tk()
    mainMenu = MainMenu(mainMenu)

# Checks if this module is the main module that is being run using the special '__name__' variable:
#   > '__name__' is a built-in variable in every module that has a default string value of the current module it is in.
#   > If the module it is in is the module being run, it is instead set to the string "__main__".
# It then executes the main program subroutine if it is the main module.
if __name__ == "__main__":
    main()
    tk.mainloop()
