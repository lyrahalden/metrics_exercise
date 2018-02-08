"""Models and database functions for Metrics project."""

from flask_sqlalchemy import SQLAlchemy


# This is the connection to the PostgreSQL database thru Flask-SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

# class Household(db.Model):
#     """One household, represented by a primary buyer, or user"""

#     __tablename__ = "households"

#     household_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     # user_id is the data directly from the csv file
#     user_id = db.Column(db.Integer)

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Household household_id=%s" % (self.household_id)


# class Brand(db.Model):
#     """A brand"""

#     __tablename__ = "brands"

#     brand_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     brand_name = db.Column(db.String(80))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Brand brand_id=%s" % (self.brand_id)


# class Retailer(db.Model):

#     __tablename__ = "retailers"

#     retailer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     retailer_name = db.Column(db.String(80))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Retailer retailer_id=%s" % (self.retailer_id)


# class Purchase(db.Model):
#     """A purchase event"""

#     __tablename__ = "purchases"

#     purchase_id = db.Column(db.Integer, primary_key=True)
#     household_id = db.Column(db.Integer, db.ForeignKey('households.household_id'), nullable=False)
#     brand_id = db.Column(db.Integer, db.ForeignKey('brands.brand_id'), nullable=False)
#     retailer_id = db.Column(db.Integer, db.ForeignKey('retailers.retailer_id'), nullable=False)
#     price = db.Column(db.Integer)
#     date = db.Column(db.DateTime, nullable=True)

#     household = db.relationship('Household', backref='purchases')
#     brand = db.relationship('Brand', backref='purchases')
#     retailer = db.relationship('Retailer', backref='purchases')

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Purchase purchase_id=%s" % (self.purchase_id)


class Purchase(db.Model):
    """A purchase event"""

    __tablename__ = "purchases"

    purchase_id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(db.Integer, nullable=False)
    brand_name = db.Column(db.String(80), nullable=False)
    retailer_name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer)
    units_sold = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Purchase purchase_id=%s" % (self.purchase_id)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to the Flask app."""

    # Configure to use the PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///energydrinks'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

# # You are being asked to create an application that includes the following functions:
# # 1) A function that given a brand, returns the strongest retailer affinity relative
#     to other brands. (Note: this should compare the focus brand to all other brands,
#     and every brand should not return 'walmart')
# # def retailer_affinity(focus_brand):
# # 2) A function that returns the number of households (a household could have many
# transactions in the provided dataset), allowing for a dynamic optional set of inputs:
# # def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
# 3) Identify brand with top buying rate ($ spent / HH)
# # def top_buying_brand():


def retailer_affinity(focus_brand):
    """Given a brand, returns the strongest retailer affinity relative to other brands"""

    focus_brand_obj = Brand.query.filter_by(brand_name=focus_brand).first()

    purchases_of_focus_brand = db.session.query(Purchase, Brand).join(Purchase).filter(Brand.name=focus_brand).all()

    for purchase in purchases_of_focus_brand:

    # retailer_list = Retailer.query.all()

    # affinity_score = 0

    # for retailer in retailer_list:
    #     purchases = Purchase.query.filter_by(brand_name=)





def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """Given inputs, returns the number of households that matches the inputs"""


def top_buying_brand():
    """Returns the brand with the top buying rate ($ spent per household)"""


if __name__ == "__main__":
    # can work with the db interactively
    from server import app
    connect_to_db(app)
    print "Connected to DB."

    #delete to create new tables
    db.delete_all()
    # in case tables have not been created yet
    db.create_all()
