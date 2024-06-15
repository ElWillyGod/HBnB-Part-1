#/usr/bin/python3

'''
    Aplication runner.
    WIP
'''

import logic.logicfacade
#import api

test = logic.logicfacade.LogicFacade
test.createObjectByJson("user",
                        {"first_name": "Matias",
                         "last_name": "Davezac",
                         "email": "matiasdavezac@gmail.com"})