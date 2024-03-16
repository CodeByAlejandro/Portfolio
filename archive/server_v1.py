import logging
import os
import smtplib
from email.message import EmailMessage

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


### Routing ###
@app.route("/")
def index():
    return redirect(url_for("load_page", page="index"))


@app.route("/<string:page_name>")
def load_page(page_name):
    return render_template(f"{page_name}.html")


@app.post("/contact")
def contact_post():
    send_result = None

    # Validate if any form fields are missing
    send_result_msg = None
    if not request.form["email"]:
        send_result_msg = "Please provide your email address!"
    elif not request.form["subject"]:
        send_result_msg = "Please provide a subject!"
    elif not request.form["message"]:
        send_result_msg = "Please provide a meaningful message!"
    if send_result_msg is not None:
        send_result = False
        error_msg = "An error occurred while attempting to send mail: " + \
                    send_result_msg
        app.logger.error(error_msg)
        return render_template("contact.html",
                               send_result=send_result,
                               send_result_msg=send_result_msg)

    # Retrieve webmailer account password
    password = os.getenv("GOOGLE_APP_PASSWORD")
    if not password:
        send_result = False
        error_msg = "An error occurred while attempting to send mail: " + \
                    "Environmental variable 'GOOGLE_APP_PASSWORD' not set!"
        app.logger.error(error_msg)
        return render_template("contact.html", send_result=send_result)

    # Prepare email
    email = EmailMessage()
    email["from"] = "Webmailer <CodeByAlejandro@gmail.com>"
    email["to"] = "alejandrodegroote@outlook.com"
    email["cc"] = request.form["email"]
    email["subject"] = request.form["subject"]
    email.set_content(request.form["message"])

    # Send email
    try:
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('CodeByAlejandro', password)
            smtp.send_message(email)
        send_result = True
        app.logger.info("Succesfully send mail for: " + request.form["email"])
    except Exception as e:
        send_result = False
        error_msg = "An error occurred while attempting to send mail: " + \
                    type(e).__module__ + "." + type(e).__name__ + ": " + \
                    str(e)
        app.logger.error(error_msg)
    return render_template("contact.html", send_result=send_result)


### Configuration ###
def configureLogger():
    # Remove the default handler for the Flask logger
    # app.logger.removeHandler(app.logger.handlers[0])

    # Create a file handler
    file_handler = logging.FileHandler("flask.log")
    file_handler.setLevel(logging.INFO)

    # Create a formatter and set it for the file handler
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the Flask logger
    app.logger.addHandler(file_handler)


### Run server initialization here ###
configureLogger()
