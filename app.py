from selenium import webdriver
import time
import warnings
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from flask import Flask, request

warnings.filterwarnings("ignore")

app = Flask(__name__)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
PROXY = "localhost:8888"

options = ChromeOptions()
options.headless = True

options.add_argument(f"user-agent={user_agent}")
# options.add_argument("--window-size=1920,1080")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
# options.add_argument("--start-maximized")
options.add_argument("--enable-javascript")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")


@app.route("/checkAvailability", methods=["GET", "POST"])
def get_availability():
    if request.method == "POST":

        # Getting api parameters
        data = request.get_json(force=True)
        date = data["dateForBooking"]
        newDate = date.split("/")
        newDate = newDate[::-1]
        timing = data["timing"]
        timing = int(timing)

        # using links
        links = [
            "https://girlion.gujarat.gov.in/GirJungleTrailBooking.aspx",
            "https://girlion.gujarat.gov.in/GIZDevaliaGypsyBooking.aspx",
        ]

        errorids = [
            "#ContentPlaceHolder1_GirJungleTrail_lblErrorMessage",
            "#ContentPlaceHolder1_GIZDevaliaGypsy_lblErrorMessage",
        ]

        # starting driver
        driver = webdriver.Chrome(options=options)
        driver.get(links[data["number"] - 1])
        time.sleep(2)  # sleep_between_interactions

        # executing scripts
        driver.execute_script(
            "document.querySelectorAll('table input')[0].value=arguments[0]", date
        )
        time.sleep(5)
        driver.execute_script(
            "document.querySelectorAll('div.form-group select')[0].options[arguments[0]].selected=true",
            timing,
        )
        time.sleep(5)
        driver.execute_script("document.querySelector('#btnCheckAvailability').click()")
        time.sleep(5)
        driver.execute_script(
            "document.querySelectorAll('table input')[1].value=arguments[0]",
            "-".join(newDate) + "-00-00-00",
        )
        time.sleep(5)
        driver.execute_script("document.querySelector('#btnCheckAvailability').click()")
        time.sleep(5)
        driver.execute_script(
            "document.querySelectorAll('div.form-group select')[0].options[arguments[0]].selected=true",
            timing,
        )
        time.sleep(5)
        driver.execute_script("document.querySelector('#btnCheckAvailability').click()")
        time.sleep(5)
        txt = driver.execute_script(
            "return document.querySelector(arguments[0]).textContent",
            errorids[data["number"] - 1],
        )

        # Returning Availability
        if "Permits" in txt:
            return str(False)
        else:
            return str(True)


app.run()
