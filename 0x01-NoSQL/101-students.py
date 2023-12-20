#!/usr/bin/env python3
""" The `101-students` module supplies a function `top_students` """


def top_students(mongo_collection):
    """
    top_students: Function that returns all students sorted by average score

    Args:
    mongo_collection: mongo collection

    Return:
    Students sorted by average
    """
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "averageScore": {"$avg": "$topics.score"}
            }},
        {"$sort": {"averageScore": -1}}
    ]
    result = mongo_collection.aggregate(pipeline)
    return result
