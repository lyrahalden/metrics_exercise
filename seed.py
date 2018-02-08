"""Utility file to seed energydrinks database from files in data folder"""

from sqlalchemy import func
from model import User

from model import connect_to_db, db
from server import app


def load_households():
    """Load users from u.user into database."""

    print "Households"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicates
    Household.query.delete()

    # Read trips_gdrive.csv file and insert data
    for row in open("data/trips_gdrive.csv"):
        row = row.rstrip()
        trip_id, date, retailer_name, brand_name, user_id, price, item_units = row.split(",")

        household = Household(user_id=user_id)


        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
