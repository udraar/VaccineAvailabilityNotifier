import requests
import argparse
import sys
import time
from datetime import datetime, timedelta


class ArgParser(object):

    @staticmethod
    def arg_parser() -> argparse.ArgumentParser:
        """
        Object for parsing command line strings into Python objects
        """
        parser = argparse.ArgumentParser(
            description="Vaccine availability argument parser")
        parser.add_argument("--search_by", required=True,
                            help="Options: pin, district")
        parser.add_argument("--search_days", required=False, default=1, type=int,
                            help="Number of days to search from today")
        parser.add_argument("--age", required=False, default=100,
                            help="Age of the person to be vaccinated")
        parser.add_argument("--pin", required=False,
                            help="PIN code of search area")
        parser.add_argument("--district", required=False,
                            help="District of the search area")
        parser.add_argument("--state", required=False,
                            help="State of the search area")
        parser.add_argument("--search_frequency", required=False, default=30,
                            help="Interval between search retry. Default 30 mins")
        return parser


class Searcher(object):
    base_url = "https://cdn-api.co-vin.in/api"

    def __init__(self, age=100):
        self.age = age
        self.pin_code = None
        self.district_name = None
        self.state_code = 36

    def search_by_pin(self, pin_code, duration_in_days=1):
        self.pin_code = pin_code
        api_endpoint = "/v2/appointment/sessions/public/calendarByPin"
        url = f"{Searcher.base_url + api_endpoint}?pincode={self.pin_code}"
        headers = {"User-Agent": "PostmanRuntime/7.28.0"}
        payload = {}
        date_range = Searcher.fetch_dates(duration_in_days)
        availability = []

        for day in date_range:
            iter_url = f"{url}&date={day}"
            response = requests.request("GET", iter_url, headers=headers,
                                        data=payload)
            if response.status_code == 200:
                formatted_response = Searcher.json_formatter(response.json(),
                                                             self.age)
                availability.extend(formatted_response)
        Searcher.printer(availability)

    def search_by_district(self, district_name, duration_in_days=1):
        self.district_name = district_name
        api_endpoint = "/v2/appointment/sessions/public/calendarByDistrict"
        district_id = self.fetch_district_code()
        url = f"{Searcher.base_url + api_endpoint}?district_id={district_id}"
        headers = {"User-Agent": "PostmanRuntime/7.28.0"}
        payload = {}
        date_range = Searcher.fetch_dates(duration_in_days)
        availability = []

        for day in date_range:
            iter_url = f"{url}&date={day}"
            response = requests.request("GET", iter_url, headers=headers,
                                        data=payload)
            if response.status_code == 200:
                formatted_response = Searcher.json_formatter(response.json(),
                                                             self.age)
                availability.extend(formatted_response)
        Searcher.printer(availability)

    def fetch_district_code(self):
        api_endpoint = "/v2/admin/location/districts/" + str(self.state_code)
        url = f"{Searcher.base_url + api_endpoint}"
        headers = {"User-Agent": "PostmanRuntime/7.28.0"}
        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            district_names = []
            district_id = None
            response_json = response.json()
            for district in response_json["districts"]:
                if district["district_name"] == self.district_name:
                    district_id = district["district_id"]
                else:
                    district_names.append(district["district_name"])
            if district_id:
                return district_id
            else:
                print(
                    f"District name not found.\nAvailable district names:\n{district_names}")
                exit(0)

    @staticmethod
    def fetch_dates(days_cnt):
        today = datetime.today()
        date_range = [today + timedelta(days=c) for c in range(days_cnt)]
        op_dates = [d.strftime("%d-%m-%Y") for d in date_range]
        return op_dates

    @staticmethod
    def json_formatter(json_obj, age_limit=100):
        formatted_json = []
        for center in json_obj["centers"]:
            op_json = {"Center Name": center["name"],
                       "Address": center["address"],
                       "Pincode": center["pincode"],
                       "Fee": center["fee_type"]}
            for session in center["sessions"]:
                if session["available_capacity"] > 0 and int(
                        session["min_age_limit"]) <= age_limit:
                    op_json["Min Age"] = session["min_age_limit"]
                    op_json["Vaccine Name"] = session["vaccine"]
                    op_json["Availability On"] = session["date"]
                    op_json["Slots"] = ", ".join(session["slots"])
                    op_json["Total Availability"] = session[
                        "available_capacity"]
                    op_json["Dose 1 Capacity"] = session[
                        "available_capacity_dose1"]
                    op_json["Dose 2 Capacity"] = session[
                        "available_capacity_dose2"]
                    formatted_json.append(op_json)
        return formatted_json

    @staticmethod
    def printer(json_obj):
        if json_obj:
            print("Vaccine availability:")
            for line in json_obj:
                print("")
                for key in line.keys():
                    print(f"{key}: {line[key]}")
            exit(0)
        else:
            print("No slots available")


def main():
    search_args = vars(ArgParser.arg_parser().parse_args())
    if search_args["search_by"] == "pin":
        if search_args.get("pin"):
            while True:
                search_obj = Searcher(int(search_args["age"]))
                search_obj.search_by_pin(search_args["pin"], search_args["search_days"])
                time.sleep(int(search_args["search_frequency"]) * 60)
        else:
            print("No pin available")
            exit(0)
    if search_args["search_by"] == "district":
        if search_args.get("district"):
            while True:
                search_obj = Searcher(int(search_args["age"]))
                search_obj.search_by_district(search_args["district"], search_args["search_days"])
                time.sleep(int(search_args["search_frequency"]) * 60)
        else:
            print("No district available")
            exit(0)


if __name__ == "__main__":
    print(sys.argv)
    main()
