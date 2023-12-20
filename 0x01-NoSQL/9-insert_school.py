#!/usr/bin/env python3
""" The `9-insert_school` module supplies a function `insert_school` """
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    A function that that inserts a new document in a collection based
    on kwargs

    Args:
    mongo_collection: mongo collection

    Return:
    _id
    """
    return mongo_collection.insert_many(kwargs)
