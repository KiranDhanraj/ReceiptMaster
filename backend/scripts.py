import os
import urllib.request
import json
import pprint
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import math
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("UPC_API_KEY")
if not API_KEY:
    raise ValueError("UPC_API_KEY environment variable not set")

# This function takes an string barcode as input and searches for the product site on Walmart's Website
def add_check_digit(barcode):
    mod_code = int(barcode)/10
    sum_even = 0
    sum_odd = 0
    for i in range(math.floor(math.log10(mod_code))+1):
        digit = int(mod_code%10)
        if i%2 == 0:
            sum_even += digit
        else:
            sum_odd += digit
        mod_code /= 10
    check_digit = (10 - ((sum_even*3 + sum_odd) % 10)) % 10
    return (str(int(barcode) + check_digit))
def get_product(barcode):
    if(bool(re.fullmatch(r"0{6}\d{6}", barcode))):
        return "Bulk Produce", "Bulk Produce", "N/A", "Bulk Item"
    barcode = add_check_digit(barcode)
    req = Request('https://go-upc.com/api/v1/code/' + barcode)
    req.add_header('Authorization', 'Bearer ' + API_KEY)
    try:
        content = urlopen(req).read()
        data = json.loads(content.decode())
    except HTTPError:
        return "N/A", "N/A", "N/A", "N/A"
    except URLError:
        return "N/A", "N/A", "N/A", "N/A"
    product = data.get("product") or {}
    name = product.get("name") or "N/A"
    description = product.get("description") or "N/A"
    brand = product.get("brand") or "N/A"
    category_path = product.get("categoryPath") or []
    category = category_path[0] if category_path else (product.get("category") or "N/A")

    return name, category, brand, description

