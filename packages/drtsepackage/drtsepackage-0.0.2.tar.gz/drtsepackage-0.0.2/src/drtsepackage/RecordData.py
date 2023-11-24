# To use these functions, put the following at the top of the program
# import RecordDataFunction

###############################################################################################################
# Function to receive data from the Speedgoat and post the data to the database
# To use the function in a program the syntax is RecordDataFunction.DatabaseWrite(location, experiment)

# The input is:
# location is a string containing the name of the Speedgoat that data is to be posted from, options can be seen in the table below 'speedgoat_lookup'
# experiment is the experiment that is being conducted, this tag will be added to the database

# Define the function called ReceiveData
def DatabaseWrite(location, experiment):

    # Define the database bucket to write to 
    bucket="RealTimeStorageSimulators"
    
    # Required to connect to the Speedgoat using TCP
    import socket
    import struct
    
    # Various imports required to write data to the InfluxDB database
    import influxdb_client, os, time
    from influxdb_client import InfluxDBClient, Point, WritePrecision
    from influxdb_client.client.write_api import SYNCHRONOUS
    
    # Token for University of Oxford
    token = "Nq-5r5jJ2s1jf0ePEJ2B7cNCqWk4J1nzmnULvh4k247mHxXrdEon2tMczUXfqp7WnxXe80ZfSzGlmDjii1hqzg=="
    org = "UniversityOfOxford"
    url = "http://localhost:8086"
    
    # Defining Influxdb writing procedure
    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    write_api = write_client.write_api(write_options=SYNCHRONOUS)
 
    # Import json which is needed to read in the data table regarding variables that should be expected
    import json
    
    # Open and load the json file containing the data tables
    f = open('../DataFromSimulink.json')
    datafromspeedgoat = json.load(f)
    f.close()
    datafromspeedgoatLocation = datafromspeedgoat[location]
    
    # Table to lookup the port number for the requested Speedgoat
    # For example, if the powers should be received from the Oxford Speedgoat, it is received from port 50114
    speedgoat_lookup_Record = {
        'Oxford': 41001,
        'Sheffield': 41002,
        'Birmingham': 41003,
        'Newcastle': 41004,
        'Manchester': 41005       
    }

    # User enter IP and port to listen to, with the SSH tunneling, host will 
    # always be 127.0.0.1. Port is chosen for each Speedgoat
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = speedgoat_lookup_Record[location]  # Port to listen on (non-privileged ports are > 1023)

    # Loop to run program forever
    while True:
    
        # Create a socket object 's', AF_INET means that an IPv4 address will be 
        #supplied, SOCK_STREAM is almost always used by TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # Attach the given host and port to the socket object
            s.bind((HOST, PORT))
        
            # Place the socket in listening state to listen for incoming data
            s.listen()
        
            # Read variables conn and addr when a connection is made
            conn, addr = s.accept()
        
            # When the connection is made
            with conn:
            
                # Print the address which it is connected from
                print(f"Connected by {addr}")
            
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
                    Values2Post = struct.unpack(fmt,data)
                    
                    # Create a dictionary containing all the data to post to the database
                    # Predefine the fieldsvec which contains the different variables
#                    fieldsvec = {}                   
#                    for i in range(len(datafromspeedgoatLocation)):
#                        fieldsvec[datafromspeedgoatLocation[i]] = Values2Post[i]
                        
                    for j in range(20):
                        point = {}
                        fieldsvec = {}
                        for i in range(len(datafromspeedgoatLocation)-1):
                            fieldsvec[datafromspeedgoatLocation[i]] = Values2Post[i+j*len(datafromspeedgoatLocation)]
                            
                        timerec = int(Values2Post[len(datafromspeedgoatLocation)-1+j*len(datafromspeedgoatLocation)])
                    
                        # Create the point vector to write to the database    
                        point = [
                        	  {
                        	      "measurement": experiment, 
                        	      "tags": 
                        	          {
                        	              "location": location
                        	          },
                        	      "fields": fieldsvec,
                                "time": timerec
                       	    }
                        ]
                        
                        # Post the values to the database
                        write_api.write(bucket=bucket, org=org, record=point)