import requests
import datetime as dt
import smtplib
import time

def check_iss_location_sendmail():
    # ------------------------------ ISS LOCATION ------------------------------
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    iss_latitude = float(response.json()["iss_position"]["latitude"])
    iss_longitude = float(response.json()["iss_position"]["longitude"])


    iss_position = (iss_latitude, iss_longitude)
    print(f"Current ISS position: {iss_position}")

    # ------------------------- SUNRISE AND SUNSET HOUR ------------------------
    MY_LATITUDE = 46.239750
    MY_LONGITUDE = 15.267706
    # MY_LATITUDE = 28.4554 #testing
    # MY_LONGITUDE = -21.3067 #testing

    parameters = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        "formatted": 0,
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    sunrise_sunset_data = response.json()
    sunrise = (sunrise_sunset_data["results"]["sunrise"])
    sunset = (sunrise_sunset_data["results"]["sunset"])
    sunrise_hour = int(sunrise.split("T")[1].split(":")[0]) + 2
    sunset_hour = int(sunset.split("T")[1].split(":")[0]) + 2
    print(f"Sunrise: {sunrise_hour}, Sunset:{sunset_hour}")

    # -------------------------- CURRENT TIME (HOUR) --------------------------
    current_hour = dt.datetime.now().time().hour
    print(f"Current clock: {current_hour}")

    # -------------------- SEND EMAIL WHEN ISS ISS IS NEAR --------------------
    MY_GMAIL = ""
    MY_PASSWORD = ""

    if current_hour > sunrise_hour:
        if MY_LATITUDE - 5 < iss_latitude < MY_LATITUDE + 5 and MY_LONGITUDE - 5 < iss_longitude < MY_LONGITUDE + 5:
            print("look up")
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_GMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_GMAIL,
                    to_addrs="peter.stepanic@hotmail.com",
                    msg=f"ISS above\n\nLOOK UP and spot the ISS"
                )
        else:
            print("Out of range")
    else:
        print("It is not night time.")


while True:
    check_iss_location_sendmail()
    time.sleep(16)
