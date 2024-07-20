class Socket:
    def __init__(self, ip_adress, socketnr):
        import socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (ip_adress, socketnr)
        self.server_socket.bind(self.server_address)
        print("socket class setup complete")
        
    def dataToJSON(self, decodedData):
        #Splits the string based on commas
        tempStrings = decodedData.split(',')
        # Convert each string to float and then to int
        temperatures = [int(float(temp)) for temp in tempStrings]
        # Finds the difference between the two numbers
        diff = abs(temperatures[0]-temperatures[1])
        # Appends the temperature into the list temperatures
        temperatures.append(diff)
        # converts the list to JSON dic
        tempDict = {
        "termo1": temperatures[0],
        "termo2": temperatures[1],
        "diff": temperatures[2]
        }
        print(f"The tempDict is:{tempDict}")
        return tempDict
    
    def sendToMySQL(self, JSON):
        import mysql.connector
        # Connect to MySQL server
        dbConnection = mysql.connector.connect(
        host="localhost",
        user="Andreas",
        password="minityhei98"
        )
        # Create a cursor object to interact with the database
        cursor = dbConnection.cursor()
        alterUserQuery = """
        ALTER USER 'Andreas'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'minityhei98';
        """
        cursor.execute(alterUserQuery)
        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS personalDatabase")
        cursor.execute("USE personalDatabase")
        # Create the table if it doesn't exist
        createTableQuery = """
        CREATE TABLE IF NOT EXISTS recordedData (
        IDnr INT AUTO_INCREMENT PRIMARY KEY,
        termo1 FLOAT,
        termo2 FLOAT,
        diff FLOAT,
        datetime DATETIME
        )
        """
        cursor.execute(createTableQuery)

        # Insert data into the table
        insertDataQuery = """
        INSERT INTO recordedData (termo1, termo2, diff, datetime)
        VALUES (%s, %s, %s, NOW())
        """
        # Replace these values with your actual data
        dataToInsert = (JSON['termo1'], JSON['termo2'], JSON['diff'])

        cursor.execute(insertDataQuery, dataToInsert)
        # Commit the changes and close the connection
        dbConnection.commit()
        cursor.close()
        dbConnection.close()

        
    def recieveNPrint(self):
        print("recieveNPrint called")
        while True:
            data, client = self.server_socket.recvfrom(1024)
            print("socket bind complete")
            decodedData = data.decode()
            print(f"Recieved message from {client} {decodedData}")
            
            #Calls the funktion DataToJSON. That turns the decodedData into a JSON dictonary. So it is ready for MySQL
            JSON = udpSock.dataToJSON(decodedData)
            
            #Sends the JSON to a MySQL database
            udpSock.sendToMySQL(JSON)
                
            
if __name__ == "__main__":
    
    udpSock = Socket("0.0.0.0", 12345)
    udpSock.recieveNPrint()

