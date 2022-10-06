from talon.signature.bruteforce import extract_signature
import re

def remove_original_message(email_content):
    regex = r"(?s)^\s*\bOn\b.*\nwrote:.*$"
    subst = ""

    # You can manually specify the number of replacements by changing the 4th argument
    result = re.sub(regex, subst, email_content, 0, re.MULTILINE)

    if result:
        return result

def extract_original_message(email_content):
    ## Using custom function to remove original message from email
    recent_message = remove_original_message(email_content)
    ## Using talon to remove signature from email
    text, signature = extract_signature(recent_message)
    ## Using custom function to remove original message from email
    recent_message = remove_original_message(text)
    return recent_message

