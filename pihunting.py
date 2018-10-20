#!/usr/bin/env python3
#Searching the net for unsecure raspberrys with default ssh credentials
#RaspiHunting
#Hunting is just the beginning...

import shodan
import paramiko
import os
import socket
import os

def terajo():
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


def main():

    ShodanKeyString = open('shodankey').readline().rstrip('\n')
    ShodanApi = shodan.Shodan(ShodanKeyString)
    terajo()
    try:
        results = ShodanApi.search('raspbian')
        print('Results: %s' % results['total'])
        for i in results['matches']:
            print('IP: %s' % i['ip_str'])
    except shodan.APIError as e:
        print('Ups... Something has gone wrong: %s' % e)

if __name__== "__main__":
    main()
