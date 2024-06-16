#!/usr/bin/python3

'''
    Run all tests.
'''

import test_amenities
import test_countries
import test_users
import test_cities
import test_places
import test_reviews

def run():
    test_amenities.run()
    test_countries.run()
    test_users.run()
    test_cities.run()
    test_places.run()
    test_reviews.run()

if __name__ == "__main__":
    run()
