from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    date = db.Column(
        db.String(20),
        nullable=False
    )

    time = db.Column(
        db.String(20),
        nullable=False
    )

    total_seats = db.Column(
        db.Integer,
        nullable=False,
        default=60
    )

    available_seats = db.Column(
        db.Integer,
        nullable=False
    )

    bookings = db.relationship(
        "Booking",
        backref="event",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    number_of_seats = db.Column(
        db.Integer,
        nullable=False
    )

    selected_seats = db.Column(
        db.String(500),
        nullable=False
    )

    booking_date = db.Column(
        db.DateTime,
        default=datetime.now
    )

    user_id = db.Column(
        db.Integer,
        nullable=True
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        nullable=False
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Confirmed"
    )