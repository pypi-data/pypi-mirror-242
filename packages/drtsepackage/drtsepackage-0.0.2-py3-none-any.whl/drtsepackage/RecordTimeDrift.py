# Define the function called DatabaseWriteTimings
def DatabaseWriteTimings(location):

    # Define the database bucket to write to 
    bucket="RealTimeStorageSimulators"
    
    # Required to connect to the Speedgoat using TCP
    import socket
    import struct
    import time
    
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
    
    # Table to lookup the port number for the requested Speedgoat
    # For example, if the powers should be received from the Oxford Speedgoat, it is received from port 50114
    speedgoat_lookup_Record = {
        'Oxford': 32001,
        'Sheffield': 32002,
        'Birmingham': 32003,
        'Newcastle': 32004,
        'Manchester': 32005       
    }
    
    # User entered IP and port to listen to, with the SSH tunneling, host will 
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
                    conn.sendall(data)
                    
                    offset = float(data.decode())          
                
                    # Create the point vector to write to the database    
                    point = [
                        {
                 	          "measurement": "TimingDrift", 
                    	      "tags": 
                	              {
                    	              "location": location
                    	          },
                    	      "fields":
                                {
                    	              "offset": offset
                    	          }
                   	    }
                    ]
                        
                    # Post the values to the database
                    write_api.write(bucket=bucket, org=org, record=point)
                    
                    conn.close()
                    
                    time.sleep(200)
                    
                    break