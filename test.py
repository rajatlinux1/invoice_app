import json

# Opening JSON file
f = open('data.json')

# returns JSON object as
# a dictionary

data = json.load(f)


print("CUSTOMER_NAME == ",data["CUSTOMER_NAME"])
print("CUSTOMER_ADDRESS == ",data["CUSTOMER_ADDRESS"])
print("CUSTOMER_PHONE == ",data["CUSTOMER_PHONE"])
print("TERM_DAYS == ",data["TERM_DAYS"])
print("COMPANY_NAME == ",data["COMPANY_NAME"])
print("WEB_SITE == ",data["WEB_SITE"])
print("COMPANY_ADDRESS == ",data["COMPANY_ADDRESS"])
print("INVOICE_NUMBER == ",data["INVOICE_NUMBER"])
print("UPI_ID == ",data["UPI_ID"])
print("CASHIER_NAME == ",data["CASHIER_NAME"])
print("AMOUNT_IN_WORK == ",data["AMOUNT_IN_WORK"], end=" ONLY")

for i in data["DATA"]:
    print("LOOP", i[0], i[1], i[2])

# Closing file
f.close()