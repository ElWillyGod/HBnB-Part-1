#!/usr/bin/python3

'''
    Aplication runner.
'''

from api import app

if __name__ == '__main__':
    app.run(host='0.0.0.0')
