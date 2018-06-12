""" Server accepts connections from clients and checks whether they are new users or existing users
For new users it sends private_id (useful for next time logins) and public_id( to share with others to send message to user)
If they are old users then server checks private private_id and replaces the last time socket object with latest one for communication with client

For every message it receives it checks whether it should be routed to GROUP or to INDIVIDUAL and sends accordingly"""

import socket, threading

# groups is dictionary maintaining lists of groups and public keys of group members
groups = {'g1':['pub1','pub3','pub5'],'g2':['pub2','pub4','pub6']}

# connection_list is dictionary maintaining list of public id as keys and their corresponding socket object(lastest) as values 
connection_list = {}

""" ids is dictionary maintaining private id as keys and public id as values
This is userful for login and establishing connection to client """

ids = {'priv1':'pub1','priv2':'pub2','priv3':'pub3','priv4':'pub4','priv5':'pub5','priv6':'pub6'}   # List of ids of sign up users



# Function accepts clients and verifies whether they are new users or existing users

def accept_client():
    while True:
        #accept    
        cli_sock, cli_add = ser_sock.accept()
        response = cli_sock.recv(4096)
        response = response.strip()
        
        # Checking whether new user or not
        if response == 'Y':
            num = str(len(list(ids.keys()))+1)
            pri_id = 'priv' + num
            pub_id = 'pub' + num
            ids[pri_id] = pub_id
            connection_list[pub_id] = cli_sock
        
            data = "~".join([pri_id,pub_id])
            cli_sock.send(data)

        else:
            pri_id = cli_sock.recv(4096)

            for key in ids.keys():
                if key == pri_id:
                    pub_id = ids[pri_id]
                    connection_list[pub_id] = cli_sock  # Replacing old socket object with new one
                    break
                    

        thread_client = threading.Thread(target = handle_usr, args=(cli_sock,))
        thread_client.start()

def handle_usr(cli_sock):
    while True:
        try:
            data = cli_sock.recv(4096)
            if data:        # data format 'FROM ~ GROUP_ID ~ TO ~ MESSAGE'
                check = data.split("~")
                
                if check[1] == '':   # Message is not to group
                    send_to_user(connection_list[check[2]],data)
                    
                else:   # Message should be sent to all members of group
                    for member in groups[check[1]]:
                        send_to_user(connection_list[member],data)
                    
        except:
            continue

#  Sending messages to user_sock
def send_to_user(user_sock, msg):
    user_sock.send(msg)

if __name__ == "__main__":    

    # socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind
    HOST = 'localhost'
    PORT = 8080
    server_sock.bind((HOST, PORT))

    # listen    
    server_sock.listen(5)

    thread_accept = threading.Thread(target = accept_client)
    thread_accept.start()
