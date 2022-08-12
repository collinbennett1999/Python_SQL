# Python_SQL
Visualization of PLC Tag Data in Python

Introduction

This SQL Data Visualization tool is used to visualize data collected from the Beckhoff PLC into a SQL Server database. It can be run as an executable or a python script. Not a production application and should only be used to visualize and retrieve data. It is meant to be run on the computer collecting the PLC data. 

How to use:
	
Start the program. This can be done by either:
 running the executable
executing the Python script 
Running the executable is easier, but if you would like to make changes to the program without having to regenerate an executable, executing the script is more efficient. 

The connection window will popup. It looks like this:
![alt text](https://github.com/collinbennett1999/Python_SQL/blob/main/image.jpg)

The database this program uses does not have username/password authentication, instead opting to use a trusted connection. Windows Authentication is used, which requires a server and database name. 

Enter the server name. This can be found in MS SQL Server Management Studio, and will follow the naming pattern, “PC_NAME\SQLEXPRESS”. This is the PC name followed by SQLEXPRESS. The database name is the name of the target database you are connecting to. For example, this could be “Beckhoff_PLC”. Be aware that these are case sensitive and if any credentials are entered incorrectly, the connection will fail. 




A successful connection will lead to the visualization window.
![alt text](https://github.com/collinbennett1999/Python_SQL/blob/main/image2.jpg)



You will begin by selecting the desired table. The original data logging software would create a table for each 24 four hour cycle of data logging, naming the table after the respective day. This GUI allows you to select from the tables (days) in the database and this will generate the available PLC tags to choose from. These tags can be boolean, integer, unsigned integer, and real data types. Once the desired tag is selected, a time interval can be selected. The start and end times of the desired information are entered, and once plotted, will be displayed on the graph. The graph can be interacted with, and an image of the plot can be saved to the computer. To save the desired information to a .CSV, press the “Write to .CSV” button in the bottom right corner. This saves the datetime timestamp and respective PLC tag values along the desired interval to the .CSV file. This file is named using the date and PLC tag as the file name. 

Once all the desired information has been obtained, you can safely exit the program. The connection is closed and the .CSV remains. 
