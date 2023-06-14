from recognize import speak, command
import re
from twilio.rest import Client

account_sid = "YOUR'S ACCOUNT SID"
auth_token = "YOUR'S AUTH_TOKEN"


def msg_send():
    while True:
        speak("Please speak the number to whom you want to send the message")
        text = command.lower()
        num = re.findall(r'\d+', text)
        number = ''.join(num)
        number = number.replace(' ', '')
        if number.startswith("92"):
            number = "+" + number
        elif not number.startswith("+92"):
            number = "+92" + number

        if len(number) == 13:
            speak(f"Do you want to send a message to this number {number}")
            check = command.lower()
            if check == "yes" or check == "yeah":
                speak("what do you want to send")
                msg = command()

                client = Client(account_sid, auth_token)
                message = client.messages.create(
                body=msg,
                from_="+19593350437",
                to=number
                )
                speak("Message successfully sent")
                break
        else:
            speak(f"Phone Number is not correct : {number}")
