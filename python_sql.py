'''required imports'''
from tkinter import *
from tkinter import ttk
import csv
import pyodbc
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import messagebox
from datetime import datetime

# global variables
first_timestamp_value = datetime.now()
last_timestamp_value = datetime.now()
table_names = []
table_names_string = []
table_names_string_replace = []
table_names_string_replace_2 = []
tag_names = []
tag_names_string = []
tag_names_string_replace = []
tag_names_string_replace_2 = []
values_between_dates = []
timestamp_values = []
int_values = []
NUMBER_OF_DATA_ENTRIES = None
CONN = None
CANVAS = None


# arrays for hour, minute, and second values
# array of hour candidates ranging from 0 - 23 
hours = []
for x in range(25):
    hours.append(str(x))
hours.append('00')
hours.append('01')
hours.append('02')
hours.append('03')
hours.append('04')
hours.append('05')
hours.append('06')
hours.append('07')
hours.append('08')
hours.append('09')
# array of minute candidates ranging from 0 - 59
minutes = []
for x in range(60):
    minutes.append(str(x))
minutes.append('00')
minutes.append('01')
minutes.append('02')
minutes.append('03')
minutes.append('04')
minutes.append('05')
minutes.append('06')
minutes.append('07')
minutes.append('08')
minutes.append('09')
# array of second candidates ranging from 0 - 59
seconds = []
for x in range(60):
    seconds.append(str(x))
seconds.append('00')
seconds.append('01')
seconds.append('02')
seconds.append('03')
seconds.append('04')
seconds.append('05')
seconds.append('06')
seconds.append('07')
seconds.append('08')
seconds.append('09')

# check that the end time comes after the start time
def check_times(start_hour_string, start_minute_string, start_second_string, end_hour_string, end_minute_string, end_second_string):
    if int(start_hour_string) > int(end_hour_string):
        print("Start hour bigger")
        return True
    if int(start_hour_string) == int(end_hour_string):
        print("Start hour equal")
        if int(start_minute_string) > int(end_minute_string):
            print("Start minute bigger")
            return True
        if int(start_minute_string) == int(end_minute_string):
            print("Start minute equal")
            if int(start_second_string) > int(end_second_string):
                print("Start second greater")
                return True
            if int(start_second_string) == int(end_second_string):
                print("Start second equal")
                return False
            if int(start_second_string) < int(end_second_string):
                print("start_second_smaller")
                return False
        if int(start_minute_string) < int(end_minute_string):
            print("start_minute_smaller")
            return False
    if int(start_hour_string) < int(end_hour_string):
        print("start_hour smaller")
        return False
    
# convert the combobox values into times
def convert_times():
    '''Takes in time inputs and generate datetime string'''

    # check if the table and tag input is valid if entered manually
    if n.get() not in table_names_string_replace_2:
        messagebox.showerror('Invalid Table', 'Error: Enter a valid table name from the database.')
    if n2.get() not in tag_names_string_replace_2:
        messagebox.showerror('Invalid Tag', 'Error: Enter a valid tag name from the database.')

    start_hour_string2 = start_hour_string.get()
    start_minute_string2 = start_minute_string.get()
    start_second_string2 = start_second_string.get()
    end_hour_string2 = end_hour_string.get()
    end_minute_string2 = end_minute_string.get()
    end_second_string2 = end_second_string.get()
    # check if the date time components are valid values
    if start_hour_string2 not in hours:
        messagebox.showerror('Invalid Tag', 'Error: Enter a valid start hour between 0 and 23.')
    if start_minute_string2 not in minutes:
        messagebox.showerror('Invalid Tag', 'Error: Enter a valid start minute between 0 and 59.')
    if start_second_string2 not in seconds:
        messagebox.showerror('Invalid Tag', 'Error: Enter a valid start second between 0 and 59.')
    if end_hour_string2 not in hours:
        messagebox.showerror('Invalid Tag', 'Error: Enter a valid end hour between 0 and 23.')
    if end_minute_string2 not in minutes:
        messagebox.showerror('Invalid Tag', 'Error: Enter a valid end minute between 0 and 59.')
    if end_second_string2 not in seconds:
        messagebox.showerror('Invalid Tag', 'Error: Enter a valid end second between 0 and 59.')

    # check if there are any of the boxes are left empty and warn the user
    if len(n.get()) == 0:
        messagebox.showerror('Empty Input', 'Error: Please enter a table name.')
    if len(n2.get()) == 0: 
        messagebox.showerror('Empty Input', 'Error: Please enter a tag name.')
    if len(start_hour_string2) == 0:
        messagebox.showerror('Empty Input', 'Error: Please enter a starting hour.')
    if len(start_minute_string2) == 0:
        messagebox.showerror('Empty Input', 'Error: Please enter a starting minute.')
    if len(start_second_string2) == 0:
        messagebox.showerror('Empty Input', 'Error: Please enter a starting second.')
    if len(end_hour_string2) == 0:
        messagebox.showerror('Empty Input', 'Error: Please enter an ending hour.')
    if len(end_minute_string2) == 0:
        messagebox.showerror('Empty Input', 'Error: Please enter an ending minute')
    if len(end_second_string2) == 0:
        messagebox.showerror('Empty Input', 'Error: Please enter an ending second.')
    boolean = check_times(start_hour_string2, start_minute_string2, start_second_string2, end_hour_string2, end_minute_string2, end_second_string2)
    if boolean:
        messagebox.showerror('Incorrect end date', 'Error: Please enter an end date that comes after the start date')
    
    # if all inputs are valid, connect to the database
    if (len(n.get()) != 0 and len(n2.get()) != 0 and len(start_hour_string.get()) != 0 and len(start_minute_string.get()) != 0 and len(start_second_string.get()) != 0 and len(end_hour_string.get()) != 0 and len(end_minute_string.get()) != 0 and len(end_second_string.get()) != 0 and not boolean):
        cursor = conn.cursor()
        date = str(n.get())
        date_cleaned = date[-10:]
        year_cleaned = date_cleaned[:4]
        month_cleaned = date_cleaned[5:-3]
        day_cleaned = date_cleaned[-2:]
        tag_name = str(n2.get())
        # clean and correct the values from the comboboxes
        start_hour = str(start_hour_string.get())
        if int(start_hour) < 10:
            start_hour = "0" + start_hour
        start_minute = str(start_minute_string.get())
        if int(start_minute) < 10:
            start_minute = "0" + start_minute
        start_second = str(start_second_string.get())
        if int(start_second) < 10:
            start_second = "0" + start_second
        end_hour = str(end_hour_string.get())
        if int(end_hour) < 10:
            end_hour = "0" + end_hour
        end_minute = str(end_minute_string.get())
        if int(end_minute) < 10:
            end_minute = "0" + end_minute
        end_second = str(end_second_string.get())
        if int(end_second) < 10:
            end_second = "0" + end_second

        # combien the datetime pieces into a datetime string
        start_datetime_string = year_cleaned + "-" + month_cleaned + "-" + day_cleaned + " " + start_hour + ":" + start_minute + ":" + start_second
        end_datetime_string = year_cleaned + "-" + month_cleaned + "-" + day_cleaned + " " + end_hour + ":" + end_minute + ":" + end_second

        # get the value interval between two dates
        command_timestamp = "SELECT TimeStamp FROM dbo." + date + " WHERE TimeStamp BETWEEN '" + start_datetime_string + "' AND '" + end_datetime_string + "'"
        cursor.execute(command_timestamp)
        timestamp_values_copy = timestamp_values
        for i in cursor:
            timestamp_values_copy.append(i[0])
        # get the value interval between two dates
        command_values = "SELECT " + tag_name + " FROM dbo." + date + " WHERE TimeStamp BETWEEN '" + start_datetime_string + "' AND '" + end_datetime_string + "'"
        cursor.execute(command_values)
        
        int_values_copy = int_values
        for i in cursor.fetchall():
            int_values_copy.append(i[0])
        # button that saves the specified values to a .CSV file
        csv_button = Button(master = window, command = lambda: write_to_csv(tag_name, date, timestamp_values_copy, int_values_copy), height = 2, width = 10, text = "Write to CSV")
        csv_button.place(x=712, y=550, anchor=CENTER)
        plot(timestamp_values, int_values)

def write_to_csv(tag_name, date, timestamp_values_copy, int_values_copy):
    # creating a csv title based on the tag name and time
    csv_title = tag_name + "_" + date
    with open(csv_title, "w+", newline="", encoding='UTF-8') as file:
        file.truncate()
        writer = csv.writer(file)
        for i in range(len(timestamp_values_copy)):
            tup = (timestamp_values_copy[i], int_values_copy[i])
            writer.writerow(tup)
        file.close()
def plot(timestamp_values, int_values):
    '''plot of the graph'''
    fig = Figure(figsize = (7.75, 4), dpi = 100)
    # clearing any previously plotted graphs
    CANVAS = FigureCanvasTkAgg(fig, master = window) 
    # adding the subplot
    plot1 = fig.add_subplot(111)
    # plotting the graph
    plot1.plot(timestamp_values, int_values)
    # creating the Tkinter canvas
     
    CANVAS.draw()
    # placing the canvas on the Tkinter window
    CANVAS.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(CANVAS, window) 
    toolbar.update()
    # placing the toolbar on the Tkinter window
    CANVAS.get_tk_widget().place(x=400, y=300, anchor=CENTER)

def callbackFunc(event):
    cursor = conn.cursor()
    date = str(n.get())
    # get the first timestamp value
    first_timestamp_command = "SELECT TOP 1 TimeStamp FROM dbo." + date + " ORDER BY TimeStamp ASC"
    cursor.execute(first_timestamp_command)
    for i in cursor:
        first_timestamp_value = i[0]
    # get the last timestamp value
    last_timestamp_command = "SELECT TOP 1 TimeStamp FROM dbo." + date + " ORDER BY TimeStamp DESC"
    cursor.execute(last_timestamp_command)
    for i in cursor:
        last_timestamp_value = i[0]
    timestamp_text = "Please enter a time interval between " + str(first_timestamp_value) + " and " + str(last_timestamp_value)
    END_SECOND_LABEL = Label(window, text=timestamp_text) .place(x=400, y=90, anchor=CENTER)
    '''obtain the column names for the selected table'''
    table_instance = event.widget.get()
    tag_names.clear()
    tag_names_string.clear()
    tag_names_string_replace.clear()
    tag_names_string_replace_2.clear()
    # get the tag names
    cursor.execute("SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('dbo.{}')".format(table_instance))
    for idx in cursor:
        tag_names.append(idx)
    for idx in tag_names:
        tag_names_string.append(str(idx))
    for idx in tag_names_string:
        tag_names_string_replace.append(idx.replace("', )", ""))
    for idx in tag_names_string_replace:
        tag_names_string_replace_2.append(idx.replace("('", ""))
    # remove the timestamp tag 
    tag_names_string_replace_2.pop(0)
    w2['values'] = tag_names_string_replace_2

def get_sql_data():
    '''get first and last timestamps, as well table names from the database'''
    cursor = conn.cursor()
    # get the tables in the database
    cursor.execute("SELECT name FROM sys.tables")
    for i in cursor:
        table_names.append(i)
    # get the number of data entries
    cursor.execute('SELECT COUNT(*) FROM dbo.Dta_2022_06_26')
    for i in cursor:
        NUMBER_OF_DATA_ENTRIES = i

def connect_and_close():
    '''connection to the database'''
    global conn
    if len(database.get()) == 0: 
        messagebox.showerror('Empty Input', 'Error: Please enter a database name.')
    if len(server.get()) == 0:
        messagebox.showerror('Empty Input', 'Error: Please enter a server name.')
    if len(database.get()) != 0 and len(server.get()) != 0:
        database_name = database.get()
        server_name = server.get()
        driver = "SQL Server"
        trusted_connection='yes'
        try:
            conn = pyodbc.connect(driver=driver, server=server_name, database=database_name, trusted_connection=trusted_connection, timeout=3)
        except:
            messagebox.showerror('Invalid Configuration', 'Error: Unable to connect to the database.')
            server.delete(0, END)
            database.delete(0, END)
        else:
            close_window()

# exit function
def close_window():
    window.destroy()
    #exit()

# initial configuration window
window = Tk()
# setting the configuration window sizing to 600x400 pixels
window.geometry("600x400")
window.title("Database Configuration Settings")
# label creation
Label(window, text="Enter the name of the server:", bg="black", fg="white", font="none 12 bold", width="25") .place(x=300, y=75, anchor=CENTER)
# create a text entry box
server = Entry(window, width=35, bg="white")
server.place(x=300, y=125, anchor=CENTER)
Label(window, text="Enter the name of the database:", bg="black", fg="white", font="none 12 bold", width="25") .place(x=300, y=175, anchor=CENTER)
# create a text entry box
database = Entry(window, width=35, bg="white")
database.place(x=300, y=225, anchor=CENTER)
# add a submit button
Button(window, text="SUBMIT", width=35, command=connect_and_close) .place(x=300, y=275, anchor=CENTER)
window.mainloop()
get_sql_data()
table_names_copy = table_names
for i in table_names_copy:
    table_names_string.append(str(i))
for i in table_names_string:
    table_names_string_replace.append(i.replace("', )", ""))
for i in table_names_string_replace:
    table_names_string_replace_2.append(i.replace("('", ""))
window = Tk()
window.geometry("800x600")
window.title("Database Visualization")
n = StringVar()
w = ttk.Combobox(window, textvariable = n)
w['values'] = table_names_string_replace_2
w.current()
w.bind("<<ComboboxSelected>>", callbackFunc)
w.place(x=200, y=15, anchor=CENTER)
n2 = StringVar()
w2 = ttk.Combobox(window, textvariable = n2)
w2['values'] = tag_names_string_replace_2
w2.current()
w2.place(x=550, y=15, anchor=CENTER)
# Text labels
table_label = Label(window, text="Select the table:") 
table_label.place(x=50, y=15, anchor=CENTER)
tag_label = Label(window, text="Select the PLC tag:") 
tag_label.place(x=400, y=15, anchor=CENTER)
start_time_label = Label(window, text="Start time:") 
start_time_label.place(x=50, y=50, anchor=CENTER)
end_time_label = Label(window, text="End time:") 
end_time_label.place(x=400, y=50, anchor=CENTER)
# Hour, minute, and second labels
START_HOUR_LABEL = Label(window, text="H") .place(x=100, y=50, anchor=CENTER)
START_MINUTE_LABEL = Label(window, text="M") .place(x=175, y=50, anchor=CENTER)
START_SECOND_LABEL = Label(window, text="S") .place(x=250, y=50, anchor=CENTER)
END_HOUR_LABEL = Label(window, text="H") .place(x=450, y=50, anchor=CENTER)
END_MINUTE_LABEL = Label(window, text="M") .place(x=525, y=50, anchor=CENTER)
END_SECOND_LABEL = Label(window, text="S") .place(x=600, y=50, anchor=CENTER)


# time combo boxes
start_hour_string = StringVar()
start_hour_combobox = ttk.Combobox(window, textvariable = start_hour_string, width=4)
start_hour_combobox['values'] = hours
start_hour_combobox.current()
start_hour_combobox.place(x=135, y=50, anchor=CENTER)
start_minute_string = StringVar()
start_minute_combobox = ttk.Combobox(window, textvariable = start_minute_string, width=4)
start_minute_combobox['values'] = minutes
start_minute_combobox.current()
start_minute_combobox.place(x=210, y=50, anchor=CENTER)
start_second_string = StringVar()
start_second_combobox = ttk.Combobox(window, textvariable = start_second_string, width=4)
start_second_combobox['values'] = seconds
start_second_combobox.current()
start_second_combobox.place(x=285, y=50, anchor=CENTER)
end_hour_string = StringVar()
end_hour_combobox = ttk.Combobox(window, textvariable = end_hour_string, width=4)
end_hour_combobox['values'] = hours
end_hour_combobox.current()
end_hour_combobox.place(x=485, y=50, anchor=CENTER)
end_minute_string = StringVar()
end_minute_combobox = ttk.Combobox(window, textvariable = end_minute_string, width=4)
end_minute_combobox['values'] = minutes
end_minute_combobox.current()
end_minute_combobox.place(x=560, y=50, anchor=CENTER)
end_second_string = StringVar()
end_second_combobox = ttk.Combobox(window, textvariable = end_second_string, width=4)
end_second_combobox['values'] = seconds
end_second_combobox.current()
end_second_combobox.place(x=635, y=50, anchor=CENTER)
# button that displays the plot
plot_button = Button(master = window, command = convert_times, height = 2, width = 10, text = "Plot Data")
plot_button.place(x=712, y=45, anchor=CENTER)
window.mainloop()