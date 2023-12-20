#!/usr/bin/env python3
""" The `10-update_topics` module supplies a function `update_topics` """
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    A function that changes all topics of a school document based on the name

    Args:
    mongo_collection: mongo collection
    name:             school name
    topics:           topic

    Return:
    nothing
    """
    update_criteria = {"name": name}
    update_operation = {"$set": {"topics": topics}}
    mongo_collection.update_many(update_criteria, update_operation)
