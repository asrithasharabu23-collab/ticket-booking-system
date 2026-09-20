/* =========================================================
   CINEMA TICKET BOOKING
   SEAT SELECTION + PRICE CALCULATION
========================================================= */


document.addEventListener(
    "DOMContentLoaded",
    function () {


        // =================================================
        // GET ELEMENTS
        // =================================================

        const seatInput =
            document.getElementById(
                "number_of_seats"
            );


        const selectedSeatsInput =
            document.getElementById(
                "selectedSeats"
            );


        const totalAmount =
            document.getElementById(
                "totalAmount"
            );


        const seatCount =
            document.getElementById(
                "seatCount"
            );


        const increaseButton =
            document.getElementById(
                "increaseSeat"
            );


        const decreaseButton =
            document.getElementById(
                "decreaseSeat"
            );


        const bookingForm =
            document.querySelector(
                ".booking-form"
            );


        const seats =
            document.querySelectorAll(
                ".seat:not(.occupied)"
            );


        // =================================================
        // IF NOT ON BOOKING PAGE
        // =================================================

        if (!seatInput || !bookingForm) {

            return;

        }


        // =================================================
        // MOVIE PRICE
        // =================================================

        const price =
            parseFloat(
                seatInput.dataset.price
            ) || 0;


        // =================================================
        // GET SELECTED SEATS
        // =================================================

        function getSelectedSeats() {

            return Array.from(
                document.querySelectorAll(
                    ".seat.selected"
                )
            );

        }


        // =================================================
        // UPDATE PRICE
        // =================================================

        function updatePrice() {

            const selected =
                getSelectedSeats();


            const count =
                selected.length;


            seatInput.value =
                count;


            seatCount.textContent =
                count;


            const total =
                count * price;


            totalAmount.textContent =
                "₹" + total.toFixed(0);


            selectedSeatsInput.value =
                selected
                    .map(
                        seat =>
                            seat.dataset.seat
                    )
                    .join(",");

        }


        // =================================================
        // SELECT SEAT
        // =================================================

        function selectSeat(seat) {

            if (
                seat.classList.contains(
                    "occupied"
                )
            ) {

                return;

            }


            const selected =
                getSelectedSeats();


            const maxSeats =
                parseInt(
                    seatInput.max
                );


            if (
                selected.length >=
                maxSeats
            ) {

                showMessage(
                    "You cannot select more than " +
                    maxSeats +
                    " seats."
                );

                return;

            }


            seat.classList.add(
                "selected"
            );


            updatePrice();

        }


        // =================================================
        // UNSELECT SEAT
        // =================================================

        function unselectSeat(seat) {

            seat.classList.remove(
                "selected"
            );


            updatePrice();

        }


        // =================================================
        // SEAT CLICK
        // =================================================

        seats.forEach(
            function (seat) {

                seat.addEventListener(
                    "click",
                    function () {


                        if (
                            seat.classList.contains(
                                "selected"
                            )
                        ) {

                            unselectSeat(
                                seat
                            );

                        } else {

                            selectSeat(
                                seat
                            );

                        }

                    }
                );

            }
        );


        // =================================================
        // INCREASE NUMBER OF TICKETS
        // =================================================

        if (increaseButton) {

            increaseButton.addEventListener(
                "click",
                function () {


                    const selected =
                        getSelectedSeats();


                    const maxSeats =
                        parseInt(
                            seatInput.max
                        );


                    if (
                        selected.length >=
                        maxSeats
                    ) {

                        showMessage(
                            "Maximum available seats reached."
                        );

                        return;

                    }


                    /*
                       Find first available
                       unselected seat.
                    */

                    const nextSeat =
                        Array.from(
                            seats
                        ).find(
                            seat =>
                                !seat.classList.contains(
                                    "selected"
                                )
                        );


                    if (nextSeat) {

                        selectSeat(
                            nextSeat
                        );

                    }

                }
            );

        }


        // =================================================
        // DECREASE NUMBER OF TICKETS
        // =================================================

        if (decreaseButton) {

            decreaseButton.addEventListener(
                "click",
                function () {


                    const selected =
                        getSelectedSeats();


                    if (
                        selected.length <= 1
                    ) {

                        showMessage(
                            "At least one seat must be selected."
                        );

                        return;

                    }


                    const lastSeat =
                        selected[
                            selected.length - 1
                        ];


                    unselectSeat(
                        lastSeat
                    );

                }
            );

        }


        // =================================================
        // FORM SUBMISSION
        // =================================================

        bookingForm.addEventListener(
            "submit",
            function (event) {


                const selected =
                    getSelectedSeats();


                if (
                    selected.length === 0
                ) {

                    event.preventDefault();


                    showMessage(
                        "Please select at least one seat."
                    );


                    return;

                }


                /*
                   Make sure hidden input
                   contains the selected seats.
                */

                selectedSeatsInput.value =
                    selected
                        .map(
                            seat =>
                                seat.dataset.seat
                        )
                        .join(",");


                seatInput.value =
                    selected.length;


                updatePrice();

            }
        );


        // =================================================
        // MESSAGE
        // =================================================

        function showMessage(message) {


            let messageBox =
                document.querySelector(
                    ".seat-message"
                );


            if (!messageBox) {

                messageBox =
                    document.createElement(
                        "div"
                    );


                messageBox.className =
                    "seat-message";


                messageBox.style.cssText = `
                    margin: 15px 0;
                    padding: 12px 15px;
                    border-radius: 10px;
                    background: rgba(255,83,100,0.10);
                    border: 1px solid rgba(255,83,100,0.25);
                    color: #ff7482;
                    font-size: 12px;
                    text-align: center;
                `;


                bookingForm.insertBefore(
                    messageBox,
                    bookingForm.firstChild
                );

            }


            messageBox.textContent =
                message;


            setTimeout(
                function () {

                    if (messageBox) {

                        messageBox.remove();

                    }

                },
                2500
            );

        }


        // =================================================
        // SELECT FIRST SEAT AUTOMATICALLY
        // =================================================

        const firstAvailableSeat =
            Array.from(
                seats
            ).find(
                seat =>
                    !seat.classList.contains(
                        "occupied"
                    )
            );


        if (firstAvailableSeat) {

            firstAvailableSeat.classList.add(
                "selected"
            );

        }


        // =================================================
        // INITIAL PRICE
        // =================================================

        updatePrice();

    }
);
