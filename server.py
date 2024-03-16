import logging

from flask import Flask, redirect, render_template, request, url_for
from contact import ContactMethod, ContactHandler

app = Flask(__name__)


### Routing ###
@app.route("/")
def index():
    return redirect(url_for("load_page", page_name="index"))


@app.route("/<string:page_name>")
def load_page(page_name):
    return render_template(f"{page_name}.html")


@app.post("/contact")
def contact_post():
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
        error_msg = "An error occurred while attempting to " + \
                    "handle contact post: " + send_result_msg
        app.logger.error(error_msg)
        return render_template("contact.html",
                               send_result=send_result,
                               send_result_msg=send_result_msg)
    else:
        return ContactHandler(app,ContactMethod.SEND_EMAIL).handle_contact()


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
