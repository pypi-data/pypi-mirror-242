import json

import time

import paramiko

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from datetime import datetime, timezone

speedgoat_lookup_restart = {
    'Oxford': 30001,
    'Sheffield': 30002,
    'Birmingham': 30003,
    'Newcastle': 30004,
    'Manchester': 30005       
}

# Function to replace the previous SoC value with the new SoC value
def replaceSoC(NewSoC,locationrestart):
    
    NewSoCwrite = str(NewSoC)
    
    # Find the port we need to connect to
    PORTcon = speedgoat_lookup_restart[locationrestart]
    
    # Go into the Speedgoat and find the name of the installed applications
    # Define client as a paramiko ssh client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Add the details required, the host, username and password are the same
    # The port varies depending on which Speedgoat we are connecting to
    client.connect("127.0.0.1", username = "slrt", password = "slrt", port = PORTcon)
    
    # The command is to list the applications installed on the Speedgoat
    command = "cd /home/slrt/applications/ && ls"
    
    # Execute the command on the Speedgoat
    stdin, out, err = client.exec_command(command)
    
    # Read the results and put them in the variable AppName, 
    # using a for loop ensures only the final appname is used
    for items in out:
        AppName = items
        
    # Change to the directory of the saved parameters file and read the file
    command = "cd /home/slrt/applications/" + AppName.strip() + "/paramSet/ && cat autoSaveOnStop.json"
    stdin, out, err = client.exec_command(command)
    # Predefine a variable for the parameters file
    paramfile = ""
    # Read in the parameters file
    for items in out:
        paramfile = paramfile + items
    
    # Convert the read in file to json format
    paramfilejson = json.loads(paramfile)
        
    # Find the previous SoC and replace with the new SoC
    for member in paramfilejson['parameters']:
        if member['Name'] == 'BBBSoC':
            member['Value'] = NewSoCwrite
    
    # Define the directory where the new file we be written to
    file2write = "/home/slrt/applications/" + AppName.strip() + "/paramSet/autoSaveOnStop.json"
    
    # Define the data to write
    data2write = json.dumps(paramfilejson)
            
    # Open a file transfer item
    sftp = client.open_sftp()
    
    # Open the file to write to and write the SoC
    f = sftp.open(file2write, 'w')
    f.write(data2write)
    f.close()
    client.close()

# Function to check when the most recent data entered in the data is
def Check4Restart(location):
    
    while True:
    
        bucket = "RealTimeStorageSimulators"
        org = "UniversityOfOxford"
        token = "Nq-5r5jJ2s1jf0ePEJ2B7cNCqWk4J1nzmnULvh4k247mHxXrdEon2tMczUXfqp7WnxXe80ZfSzGlmDjii1hqzg=="
        # Store the URL of your InfluxDB instance
        url="http://localhost:8086"
        
        client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org
        )
        
        # Query script
        bind_params = {"_location": location}
        
        query_api = client.query_api()
        
        query = 'from(bucket:"RealTimeStorageSimulators")\
        |> range(start: -365d)\
        |> filter(fn:(r) => r.location == _location)\
        |> filter(fn:(r) => r._field == "BESSSoC")\
        |> last()'
        result = query_api.query(org=org, query=query, params=bind_params)
        
        
        results = []
        for table in result:
            for record in table.records:
                timeentered = record.get_time()
                SoC = record.get_value()
    
        timesince = datetime.now(timezone.utc) - timeentered
        timesincesecs = timesince.total_seconds()
        
        # Check if the number of seconds is greater than 60
        if timesincesecs > 60:
            
            print("Replaced")
            print(SoC)
            print(timesincesecs)
            replaceSoC(SoC,location)
            
            # Find the port we need to connect to
            PORTcon = speedgoat_lookup_restart[location]
                
            # Go into the Speedgoat and find the name of the installed applications
            # Define client as a paramiko ssh client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
            # Add the details required, the host, username and password are the same
            # The port varies depending on which Speedgoat we are connecting to
            client.connect("127.0.0.1", username = "slrt", password = "slrt", port = PORTcon)
                
            # The command is to list the applications installed on the Speedgoat
            command = "shutdown -S reboot"
                
            # Execute the command on the Speedgoat
            stdin, out, err = client.exec_command(command)
            
            time.sleep(100)
            
        time.sleep(10)