#Yoyo Python API Test

##The Setup
You are building the API for a simple Python/Django-based loyalty programme for a retail shop.

- the shop sells two products: a widget and a gizmo
- for each widget you buy, you earn one loyalty stamp
- for each gizmo you buy, you do not earn a loyalty stamp
- you can buy multiple products in a single transaction
- if you earn ten loyalty stamps you automatically earn a voucher for a free widget
- when you earn a voucher for a free widget, your widget loyalty stamps balance resets
- you can only use a voucher once

##The Test

Create a set of REST APIs that allow you to:

- see how many stamps a customer has
- see how many vouchers a customer has
- add stamps to a customer
- add vouchers to a customer
- mark a voucher as redeemed
- __*BONUS: return a customers transaction history (purchases, stamps, vouchers)*__

##What We Expect
It is expected that you:

- create your own data models
- either stub data or create and connect to a real database (it's free on Heroku!)
- write unit tests
- commit often
- deploy on Heroku
- provide basic api documentation in the project

##Afterwards
When complete, send us the urls of the Heroku application and git repository.
