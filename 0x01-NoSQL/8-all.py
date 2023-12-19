#!/usr/bin/env python3
""" The `8-all` module supplies a function `list_all` """
import pymongo


def list_all(mongo_collection):
    """
    A function that lists all documents in a collection

    Args:
    mongo_collection: mongo collection

    Return:
    Empty list if no collection
    """
    if mongo_collection is None:
        return []
    return [doc for doc in mongo_collection.find()]