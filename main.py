from datetime import datetime, date, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import qrcode
import assests.data as data
import re
import os

# from .assests import data
today_date = date.today()
now = datetime.now()


# ---------------------------------------------------------------------------------------------------
term_days = data.TERM_DAYS
company_name = data.COMPANY_NAME
web_site = data.WEB_SITE
company_address = data.COMPANY_ADDRESS
to_address = data.CUSTOMER_ADDRESS
customer_name = data.CUSTOMER_NAME
customer_phone = data.CUSTOMER_PHONE
invoice_number = data.INVOICE_NUMBER
to_address = (re.sub("(.{35})", "\\1\n", to_address, 0, re.DOTALL))
upi_id = data.UPI_ID
# ---------------------------------------------------------------------------------------------------

current_time = now.strftime("%H:%M")
current_date = today_date.strftime("%b %d, %Y")
due_date = (today_date + timedelta(days=data.TERM_DAYS)).strftime("%b %d, %Y")


pdfmetrics.registerFont(
    TTFont('GreatVibes-Regular', 'assests/GreatVibes-Regular.ttf'))  # Thank-you
# pdfmetrics.registerFont(TTFont('nutellaBold', 'nutellaBold.ttf')) #INVOICE

w, h = A4
invoice_number = f"#-{data.INVOICE_NUMBER}"


both_side_margin = 60
right_side = w-both_side_margin
left_side = w-(w-both_side_margin)
centre = w/2

top_bottom_margin = 20
top = h - top_bottom_margin
bottom = h - (h-top_bottom_margin)

c = canvas.Canvas('invoice.pdf', pagesize=A4)
c.setTitle = "Invoice"
c.setAuthor = "By_Replit"

def home():

    def top_section():
        """
        pass
        """
        c.setFillColor('black')
        # c.setFont("nutellaBold", 10)
        c.setFont("Helvetica-Bold", 8)
        c.drawRightString(right_side-40, 720, invoice_number)

        c.drawImage("assests/invoice_logo.jpg",
                    left_side, 750, width=130, height=50)
        c.drawImage("assests/happy_shop.jpg", 430, 730,
                    width=90, height=80)  # shop-logo

        c.setFont("Helvetica-Bold", 10)
        # c.drawString(left_side, 600, "Bill To: ")
        c.drawString(left_side, 650, "Bill To: ")
        slight_left = 360
        c.drawString(slight_left, 650, "Invoice Date: ")
        c.drawString(slight_left, 620, "Terms: ")
        c.drawString(slight_left, 590, "Due Date: ")

        # Bill_to_address
        c.setFont("Helvetica-Bold", 10)
        c.drawString(left_side+40, 650, data.CUSTOMER_NAME)
        c.drawString(left_side, 635, str(data.CUSTOMER_PHONE))

        c.setFont("Helvetica", 10)
        text = c.beginText(left_side, 620)
        text.textLines(to_address)
        c.drawText(text)

        # Invoice Date
        c.drawRightString(right_side, 650, current_date)
        # Terms
        c.drawRightString(right_side, 620, f"{str(data.TERM_DAYS)} Days")
        # Due Date:
        c.drawRightString(right_side, 590, due_date)


    top_section()

    # Description_section
    up_side_inc = 50
    c.line(left_side, 500+up_side_inc, right_side, 500+up_side_inc)
    c.line(left_side, 475+up_side_inc, right_side, 475+up_side_inc)

    c.drawString(left_side+20, 485+up_side_inc, "ITEM DESCRIPTION")
    c.drawCentredString(left_side+250+20, 485+up_side_inc, "PRICE")
    c.drawCentredString(left_side+336+20, 485+up_side_inc, "QTY")
    c.drawCentredString(left_side+415+20, 485+up_side_inc, "TOTAL")


    item_down = 15
    downward = 455+up_side_inc

    counter = 0
    pointer = 0
    total_price = 0
    next_index = 1
    Sr_No = 1
    next_page_list = [28, 28*2, 28*3, 28*4, 28*5, 28*6, 28*7, 28*8, 28*9, 28*10]

    for item in data.ITEMS:
        down = downward-(item_down*counter)
        # ITEM_DESCRIPTION
        c.drawString(left_side + 20, down, f"{Sr_No} - {item[0]}")
        c.drawCentredString(left_side + 270, down, f"{item[1]}")  # PRICE
        c.drawCentredString(left_side + 356, down, f"{item[2]}")  # QTY
        c.drawCentredString(left_side + 435, down, f"{item[1]*item[2]}")  # TOTAL
        total_price = total_price+(item[1]*item[2])
        counter += 1
        next_index += 1
        Sr_No += 1
        pointer = down
        current_page_number = c.getPageNumber()
        c.setFont("Helvetica", 10)
        c.drawRightString(right_side+10, bottom, str(current_page_number))

        if next_index in next_page_list:
            # bottom Section
            c.setFont("GreatVibes-Regular", 30)
            c.drawCentredString(w/2, 60, "Thank you")
            c.setFont("Helvetica", 10)
            c.line(left_side, bottom+25, right_side, bottom+25)
            c.drawCentredString(w/2, bottom, data.COMPANY_ADDRESS)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(w/2, bottom+12, data.WEB_SITE)

            c.showPage()
            top_section()
            up_side_inc = 50
            c.line(left_side, 500+up_side_inc, right_side, 500+up_side_inc)
            c.line(left_side, 475+up_side_inc, right_side, 475+up_side_inc)

            c.drawString(left_side+20, 485+up_side_inc, "ITEM DESCRIPTION")
            c.drawCentredString(left_side+250+20, 485+up_side_inc, "PRICE")
            c.drawCentredString(left_side+336+20, 485+up_side_inc, "QTY")
            c.drawCentredString(left_side+415+20, 485+up_side_inc, "TOTAL")
            counter = 0

    c.line(left_side, pointer-10, right_side, pointer-10)


    # Bill Calculation
    vat_rate = 18
    discount_rate = 10

    vat = (total_price % vat_rate)
    discount = ((total_price % discount_rate))
    grand_total = (total_price+vat)-discount

    vat = (f"{vat:.2f}")
    discount = (f"{discount:.2f}")


    # bill
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_side+310, pointer-25, "SUB TOTAL")
    c.drawRightString(right_side-25, pointer-25, f"{total_price}")
    c.setFont("Helvetica", 10)
    c.drawString(left_side+310, pointer-40, "Vat 18%")
    c.drawRightString(right_side-25, pointer-40, vat)
    c.drawString(left_side+310, pointer-55, "Discount 10%")
    c.drawRightString(right_side-25, pointer-55, discount)
    c.line(350, pointer-60, right_side, pointer-60)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_side+310, pointer-75, "Grand Total")
    c.drawRightString(right_side-25, pointer-75, str(grand_total))


    # Signature
    c.drawRightString(right_side-5, pointer-145, data.ACCOUNTANT)
    c.setFont("Helvetica", 10)
    c.drawRightString(right_side-5, pointer-155, data.ACCOUNTANT_POSTION)
    c.rect(left_side+345, pointer-160, 130, 60)


    # Payment method
    img = qrcode.make(upi_id)
    img.save(f"qr-{today_date}-{current_time}.png")
    qr_code = f"qr-{today_date}-{current_time}.png"
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_side, pointer-30, "Payment Method")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_side, pointer-45, "Payment:")
    c.drawString(left_side, pointer-60, "UPI:")

    c.drawString(left_side, pointer-75, "QR CODE:")
    c.setFont("Helvetica", 10)
    c.drawString(left_side+50, pointer-45, "Visa, MasterCard, Cheque")
    c.drawString(left_side+25, pointer-60, data.UPI_ID)
    c.drawImage(qr_code, left_side, pointer-160, width=80, height=80)  # QR-CODE


    # BOTTOM SECTION
    c.setFont("GreatVibes-Regular", 30)
    c.drawCentredString(w/2, 60, "Thank you")

    c.setFont("Helvetica", 10)
    c.line(left_side, bottom+25, right_side, bottom+25)
    c.drawCentredString(w/2, bottom, data.COMPANY_ADDRESS)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(w/2, bottom+12, data.WEB_SITE)

    c.save()
    os.remove(f"{qr_code}")
    print("Saved!")

if __name__=="__main__":
    home()