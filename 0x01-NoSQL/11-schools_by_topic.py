#!/usr/bin/env python3
""" The `11-schools_by_topic` module supplies a function `schools_by_topic` """
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    A function that returns the list of school having a specific topic

    Args:
    mongo_collection: mongo collection
    topic:           topic

    Return:
    List of schools with a specific topic
    """
    search_criteria = {"topics": topic}
    result = mongo_collection.find(search_criteria)
    return list(result)
