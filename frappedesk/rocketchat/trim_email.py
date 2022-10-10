from talon.signature.bruteforce import extract_signature
import re

def remove_original_message(email_content):
    regex = r"(?s)^\s*\bOn\b.*\nwrote:.*$"
    subst = ""

    # You can manually specify the number of replacements by changing the 4th argument
    result = re.sub(regex, subst, email_content, 0, re.MULTILINE)

    if result:
        return result
    else:
        return email_content

# source : https://github.com/Trindaz/EFZP/blob/master/EFZP.py
def get_reply_text(email_text):
    #Notes on regex
    #Search for classic prefix from GMail and other mail clients "On May 16, 2011, Dave wrote:"
    #Search for prefix from outlook clients From: Some Person [some.person@domain.tld]
    #Search for prefix from outlook clients when used for sending to recipients in the same domain From: Some Person\nSent: 16/05/2011 22:42\nTo: Some Other Person
    #Search for prefix when message has been forwarded
    #Search for From: <email@domain.tld>\nTo: <email@domain.tld>\nDate:<email@domain.tld
    #Search for From:, To:, Sent:
    #Some clients use -*Original Message-*
    pattern = "(?P<reply_text>" + \
        "On ([a-zA-Z0-9, :/<>@\.\"\[\]]* wrote:.*)|" + \
        "From: [\w@ \.]* \[mailto:[\w\.]*@[\w\.]*\].*|" + \
        "From: [\w@ \.]*(\n|\r\n)+Sent: [\*\w@ \.,:/]*(\n|\r\n)+To:.*(\n|\r\n)+.*|" + \
        "[- ]*Forwarded by [\w@ \.,:/]*.*|" + \
        "From: [\w@ \.<>\-]*(\n|\r\n)To: [\w@ \.<>\-]*(\n|\r\n)Date: [\w@ \.<>\-:,]*\n.*|" + \
        "From: [\w@ \.<>\-]*(\n|\r\n)To: [\w@ \.<>\-]*(\n|\r\n)Sent: [\*\w@ \.,:/]*(\n|\r\n).*|" + \
        "From: [\w@ \.<>\-]*(\n|\r\n)To: [\w@ \.<>\-]*(\n|\r\n)Subject:.*|" + \
        "(-| )*Original Message(-| )*.*)"
    groups = re.search(pattern, email_text, re.IGNORECASE + re.DOTALL)
    reply_text = None
    if not groups is None:
        if 'reply_text' in groups.groupdict():
            reply_text = groups.groupdict()["reply_text"]
    return reply_text


def get_signature(email_text):

    #try not to have the signature be the very start of the message if we can avoid it
    salutation = get_salutation(email_text)
    if salutation: email_text = email_text[len(salutation):]

    #note - these openinged statements *must* be in lower case for
    #sig within sig searching to work later in this func
    sig_opening_statements = [
                              "warm regards",
                              "kind regards",
                              "regards",
                              "cheers",
                              "many thanks",
                              "thanks",
                              "sincerely",
                              "ciao",
                              "Best",
                              "bGIF",
                              "thank you",
                              "thankyou",
                              "talk soon",
                              "cordially",
                              "yours truly",
                              "thanking You",
                              "sent from my iphone"]
    pattern = "(?P<signature>(" + "|".join(sig_opening_statements) + ")(.)*)"
    groups = re.search(pattern, email_text, re.IGNORECASE + re.DOTALL)
    signature = None
    if groups:
        if "signature" in groups.groupdict():
            signature = groups.groupdict()["signature"]
            reply_text = get_reply_text(email_text[email_text.find(signature):])
            if reply_text: signature = signature.replace(reply_text, "")

            #search for a sig within current sig to lessen chance of accidentally stealing words from body
            tmp_sig = signature
            for s in sig_opening_statements:
                if tmp_sig.lower().find(s) == 0:
                    tmp_sig = tmp_sig[len(s):]
            groups = re.search(pattern, tmp_sig, re.IGNORECASE + re.DOTALL)
            if groups: signature = groups.groupdict()["signature"]

    #if no standard formatting has been provided (e.g. Regards, <name>),
    #try a probabilistic approach by looking for phone numbers, names etc. to derive sig
    if not signature:
        #body_without_sig = get_body(email_text, check_signature=False)
        pass

    #check to see if the entire body of the message has been 'stolen' by the signature. If so, return no sig so body can have it.
    body_without_sig = get_body(email_text, check_signature=False)
    if signature==body_without_sig: signature = None
    return signature


def get_salutation(email_text):
    #remove reply text fist (e.g. Thanks\nFrom: email@domain.tld causes salutation to consume start of reply_text
    reply_text = get_reply_text(email_text)
    if reply_text: email_text = email_text[:email_text.find(reply_text)]
    #Notes on regex:
    #Max of 5 words succeeding first Hi/To etc, otherwise is probably an entire sentence
    salutation_opening_statements = [
                                     "hi",
                                     "dear",
                                     "to",
                                     "hey",
                                     "hello",
                                     "thanks",
                                     "good morning",
                                     "good afternoon",
                                     "good evening"]
    pattern = "\s*(?P<salutation>(" + "|".join(salutation_opening_statements) + ")+(\s*\w*)(\s*\w*)(\s*\w*)(\s*\w*)(\s*\w*)[\.,\xe2:]+\s*)"
    groups = re.match(pattern, email_text, re.IGNORECASE)
    salutation = None
    if not groups is None:
        if "salutation" in groups.groupdict():
            salutation = groups.groupdict()["salutation"]
    return salutation

def get_body(email_text, check_salutation=True, check_signature=True, check_reply_text=True):

    if check_salutation:
        sal = get_salutation(email_text)
        if sal: email_text = email_text[len(sal):]

    if check_signature:
        sig = get_signature(email_text)
        if sig: email_text = email_text[:email_text.find(sig)]

    if check_reply_text:
        reply_text = get_reply_text(email_text)
        if reply_text: email_text = email_text[:email_text.find(reply_text)]
    return email_text


def extract_original_message(email_content):
    ## Using custom function to remove original message from email
    recent_message = remove_original_message(email_content)
    ## Using talon to remove signature from email
    text, signature = extract_signature(recent_message)
    ## Using custom function to remove original message from email
    recent_message = remove_original_message(get_body(text))
    return recent_message

