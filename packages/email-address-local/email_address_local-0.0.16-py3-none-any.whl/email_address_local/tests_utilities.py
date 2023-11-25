from datetime import datetime


@staticmethod
def generic_email_generator(end):
    """ Creates a generic email adress by current date & time, end paremeter
        is to change the end of the email. for example if end = '' --> the end will be .com,
        if end = 1 --> .com1, if end = 2 --> .com2 ..."""
    return "email"+str(datetime.now())+f"@test.com{end}"
