import socket, threading

""" Function to send messages to particular person or to particular group(by group id) and data will be in the format (string)FROM ~ GROUP_ID ~ TO ~ MESSAGE """

pub_id = ''
def send():
    while True:
        
        response = input("If you are a new user enter 'Y' else enter 'N' ")

        if response == 'N':
            pr_uid = input("Enter the private ID provided ")
            server.send(pr_uid)
            break
        else if response == 'Y':
            server.send(response)
            ids = server.recv(4096)
            ids = ids.split("~")    # Returns a list ['private_id', 'public_id']
            priv_id = ids[0]
            global pub_id
            pub_id = ids[1]
            print("Remember this private unique id {0} for further login \nShare this public id {} with people to message you".format(priv_id,pub_id))
            break
        else:
            print("Invalid input")


    while True:

        # Public id starts with 'p' and group id starts with 'g'
        to = input("Enter the id of recipient/group id (you must be a member of the group)")
        to = to.strip()
        print("Enter 'Q' to close the chat with {0}".format(to))

        tobe_added = ''
        
        if to[0] == 'g':    # Message is to group
            tobe_added = "~".join([pub_id,to,''])     # data format 'FROM ~ GROUP_ID ~ TO ~ MESSAGE'
        else:               # Means meassage is to person
            tobe_added = "~".join([pub_id,'',to])

        while True:
            
            msg = input('\nMe > ')
            if msg == 'Q':
                break
            data = "~".join([tobe_added,msg])

            server.send(data)


""" For receiving messages from other people. Received 'data' contains information about SENDER, GROUP_DETAILS, RECEIVER and MESSAGE """

def receive():
    while True:
        
        data = server.recv(4096)
        data = data.strip()
        data = data.split("~")
        
        """ Now data is a list of strings as follows ['FROM','GROUP_ID','TO','MESSAGE']
        No two groups can have same GROUP_ID """

        if data[1] == '':   # Checking if message is not to group
            print{"FROM: {0}: {1}".format(data[0],data[3]))

        else:   # message should be displayed in particular GROUP 
            print{"TO GROUP {0}: {1}".format(data[1],data[3]))


if __name__ == "__main__":   
    # TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    HOST = 'localhost'
    PORT = 8080
    #Connecting to server
    server.connect((HOST, PORT))     
    print('Connected to remote host...')
    
    thread_send = threading.Thread(target = send)
    thread_send.start()

    thread_receive = threading.Thread(target = receive)
    thread_receive.start()
