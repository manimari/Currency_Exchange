# Currency_Exchange 

API for Currency Exchange Rates 
________________________

Instructions : 

You should download the files. 

You should complete the API_KEY and the SECRET_KEY at the .env file. 

Requests can be done in any way, but if you don't know I suggest Postman.

________________________ 

________________________

The task is to implement an API that will have retrieve, store and expose currency exchange rates. 

All endpoints use the database currency.db. 

We have the following end points : 

________________________ 

- POST - /users/register (No Auth needed) 

This endpoint accepts username, password, confirmPassword in JSON format.
After validating the input it creates and persists a user in the DB. 

________________________ 

- POST - /users/login (No Auth needed) 

This endpoint accepts username, password in JSON format.
After validating the input and checking that user exists and password is correct, a Json Web Token (JWT) is returned, that should be used to communicate with the other 2 endpoints of the API. 

________________________ 

- POST - /rates/seed (Needs Authentication) 

This endpoint uses a free currency API, https://freecurrencyapi.net/.
Keep in mind that you will need to potentially register with this API to use it and also respect potential request rate limits. 

When called it retrieves the exchange rates for all currencies with EUR, USD, CHF and GBP as base currency respectively. 

e.g.
{base: EUR, currencies: [{ EUR: 1, USD: 0.86, CAD: 1.23, SGD: 2.7 ... }} // Base EUR
{base: USD, currencies: [{ EUR: 1.23, USD: 1, CAD: 0.67, SGD: 8.2 ... }} // Base USD
.... 

The exchange rates are then persisted in the database. 

________________________ 

- GET - /rates/{base} (Needs Authentication) 

This endpoint returns all exchange rate from the database. If wanted, it can support sorting alphabetically or by exchange rate, by uncomment the respective query in the function get_exchange(database_file_name, base). 

________________________ 

- GET - /rates/{base}/{target} (Needs Authentication) 

The particular exchange rate is returned. 

________________________ 

- POST - /rates/{base}/{target} (Needs Authentication) 

The particular exchange rate is created / updated. 



