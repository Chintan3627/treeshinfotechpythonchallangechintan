#!/usr/bin/env python3
import requests
import json
import csv
import argparse
import sys
import os

# Get the current working directory
current_directory = os.getcwd()

# Print the result


class RestClient:
    def __init__(self, method, endpoint, outfile=None,outdata=None):
        self.method = method
        self.endpoint = endpoint
        self.outfile = outfile
        self.outdata = outdata

    def make_request(self):
        url = f"https://jsonplaceholder.typicode.com{self.endpoint}"
        response = requests.get(url)

        # Display HTTP status code
        print(f"HTTP Status Code: {response.status_code}")

        if response.status_code // 100 != 2:
            print(f"Error: {response.text}")
            sys.exit(1)

        return response.json()

    def save_to_file(self, data):
        if self.outfile:
            if self.outfile.endswith('.json'):
                with open(current_directory + '/' + self.outfile, 'w') as json_file:
                    json.dump(data, json_file, indent=2)
            elif self.outfile.endswith('.csv'):
                with open(self.outfile, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    if isinstance(data, list):
                        writer.writerow(data[0].keys())
                        for item in data:
                            writer.writerow(item.values())
                    elif isinstance(data, dict):
                        writer.writerow(data.keys())
                        writer.writerow(data.values())
            else:
                print("Unsupported file format. Use .json or .csv.")
                sys.exit(1)
        else:
            print(json.dumps(data, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Simple RESTful command-line client")
    parser.add_argument("METHOD", choices=["get", "post"], help="Request method")
    parser.add_argument("ENDPOINT", help="Request endpoint URI fragment")
    parser.add_argument("-d", "--data", help="Data to send with request")
    parser.add_argument("-o", "--output", help="Output file (JSON or CSV)")


    args = parser.parse_args()

    rest_client = RestClient(args.METHOD, args.ENDPOINT, args.output, args.data)
    if rest_client.outdata is  None:
        response_data = rest_client.make_request()
        rest_client.save_to_file(response_data)
    else:
        rest_client.save_to_file(rest_client.outdata)

        

if __name__ == "__main__":
    main()
