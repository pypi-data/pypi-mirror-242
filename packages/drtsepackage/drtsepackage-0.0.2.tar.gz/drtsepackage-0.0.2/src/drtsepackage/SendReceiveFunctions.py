# To use these functions, put the following at the top of the program
# import SendReceiveFunctions

# Import socket which is needed to send the data via TCP
import socket
# Import struct which is needed to pack the data to the correct format
import struct

# Import json which is needed to lookup in tables   
import json

import time

from timeit import default_timer as timer

# Imports required for the multiprocessing
from multiprocessing import Process
from multiprocessing import Queue

# Open the json file containing the data from the Speedgoat and save the data as a variable
f = open('../DataFromSimulink.json')
# Save the data from the file as the variable datafromspeedgoat  
datafromspeedgoat = json.load(f)
# Close the json file
f.close()

# Define the server's IP address, which is the local machine (127.0.0.1), it is the local machine as the connection is made through an SSH tunnel 
HOST = "127.0.0.1"  # The server's hostname or IP address

# Table to lookup the port number for the requested Speedgoat
# For example, if the powers should be received from the Oxford Speedgoat, it is received from port 50114
speedgoat_lookup_ReceiveDataCont = {
    'Oxford': 42001,
    'Sheffield': 42002,
    'Birmingham': 42003,
    'Newcastle': 42004,
    'Manchester': 42005       
}

# Table to lookup the port number for the requested Speedgoat
# For example, if the powers should be received from the Oxford Speedgoat, it is received from port 50114
speedgoat_lookup_SendPowers = {
    'Oxford': 51001,
    'Sheffield': 51002,
    'Birmingham': 51003,
    'Newcastle': 51004,
    'Manchester': 51005       
}

# Table to lookup the port number for the requested Speedgoat
# For example, if the powers should be received from the Oxford Speedgoat, it is received from port 50114
speedgoat_lookup_SendDataRequest = {
    'Oxford': 52001,
    'Sheffield': 52002,
    'Birmingham': 52003,
    'Newcastle': 52004,
    'Manchester': 52005       
}

###############################################################################################################
###############################################################################################################
###############################################################################################################
# Function to send Real and Reactive Power to the Speedgoat
# To use the function in a program the syntax is SendReceiveFunctions.SendPowers(location,realpower,reactivepower,communication)

# The inputs are:
# location is string, it must be the same as in the Speedgoat_lookup table below, i.e. 'Oxford'
# realpower is the real power requested from the speedgoat and is a number
# reactive power is the reactive power requested from the speedgoat and is a number
# communication is the time in seconds until the next communcation will be sent

# Define the function called SendPowers
def SendPowers(locationsend,realpower,reactivepower,communication):
    
    # The correct port to send the data is found from the lookup table
    PORTsend = speedgoat_lookup_SendPowers[locationsend]  # The port used by the server
    
    # The powers to send are packed using the pack function
    # Regarding "<3d", < means little-endian, 3 means 3 data values are being packed, and d means the data is type double    
    powerstosend = struct.pack("<3d",realpower,reactivepower,communication)
    
    # Create a socket object 's', AF_INET means that an IPv4 address will be 
    # supplied, SOCK_STREAM is almost always used by TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        # Connect to the host and port
        s.connect((HOST, PORTsend))
        
        # Send the data to the Speedgoat
        s.sendall(powerstosend)
        
        print(struct.unpack("<3d",powerstosend))

###############################################################################################################
###############################################################################################################
###############################################################################################################
# Functions to receive data from the Speedgoat when requested
# To receive data from the Speedgoat, the following syntax is used SendReceiveFunctions.ReceiveData(location, queue)

# The input is:
# location is a string containing the name of the Speedgoat that data is requested from, options can be seen in the table below 'speedgoat_lookup'
# The queue variable must also be passed

# The output of the function is a vector of varying length, depending on how many data values are available from that Speedgoat model
# The first four values of the output vector will always be 1) Grid Frequency, 2) Grid RMS Votlage, 3) Real Power, 4) Reactive Power

###############################################################################################################
# Multiple functions are required for receiving data, the first ReceiveDataCont is run continuously after startup

# Define the function called ReceiveData
def ReceiveDataCont(locationcont, queuecont):
          
    # User enter IP and port to listen to, with the SSH tunneling, host will 
    PORTreccont = speedgoat_lookup_ReceiveDataCont[locationcont]  # Port to listen on (non-privileged ports are > 1023)

    # Loop to run program forever
    while True:
    
        # Create a socket object 's', AF_INET means that an IPv4 address will be 
        # supplied, SOCK_STREAM is almost always used by TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # Attach the given host and port to the socket object
            s.bind((HOST, PORTreccont))
        
            # Place the socket in listening state to listen for incoming data
            s.listen()
        
            # Read variables conn and addr when a connection is made
            conn, addr = s.accept()
        
            # When the connection is made
            with conn:
                
                # While the connection is made, run this loop forever
                while True:
                    
                    # Receive the data
                    data = conn.recv(1024)
                
                    # If there is no data, break the inner while loop
                    if not data:
                        break
                
                    # Create a variable which defines the format for decoding the 
                    # data. The common values are: < for little-endian, d for
                    # double. The variable is a number signifying the number of 
                    # data values being transmitted
                    fmt = "<%dd" % (len(data) // 8)
                
                    # Unpack the data using this format and save a vraiable
                    SpeedgoatDataRaw = list(struct.unpack(fmt,data))
            
                    # Create a dictionary of the data available
                    SpeedgoatData = {}
                    for key in datafromspeedgoat[locationcont]:
                        for value in SpeedgoatDataRaw:
                            SpeedgoatData[key] = value
                            SpeedgoatDataRaw.remove(value)
                            break
                    
                    # Initially clear the queue in case there is any old data in the queue     
                    while not queuecont.empty():                    
                        queuecont.get()
                    # Put the data in the queue to be sent back to the main program
                    queuecont.put(SpeedgoatData)


###############################################################################################################
# The second function for receiving data is called SendDataRequest
# This function sends a request to the Speedgoat to send data
# It must be run as a multiprocess function as it includes a while True loop
# This means, once the data is received, this function should be terminated
def SendDataRequest(locationsendreq):
    
    while True:
        # The correct port to send the data is found from the lookup table
        PORTsendreq = speedgoat_lookup_SendDataRequest[locationsendreq]  # The port used by the server
        
        # The powers to send are packed using the pack function
        # Regarding "<3d", < means little-endian, 3 means 3 data values are being packed, and d means the data is type double    
        reqtosend = struct.pack("<1d",1.0)
        
        # Create a socket object 's', AF_INET means that an IPv4 address will be 
        # supplied, SOCK_STREAM is almost always used by TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # Connect to the host and port
            s.connect((HOST, PORTsendreq))
            
            # Send the data to the Speedgoat
            s.sendall(reqtosend)
        
        time.sleep(0.001)    

###############################################################################################################
# The third function is a function that should be run on startup of all models
# This function established the receiving data connection and includes the location of experiment
def CommunicationInitialisation(LocationsExperiment):

    # Predefine the queue and ReceiveProcess arrays
    queue = {}
    ReceiveProcess = {}
    SendProcessDataReqStartup = {}
    
    # Do the following for each of the locations
    for loc in LocationsExperiment:
        # Create the queues for each location
        queue[loc] = Queue()
               
        # Create the multiprocessing function for each location to start the receiving data function to run continuously
        ReceiveProcess[loc] = Process(target=ReceiveDataCont, args=(loc,queue[loc],))
        # Start the function receiving data
        ReceiveProcess[loc].start()
        
        # At startup the Speedgoat must be requested to send some data to establish the TCP connection
        # This is just run for 1 second for each location to establish the connection
        SendProcessDataReqStartup = Process(target=SendDataRequest, args=(loc,))
        # Start the function requesting data
        SendProcessDataReqStartup.start()
        # Delay for 1 second
        time.sleep(1.0)
        # Stop the process after 1 second
        SendProcessDataReqStartup.terminate()
        
        # In addition, for each location a send power command must be sent
        # SendPowers(loc,0.0,0.0,1.0)
    
    # Print that the setup process has finished    
    print('Setup Finished')
    
    # Return the queue to the main function
    return queue

###############################################################################################################
# The fourth function is the function that is actually run in the models and returns the data        
def ReceiveData(locationrec, queuerec):
    
    # Initially clear the queue     
    while not queuerec[locationrec].empty():                    
        queuerec[locationrec].get()
    
    # Predefine the receive request process
    ReceiveReqProcess = {}
    # Create the multiprocessing function for receiving data
    ReceiveReqProcess[locationrec] = Process(target=SendDataRequest, args=(locationrec,))
    # Start the function requesting receiving data
    ReceiveReqProcess[locationrec].start()

    # Once the receive data function puts new data in the queue, get this data
    DataNew = queuerec[locationrec].get()
    
    # Stop the sending requests for data process
    ReceiveReqProcess[locationrec].terminate()
    
    # Return the data received
    return DataNew