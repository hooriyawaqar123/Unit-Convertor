import streamlit as st
import requests
from pint import UnitRegistry

EXCHANGE_API_KEY = "cur_live_J9r5kJTyGCr9B6dQDg1vvOKmqY1tcIsormqLhDrD"

ureg = UnitRegistry()

def convert_units(value, from_unit, to_unit):
    try:
        print(f"Converting {value} {from_unit} to {to_unit}")
        if from_unit in ["celsius", "fahrenheit", "kelvin"] and to_unit in ["celsius", "fahrenheit", "kelvin"]:
            temp = ureg.Quantity(value, f"deg{from_unit[0].upper()}")
            result = temp.to(f"deg{to_unit[0].upper()}")
        else:
            result = (value * ureg(from_unit)).to(to_unit)
        print(f"Conversion result: {result.magnitude}")
        return round(result.magnitude, 4)
    except Exception as e:
        print("Invalid unit conversion.")
        return "Invalid unit conversion."

def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.currencyapi.com/v3/latest?apikey={EXCHANGE_API_KEY}&base_currency={from_currency.upper()}"
    try:
        print(f"Fetching currency conversion rate from {from_currency} to {to_currency}")
        response = requests.get(url)
        data = response.json()
        if "data" in data and to_currency.upper() in data["data"]:
            rate = data["data"][to_currency.upper()]['value']
            converted_amount = round(amount * rate, 2)
            print(f"Converted amount: {converted_amount}")
            return converted_amount
        else:
            print("Invalid currency code or API issue.")
            return "Invalid currency code or API issue."
    except Exception as e:
        print(f"API Error: {str(e)}")
        return f"API Error: {str(e)}"

st.title("🌎 Advanced Unit Converter")
st.write("Convert units instantly!")

conversion_types = ["Length", "Weight", "Temperature", "Currency", "Area", "Volume", "Speed", "Time"]
option = st.selectbox("Choose conversion type", conversion_types)

unit_options = {
    "Length": ["meter", "kilometer", "centimeter", "millimeter", "mile", "yard", "foot", "inch"],
    "Weight": ["kilogram", "gram", "pound", "ounce", "stone"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Area": ["square meter", "square kilometer", "square foot", "square yard", "acre", "hectare"],
    "Volume": ["liter", "milliliter", "cubic meter", "gallon", "pint", "cup"],
    "Speed": ["meter per second", "kilometer per hour", "mile per hour", "knot"],
    "Time": ["second", "minute", "hour", "day", "week", "month", "year"]
}

if option in unit_options:
    value = st.number_input("Enter value", min_value=0.0, step=0.01)
    from_unit = st.selectbox("From", unit_options[option])
    to_unit = st.selectbox("To", unit_options[option])
    
    if st.button("Convert"):
        result = convert_units(value, from_unit, to_unit)
        st.success(f"✅ **{value} {from_unit}** = **{result} {to_unit}**")

elif option == "Currency":
    amount = st.number_input("Enter amount", min_value=0.0, step=0.01)
    from_currency = st.text_input("From currency (e.g., PKR)", placeholder="PKR")
    to_currency = st.text_input("To currency (e.g., USD)", placeholder="USD")
    
    if st.button("Convert"):
        if from_currency and to_currency:
            result = convert_currency(amount, from_currency, to_currency)
            st.success(f"💰 **{amount} {from_currency.upper()}** = **{result} {to_currency.upper()}**")
        else:
            st.warning("⚠️ Please enter valid currency codes.")