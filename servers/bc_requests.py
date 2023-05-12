import json

import requests
from tenacity import retry, wait_exponential, stop_after_attempt

store_hash = "88sppjdb0w"
access_token = "1vmpwzho1hr8yw5lditr8eso0dnh4cv"
# store_hash = "rmz2xgu42d"
# access_token = "jpts4mh09fxfef5ysqcgyyuqnegorgb"
base_url = "https://api.bigcommerce.com/stores"


class BCCustomers:

    def __init__(self):
        self.session = requests.session()
        self.headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "X-Auth-Token": access_token
        }

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_a_customer(self, customer_id):
        url = f"{base_url}/{store_hash}/v2/customers/{customer_id}"
        resp = self.session.get(url, headers=self.headers)
        if resp.status_code != 200 and resp.status_code != 201:
            return False
        return resp.json()

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_all_customer(self):
        url = f"{base_url}/{store_hash}/v2/customers"
        resp = self.session.get(url, headers=self.headers)
        if resp.status_code != 200 and resp.status_code != 201:
            return False
        return resp.json()

    '''
        https://api.bigcommerce.com/stores/{store_hash}/v3/customers
        Creates a Customer. Required Fields  / POST
    '''
    """
    data = [{
            "email": user.get('email'),
            "first_name": user.get('user_name'),
            "last_name": user.get('user_name'),
            # "company": "test",
            # "phone": "11111111111",
            # "notes": "",
            # "tax_exempt_category": "",
            # "customer_group_id": 0,
            "addresses": [
                {
                    "address1": user.get('address'),
                    # "address2": "",
                    # "address_type": "residential",
                    "city": "San Francisco",
                    # "company": "History",
                    "country_code": "US",
                    "first_name": "Ronald",
                    "last_name": "Swimmer",
                    # "phone": "11111111111",
                    "postal_code": "33333",
                    "state_or_province": "California",
                    # "form_fields": []
                }
            ],
            "authentication": {
                "force_password_reset": True,
                "new_password": "Djh010726..."
            },
            "accepts_product_review_abandoned_cart_emails": True,
            "store_credit_amounts": [{"amount": 0}],
            "origin_channel_id": 1,
            "channel_ids": [1],
            "form_fields": []
        }]
    """

    def create_a_customers(self, user):
        data = [{
            "email": user.get('email'),
            "first_name": user.get('user_name'),
            "last_name": user.get('user_name'),
            "addresses": [
                {
                    "address1": user.get('address'),
                    "city": "San Francisco",
                    "country_code": "US",
                    "first_name": "Ronald",
                    "last_name": "Swimmer",
                    "postal_code": "33333",
                    "state_or_province": "California",
                }
            ],
            "authentication": {
                "force_password_reset": True,
                "new_password": user.get('password')
            },
        }]
        post_data = json.dumps(data)
        url = f"{base_url}/{store_hash}/v3/customers"
        resp = self.session.post(url, headers=self.headers, data=post_data)
        if resp.status_code != 200 and resp.status_code != 201:
            return False
        return resp.json()

    """
        Create an Order
        https://api.bigcommerce.com/stores/{store_hash}/v2/orders POST
    """
    """
    products
    billing_address
    {
        "status_id": 0,
        "customer_id": 11,
        "billing_address": {
            "first_name": "Jane",
            "last_name": "Doe",
            "street_1": "123 Main Street",
            "city": "Austin",
            "state": "Texas",
            "zip": "78751",
            "country": "United States",
            "country_iso2": "US",
            "email": "janedoe@example.com"
          },
        "products": [{
            "name": "BigCommerce Poster",
            "quantity": 1,
            "price_inc_tax": 10.98,
            "price_ex_tax": 10
        },
        {
            "name": "BigCommerce Coffee Mug",
            "quantity": 1,
            "price_inc_tax": 50,
            "price_ex_tax": 45
        },]}
    """

    def create_an_order(self, user):
        data = {
            "customer_id": user.get("customer_id"),
            "billing_address": {
                "first_name": "Jane",
                "last_name": "Doe",
                "street_1": "123 Main Street",
                "city": "Austin",
                "state": "Texas",
                "zip": "78751",
                "country": "United States",
                "country_iso2": "US",
                "email": user.get('email')
            },
            "products": [{
                "name": "BigCommerce Poster",
                "quantity": 1,
                "price_inc_tax": 10.98,
                "price_ex_tax": 10
            }, {
                "name": "BigCommerce Coffee Mug",
                "quantity": 1,
                "price_inc_tax": 50,
                "price_ex_tax": 45}]}
        url = f"{base_url}/{store_hash}/v2/orders"
        post_data = json.dumps(data)
        resp = self.session.post(url, headers=self.headers, data=post_data)
        if resp.status_code != 200 and resp.status_code != 201:
            return False
        return resp.json()


class BCCustomersNew:

    def __init__(self, store, token):
        self.base_url = "https://api.bigcommerce.com/stores/" + store
        self.session = requests.session()
        self.headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "X-Auth-Token": token
        }

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_a_customer(self, customer_id):
        url = f"{self.base_url}/v2/customers/{customer_id}"
        resp = self.session.get(url, headers=self.headers)
        if resp.status_code != 200 and resp.status_code != 201:
            return False
        return resp.json()

    @retry(reraise=True, wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(5))
    def get_all_customer(self):
        url = f"{self.base_url}/v2/customers"
        resp = self.session.get(url, headers=self.headers)
        if resp.status_code != 200 and resp.status_code != 201:
            return False
        return resp.json()

    '''
        https://api.bigcommerce.com/stores/{store_hash}/v3/customers
        Creates a Customer. Required Fields  / POST
    '''
    """
    data = [{
            "email": user.get('email'),
            "first_name": user.get('user_name'),
            "last_name": user.get('user_name'),
            # "company": "test",
            # "phone": "11111111111",
            # "notes": "",
            # "tax_exempt_category": "",
            # "customer_group_id": 0,
            "addresses": [
                {
                    "address1": user.get('address'),
                    # "address2": "",
                    # "address_type": "residential",
                    "city": "San Francisco",
                    # "company": "History",
                    "country_code": "US",
                    "first_name": "Ronald",
                    "last_name": "Swimmer",
                    # "phone": "11111111111",
                    "postal_code": "33333",
                    "state_or_province": "California",
                    # "form_fields": []
                }
            ],
            "authentication": {
                "force_password_reset": True,
                "new_password": "Djh010726..."
            },
            "accepts_product_review_abandoned_cart_emails": True,
            "store_credit_amounts": [{"amount": 0}],
            "origin_channel_id": 1,
            "channel_ids": [1],
            "form_fields": []
        }]
    """

    def create_a_customers(self, user):
        data = [{
            "email": user.get('email'),
            "first_name": user.get('user_name'),
            "last_name": user.get('user_name'),
            "addresses": [
                {
                    "address1": user.get('address'),
                    "city": "San Francisco",
                    "country_code": "US",
                    "first_name": "Ronald",
                    "last_name": "Swimmer",
                    "postal_code": "33333",
                    "state_or_province": "California",
                }
            ],
            "authentication": {
                "force_password_reset": True,
                "new_password": user.get('password')
            },
        }]
        post_data = json.dumps(data)
        url = f"{self.base_url}/v3/customers"
        resp = self.session.post(url, headers=self.headers, data=post_data)
        if resp.status_code != 200 and resp.status_code != 201:
            return False
        return resp.json()

    """
        Create an Order
        https://api.bigcommerce.com/stores/{store_hash}/v2/orders POST
    """
    """
    products
    billing_address
    {
        "status_id": 0,
        "customer_id": 11,
        "billing_address": {
            "first_name": "Jane",
            "last_name": "Doe",
            "street_1": "123 Main Street",
            "city": "Austin",
            "state": "Texas",
            "zip": "78751",
            "country": "United States",
            "country_iso2": "US",
            "email": "janedoe@example.com"
          },
        "products": [{
            "name": "BigCommerce Poster",
            "quantity": 1,
            "price_inc_tax": 10.98,
            "price_ex_tax": 10
        },
        {
            "name": "BigCommerce Coffee Mug",
            "quantity": 1,
            "price_inc_tax": 50,
            "price_ex_tax": 45
        },]}
    """

    def create_an_order(self, user):
        data = {
            "customer_id": user.get("customer_id"),
            "billing_address": {
                "first_name": "Jane",
                "last_name": "Doe",
                "street_1": "123 Main Street",
                "city": "Austin",
                "state": "Texas",
                "zip": "78751",
                "country": "United States",
                "country_iso2": "US",
                "email": user.get('email')
            },
            "products": [{
                "name": "BigCommerce Poster",
                "quantity": 1,
                "price_inc_tax": 10.98,
                "price_ex_tax": 10
            }, {
                "name": "BigCommerce Coffee Mug",
                "quantity": 1,
                "price_inc_tax": 50,
                "price_ex_tax": 45}]}
        url = f"{self.base_url}/v2/orders"
        post_data = json.dumps(data)
        resp = self.session.post(url, headers=self.headers, data=post_data)
        if resp.status_code != 200 and resp.status_code != 201:
            return False
        return resp.json()
