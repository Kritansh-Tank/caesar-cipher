import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QEvent, QObject
import smtplib
from email.mime.text import MIMEText

app = QApplication(sys.argv)

# Styling customization
app.setStyleSheet("""
    QWidget {
        background-color: #202528; 
        color: #EEEEEE;
        font-family: Arial;
    }
    QPushButton {
        background-color: #50C878; 
        border: none;
        padding: 10px 20px;
        font-size: 14px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #45A065; 
    }
    QLineEdit {
        padding: 8px;
        border: 1px solid #444;
        border-radius: 4px;
    }
""")


def center_window(window):
    screen_geometry = app.desktop().availableGeometry()  # Get screen dimensions
    window_geometry = window.frameGeometry()           # Get window dimensions

    # Calculate center coordinates
    x = (screen_geometry.width() - window_geometry.width()) // 2
    y = (screen_geometry.height() - window_geometry.height()) // 2

    # Center the window
    window.setGeometry(x, y, window_geometry.width(), window_geometry.height())


# Window setup
window = QWidget()
window.setWindowTitle("CNS PBL")
window.setContentsMargins(0, 15, 0, 0)
layout = QVBoxLayout()

# Top label
title_label = QLabel("Caesar Cipher Decryption")
title_label.setFont(QFont("Arial", 18, weight=QFont.Bold))
title_label.setAlignment(Qt.AlignCenter)
layout.addWidget(title_label)


def share_email():
    # The email addresses
    sender_email = ""  # Your sender email address
    receiver_email = ""  # Your receiver email address
    password = ""  # Your SMTP password

    # The email content
    subject = "Message"
    body = f"Received"
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Use your SMTP server
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")


share_button = QPushButton("Acknowledge")
share_button.clicked.connect(share_email)
share_button.setFixedWidth(100)
layout.addSpacing(35)
layout.addWidget(share_button, alignment=Qt.AlignCenter)

# Textboxes
textbox1 = QLineEdit()
textbox1.setPlaceholderText("Enter Encrypted Text")
textbox1.setFixedWidth(300)
textbox1.setContentsMargins(0, 25, 0, 0)
layout.addWidget(textbox1, alignment=Qt.AlignCenter)

def decrypt_text():
    encrypt_text = textbox1.text()

    if not 1 <= len(encrypt_text) <= 50:
        show_error_message("Invalid Text Value!")

    decrypted_output = caesar_decipher(encrypt_text)
    textbox3.setText(decrypted_output)


def caesar_decipher(text):
    result = ""

    for char in text:
        if char.isupper():
            new_ord = (ord(char) - 3 - 65) % 26 + 65
            result += chr(new_ord)
        elif char.islower():
            new_ord = (ord(char) - 3 - 97) % 26 + 97
            result += chr(new_ord)
        else:
            # Keep spaces and other non-alphabetic characters as they are
            result += char

    return result


def show_error_message(message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Error")
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Critical)  # Error icon
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()  # Display the message box


# Button
decrypt_button = QPushButton("Decrypt")
decrypt_button.clicked.connect(decrypt_text)
decrypt_button.setFixedWidth(100)
layout.addSpacing(35)
layout.addWidget(decrypt_button, alignment=Qt.AlignCenter)

textbox3 = QLineEdit()
textbox3.setReadOnly(True)
textbox3.setFixedWidth(300)
textbox3.setContentsMargins(0, 5, 0, 0)
layout.addWidget(textbox3, alignment=Qt.AlignCenter)

# Spacer for better visual spacing
layout.addStretch(1)

window.setLayout(layout)
center_window(window)
window.show()
app.exec()
