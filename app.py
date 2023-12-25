from flask import Flask, flash, redirect,render_template, request, session
from cs50 import SQL
from datetime import datetime
import numpy_financial as npf
import pandas as pd

app = Flask(__name__)

today = datetime.now()
year = today.year

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/")
def index():

    return render_template("index.html", date=year)

@app.route("/loan", methods=["GET", "POST"])
def loan():
    try:
        if request.method == "POST":
            annual_interest_rate = int(request.form.get("rate"))
            principal = int(request.form.get("amount"))
            terms = int(request.form.get("terms"))

            # Calculate monthly interest rate
            monthly_interest_rate = annual_interest_rate / 12 / 100

            # Total number of payments
            num_payment = terms * 12

            # Calculate monthly payment using the numpy_financial library
            monthly_payment = -npf.pmt(rate=monthly_interest_rate, nper=num_payment, pv=principal)

            # Generate amortization schedule
            payment_schedule = pd.DataFrame(index=range(1, num_payment + 1))
            payment_schedule.index.name = 'Payment'

            #Calculate Total Payement
            total_payment = round(monthly_payment * num_payment, 2)

            #total interest
            total_interest = round(total_payment - principal, 2)
            # Initialize balance
            remaining_balance = principal

            # Populate the amortization schedule
            for payment_number in range(1, num_payment + 1):
                interest_payment = remaining_balance * monthly_interest_rate
                principal_payment = monthly_payment - interest_payment

                payment_schedule.loc[payment_number, 'Principal Payment'] = principal_payment
                payment_schedule.loc[payment_number, 'Interest Payment'] = interest_payment
                payment_schedule.loc[payment_number, 'Beginning Balance'] = remaining_balance
                remaining_balance -= principal_payment
                payment_schedule.loc[payment_number, 'Remaining Balance'] = remaining_balance
            
            return render_template("loan.html", date=year, schedule=payment_schedule.iterrows(), monthly_payment=round(monthly_payment, 2), total_payment=total_payment, total_interest=total_interest)
    except ValueError:
        print()
    return render_template("loan.html", date=year)

@app.route("/savings", methods=["GET", "POST"])
def savings():
    try:
        message = "Your savings could be worth:"
        if request.method == "POST":
            rate = int(request.form.get("rate"))
            starting_amount = int(request.form.get("starting_amount"))
            terms = int(request.form.get("terms"))

            #Determine the number of deposit
            num_deposit = terms * 12

            #Calculate the monthly rate
            monthly_rate = rate /12 / 100

            #Set the new or initial starting amount
            compound = starting_amount

            future_values = pd.DataFrame(index=range(1, num_deposit + 1))

            #fille the future_value data frame with the it data 
            for deposit in range(1, num_deposit + 1):
                interest = starting_amount * monthly_rate
                future_values.loc[deposit, "New Amount"] = compound 
                future_values.loc[deposit, "Monthly Earned Interest"] = interest

                compound = compound * (1 + monthly_rate)
                future_values.loc[deposit, "Monthly Compound Amount"] = compound

            #calculate the future value after a certain amount of time.
            fv = round(npf.fv((rate/100)/12,terms*12,0,-starting_amount), 2)
            
            return render_template("savings.html", date=year, fv=fv, message=message, last_term=f"after {terms} years", future_value=future_values.iterrows())  
    except ValueError:
        print()
    return render_template("savings.html", date=year)


