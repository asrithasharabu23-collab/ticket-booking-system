from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from models import db, Event, Booking

from datetime import datetime


app = Flask(__name__)


# =========================================================
# FLASK CONFIGURATION
# =========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///ticket_booking.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "ticket-booking-secret-key"


db.init_app(app)


# =========================================================
# CREATE DATABASE AND SAMPLE MOVIES
# =========================================================

with app.app_context():

    db.create_all()

    if Event.query.count() == 0:

        events = [

            Event(
                name="Avengers",
                location="Hyderabad",
                price=250,
                date="25-09-2026",
                time="7:00 PM",
                total_seats=60,
                available_seats=60
            ),

            Event(
                name="Spider-Man",
                location="Vijayawada",
                price=200,
                date="26-09-2026",
                time="6:30 PM",
                total_seats=60,
                available_seats=60
            ),

            Event(
                name="KGF Chapter 3",
                location="Guntur",
                price=220,
                date="27-09-2026",
                time="8:00 PM",
                total_seats=60,
                available_seats=60
            )

        ]

        db.session.add_all(events)

        db.session.commit()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():

    events = Event.query.all()

    return render_template(
        "index.html",
        events=events
    )


# =========================================================
# EVENT / MOVIE DETAILS
# =========================================================

@app.route("/event/<int:event_id>")
def event_details(event_id):

    event = Event.query.get_or_404(event_id)

    confirmed_bookings = Booking.query.filter_by(
        event_id=event.id,
        status="Confirmed"
    ).all()

    booked_seats = []

    for booking in confirmed_bookings:

        if booking.selected_seats:

            seats = booking.selected_seats.split(",")

            booked_seats.extend(seats)

    return render_template(
        "event.html",
        event=event,
        booked_seats=booked_seats
    )


# =========================================================
# BOOK TICKET
# =========================================================

@app.route(
    "/book/<int:event_id>",
    methods=["POST"]
)
def book_ticket(event_id):

    event = Event.query.get_or_404(event_id)


    # -----------------------------------------------------
    # NUMBER OF SEATS
    # -----------------------------------------------------

    try:

        number_of_seats = int(
            request.form.get(
                "number_of_seats",
                0
            )
        )

    except ValueError:

        flash(
            "Please select valid seats.",
            "error"
        )

        return redirect(
            url_for(
                "event_details",
                event_id=event.id
            )
        )


    # -----------------------------------------------------
    # SELECTED SEATS
    # -----------------------------------------------------

    selected_seats_text = request.form.get(
        "selected_seats",
        ""
    ).strip()


    if not selected_seats_text:

        flash(
            "Please select your seats.",
            "error"
        )

        return redirect(
            url_for(
                "event_details",
                event_id=event.id
            )
        )


    selected_seats = [
        seat.strip()
        for seat in selected_seats_text.split(",")
        if seat.strip()
    ]


    # Remove duplicates

    selected_seats = list(
        dict.fromkeys(selected_seats)
    )


    # -----------------------------------------------------
    # VALIDATE NUMBER OF SEATS
    # -----------------------------------------------------

    if number_of_seats <= 0:

        flash(
            "Please select at least one seat.",
            "error"
        )

        return redirect(
            url_for(
                "event_details",
                event_id=event.id
            )
        )


    if len(selected_seats) != number_of_seats:

        flash(
            "Number of selected seats does not match.",
            "error"
        )

        return redirect(
            url_for(
                "event_details",
                event_id=event.id
            )
        )


    # -----------------------------------------------------
    # GET CURRENTLY BOOKED SEATS
    # -----------------------------------------------------

    confirmed_bookings = Booking.query.filter_by(
        event_id=event.id,
        status="Confirmed"
    ).all()

    booked_seats = set()


    for booking in confirmed_bookings:

        if booking.selected_seats:

            seats = booking.selected_seats.split(",")

            for seat in seats:

                booked_seats.add(
                    seat.strip()
                )


    # -----------------------------------------------------
    # CHECK WHETHER SELECTED SEATS ARE ALREADY BOOKED
    # -----------------------------------------------------

    already_booked = []

    for seat in selected_seats:

        if seat in booked_seats:

            already_booked.append(seat)


    if already_booked:

        flash(
            "These seats are already booked: "
            + ", ".join(already_booked),
            "error"
        )

        return redirect(
            url_for(
                "event_details",
                event_id=event.id
            )
        )


    # -----------------------------------------------------
    # CHECK AVAILABLE SEATS
    # -----------------------------------------------------

    if number_of_seats > event.available_seats:

        flash(
            f"Only {event.available_seats} seats are available.",
            "error"
        )

        return redirect(
            url_for(
                "event_details",
                event_id=event.id
            )
        )


    # -----------------------------------------------------
    # CALCULATE TOTAL
    # -----------------------------------------------------

    total_amount = (
        event.price *
        number_of_seats
    )


    # -----------------------------------------------------
    # CREATE BOOKING
    # -----------------------------------------------------

    booking = Booking(

        number_of_seats=number_of_seats,

        selected_seats=",".join(
            selected_seats
        ),

        booking_date=datetime.now(),

        user_id=None,

        event_id=event.id,

        total_amount=total_amount,

        status="Confirmed"

    )


    # Reduce available seats

    event.available_seats -= number_of_seats


    db.session.add(booking)

    db.session.commit()


    return redirect(
        url_for(
            "booking_success",
            booking_id=booking.id
        )
    )


# =========================================================
# BOOKING SUCCESS
# =========================================================

@app.route(
    "/booking-success/<int:booking_id>"
)
def booking_success(booking_id):

    booking = Booking.query.get_or_404(
        booking_id
    )

    return render_template(
        "booking_success.html",
        booking=booking
    )


# =========================================================
# BOOKING HISTORY
# =========================================================

@app.route("/history")
def booking_history():

    bookings = Booking.query.order_by(
        Booking.id.desc()
    ).all()

    return render_template(
        "history.html",
        bookings=bookings
    )


# =========================================================
# CANCEL BOOKING
# =========================================================

@app.route(
    "/cancel/<int:booking_id>",
    methods=["POST"]
)
def cancel_booking(booking_id):

    booking = Booking.query.get_or_404(
        booking_id
    )


    if booking.status == "Cancelled":

        flash(
            "This booking is already cancelled.",
            "error"
        )

        return redirect(
            url_for("booking_history")
        )


    # Return seats to available count

    booking.event.available_seats += (
        booking.number_of_seats
    )


    booking.status = "Cancelled"


    db.session.commit()


    flash(
        "Booking cancelled successfully.",
        "success"
    )


    return redirect(
        url_for("booking_history")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )