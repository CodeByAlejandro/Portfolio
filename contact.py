import os
from pathlib import Path
import smtplib
from email.message import EmailMessage
import csv
from enum import Enum, auto
from flask import Flask, render_template, request


class ContactMethod(Enum):
    SEND_EMAIL = auto()
    WRITE_TO_FILE = auto()
    WRITE_TO_CSV_FILE = auto()


class ContactHandler():

    def __init__(self,
        app: Flask,
        contact_method: ContactMethod = ContactMethod.SEND_EMAIL,
        filepath: str | None = None
    ) -> None:
        self.app = app
        self.contact_method = contact_method
        if self.contact_method is ContactMethod.WRITE_TO_FILE:
            if filepath is not None:
                self.filepath = filepath
            else:
                self.filepath = "database/text_database.txt"
        elif self.contact_method is ContactMethod.WRITE_TO_CSV_FILE:
            if filepath is not None:
                self.filepath = filepath
            else:
                self.filepath = "database/CSV_database.csv"
        else:
            self.filepath = None
        self.email = request.form["email"]
        self.subject = request.form["subject"]
        self.message = request.form["message"]

    def handle_contact(self) -> str:
        if self.contact_method is ContactMethod.SEND_EMAIL:
            return self._send_email()
        elif self.contact_method is ContactMethod.WRITE_TO_FILE:
            return self._write_to_text_File()
        elif self.contact_method is ContactMethod.WRITE_TO_CSV_FILE:
            return self._write_to_CSV_file()
        else:
            return self._send_email()

    def _send_email(self) -> str:
        send_result = None
        # Retrieve webmailer account password
        password = os.getenv("GOOGLE_APP_PASSWORD")
        if not password:
            send_result = False
            error_msg = "An error occurred while attempting to send mail: " + \
                        "Environmental variable 'GOOGLE_APP_PASSWORD' not set!"
            self.app.logger.error(error_msg)
            return render_template("contact.html", send_result=send_result)
        # Prepare email
        email = EmailMessage()
        email["from"] = "Webmailer <CodeByAlejandro@gmail.com>"
        email["to"] = "alejandrodegroote@outlook.com"
        email["cc"] = self.email
        email["subject"] = self.subject
        email.set_content(self.message)
        # Send email
        try:
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login('CodeByAlejandro', password)
                smtp.send_message(email)
        except Exception as e:
            send_result = False
            error_msg = "An error occurred while attempting to send mail: " + \
                        type(e).__module__ + "." + type(e).__name__ + ": " + \
                        str(e)
            self.app.logger.error(error_msg)
        else:
            send_result = True
            self.app.logger.info("Succesfully send mail for: " + request.form["email"])
        return render_template("contact.html", send_result=send_result)

    def _write_to_text_File(self) -> str:
        send_result = None
        if self.filepath is not None:
            try:
                Path(self.filepath).parent.mkdir(mode=0o755,
                                                 parents=True,
                                                 exist_ok=True)
            except Exception as e:
                send_result = False
                error_msg = "An error occurred while attempting to create " + \
                            "text database: " + \
                            type(e).__module__ + "." + type(e).__name__ + \
                            ": " + str(e)
                self.app.logger.error(error_msg)
                return render_template("contact.html", send_result=send_result)
            try:
                with open(self.filepath, "at", newline='') \
                as text_database:
                    text_database.write(
                        f"{self.email},{self.subject},{self.message}\n"
                    )
            except Exception as e:
                send_result = False
                error_msg = "An error occurred while attempting to write " + \
                            "to text database: " + \
                            type(e).__module__ + "." + type(e).__name__ + \
                            ": " + str(e)
                self.app.logger.error(error_msg)
            else:
                send_result = True
                self.app.logger.info("Succesfully wrote to text database: " + \
                                self.filepath)
            return render_template("contact.html", send_result=send_result)
        else:
            send_result = False
            error_msg = "An error occurred while attempting to create " + \
                        "text database: filepath is not defined!"
            self.app.logger.error(error_msg)
            return render_template("contact.html", send_result=send_result)


    def _write_to_CSV_file(self) -> str:
        send_result = None
        if self.filepath is not None:
            try:
                Path(self.filepath).parent.mkdir(mode=0o755,
                                                 parents=True,
                                                 exist_ok=True)
                if not Path(self.filepath).is_file():
                    with open(self.filepath, "wt") as csv_database:
                        csv.writer(csv_database).writerow(
                            ["email", "subject", "message"]
                        )
            except Exception as e:
                send_result = False
                error_msg = "An error occurred while attempting to create " + \
                            "CSV database: " + \
                            type(e).__module__ + "." + type(e).__name__ + \
                            ": " + str(e)
                self.app.logger.error(error_msg)
                return render_template("contact.html", send_result=send_result)
            try:
                with open(self.filepath, "at", newline='') \
                as csv_database:
                    csv.writer(csv_database).writerow(
                        [self.email, self.subject, self.message]
                    )
            except Exception as e:
                send_result = False
                error_msg = "An error occurred while attempting to write " + \
                            "to CSV database: " + \
                            type(e).__module__ + "." + type(e).__name__ + \
                            ": " + str(e)
                self.app.logger.error(error_msg)
            else:
                send_result = True
                self.app.logger.info("Succesfully wrote to CSV database: " + \
                                self.filepath)
            return render_template("contact.html", send_result=send_result)
        else:
            send_result = False
            error_msg = "An error occurred while attempting to create " + \
                        "CSV database: filepath is not defined!"
            self.app.logger.error(error_msg)
            return render_template("contact.html", send_result=send_result)
