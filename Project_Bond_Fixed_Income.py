# Project 6: Fixed Income Analytics
# Name: Rahul Solanki
#
# Description:
# This project performs bond valuation and interest rate risk analysis.
# It calculates:
# 1. Bond Price
# 2. Bond Price vs Yield Relationship
# 3. Macaulay Duration
# 4. Modified Duration
# 5. Convexity
# 6. Interest Rate Sensitivity Analysis
#
# Libraries Used:
# NumPy
# Pandas
# Matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------
# Inputs
# --------------------------

face_value = 100
coupon_rate = 0.06
ytm = 0.05
maturity = 3


# --------------------------
# Bond Pricing Function
# --------------------------

def bond_price(face_value, coupon_rate, ytm, maturity):

    coupon_payment = face_value * coupon_rate

    price = 0

    for t in range(1, maturity + 1):

        if t == maturity:
            cash_flow = coupon_payment + face_value
        else:
            cash_flow = coupon_payment

        present_value = cash_flow / ((1 + ytm) ** t)

        price += present_value

    return price


current_bond_price = bond_price(face_value,coupon_rate,ytm,maturity)

print("Bond Price =", round(current_bond_price,4))

# --------------------------
# Price vs Yield Analysis
# --------------------------

yield_list = np.arange(0.01,0.16,0.01)

prices = []

for y in yield_list:

    price = bond_price(face_value,coupon_rate,y,maturity)

    prices.append(price)

results_df = pd.DataFrame({
    "YTM (%)":yield_list*100,
    "Bond Price":prices
})

results_df["Bond Price"] = results_df["Bond Price"].round(4)

print()
print(results_df)

plt.figure(figsize=(10,6))

plt.plot(
    results_df["YTM (%)"],
    results_df["Bond Price"],
    marker='o'
)

plt.xlabel("Yield to Maturity (%)")
plt.ylabel("Bond Price")
plt.title("Bond Price vs Yield")
plt.grid(True)
plt.savefig( "charts/bond_price_vs_yield.png",dpi=300)
plt.show()

# --------------------------
# Macaulay Duration Function
# --------------------------

def macaulay_duration(face_value, coupon_rate, ytm, maturity):

    coupon_payment = face_value * coupon_rate

    weighted_pv_sum = 0

    bondprice = bond_price(
        face_value,
        coupon_rate,
        ytm,
        maturity
    )

    for t in range(1, maturity + 1):

        if t == maturity:
            cash_flow = coupon_payment + face_value
        else:
            cash_flow = coupon_payment

        present_value = cash_flow / ((1 + ytm)**t)

        weighted_pv_sum += t * present_value

    duration = weighted_pv_sum / bondprice

    return duration


duration = macaulay_duration(face_value,coupon_rate,ytm,maturity)

print()
print("Macaulay Duration =", round(duration,4), "years")

# --------------------------
# Modified Duration Function
# --------------------------

def modified_duration(face_value, coupon_rate, ytm, maturity):

    macaulay = macaulay_duration(
        face_value,
        coupon_rate,
        ytm,
        maturity
    )

    mod_duration = macaulay / (1 + ytm)

    return mod_duration


mod_duration = modified_duration(face_value,coupon_rate,ytm,maturity)

print()
print("Modified Duration =", round(mod_duration,4))

# --------------------------
# Convexity Function
# --------------------------

def convexity(face_value, coupon_rate, ytm, maturity):

    coupon_payment = face_value * coupon_rate

    bondprice = bond_price(face_value,coupon_rate,ytm,maturity)

    convexity_sum = 0

    for t in range(1, maturity + 1):

        if t == maturity:
            cash_flow = coupon_payment + face_value
        else:
            cash_flow = coupon_payment

        present_value = cash_flow / ((1 + ytm) ** t)

        convexity_sum += t * (t + 1) * present_value

    convexity_value = convexity_sum / (bondprice * (1 + ytm) ** 2)

    return convexity_value


conv = convexity(face_value,coupon_rate,ytm,maturity)

print()
print("Convexity =", round(conv,4))

# --------------------------
# Duration Approximation
# --------------------------

delta_y = 0.01

price_change_percent = (
        -mod_duration * delta_y
        + 0.5 * conv * (delta_y ** 2)
)

estimated_new_price = current_bond_price * (1 + price_change_percent)

new_ytm = ytm + delta_y

actual_new_price = bond_price(face_value,coupon_rate,new_ytm, maturity)

print()
print("Estimated Bond Price =", round(estimated_new_price,4))
print("Actual Bond Price =", round(actual_new_price,4))