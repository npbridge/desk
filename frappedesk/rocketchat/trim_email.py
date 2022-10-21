from talon.signature.bruteforce import extract_signature
import re


def remove_original_message(email_content):
    #regex = r"(?s)^\s*\bOn\b.*\nwrote:.*$"
    regex = r"(?s)^\s*\bOn\b.*wrote:.*"
    subst = ""

    # You can manually specify the number of replacements by changing the 4th argument
    result = re.sub(regex, subst, email_content, 0, re.MULTILINE)

    if result:
        return result
    else:
        return email_content


def get_reply_text(email_text):
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
    sig_opening_statements = [
                              "warm regards",
                              "kind regards",
                              "regards",
                              "cheers",
                              "many thanks",
                              "thanks",
                              "sincerely",
                              "best",
                              "thank you",
                              "thankyou",
                              "talk soon",
                              "cordially",
                              "yours truly",
                              "thanking You",
                              "sent from my iphone",
                              "thanks & regards"]

    pattern = "(?P<signature>(" + "|".join(sig_opening_statements) + ")(.)*)"
    groups = re.search(pattern, email_text, re.IGNORECASE + re.DOTALL)
    signature = None
    if groups:
        if "signature" in groups.groupdict():
            signature = groups.groupdict()["signature"]
    return signature


def get_salutation(email_text):
    # Max of 5 words succeeding first Hi/To etc, otherwise is probably an entire sentence
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

    if check_reply_text:
        reply_text = get_reply_text(email_text)
        if reply_text:
            email_text = email_text[:email_text.find(reply_text)]

    if check_salutation:
        sal = get_salutation(email_text)
        if sal:
            email_text = email_text[len(sal):]

    if check_signature:
        sig = get_signature(email_text)
        if sig:
            email_text = email_text[:email_text.find(sig)]

    return email_text


def remove_html_tags(text):
    ## preserving line changes
    text = re.sub(r'<br>', '__br__', text)
    ## removing all html tags
    text = re.sub('<[^<]+?>', ' ', text)
    ## replacing __br__ with \n (new line)
    text = text.replace('__br__', '\n').strip()
    ## removing extra spaces
    text = re.sub(' +', ' ', text)
    return text


def extract_original_message(email_content):
    ## Using custom function to remove original message from email
    last_cleaned_message = email_content
    recent_message = ""

    if email_content:
        # removing html tags
        recent_message = remove_html_tags(email_content)

        if len(recent_message) > 256:
            # removing reply text
            last_cleaned_message = recent_message
            recent_message = remove_original_message(recent_message)

        if len(recent_message) > 256:
            ## Using talon to remove signature from email
            last_cleaned_message = recent_message
            recent_message, signature = extract_signature(recent_message)

        ## Using custom function to remove original message from email
        if len(recent_message) > 256:
            # removing signature and salutation
            last_cleaned_message = recent_message
            recent_message = get_body(recent_message)

        if recent_message:
            last_cleaned_message = recent_message

    return last_cleaned_message
    # we can handle empty body here: target to a specific intent for empty body
    #else:
    #    return "Empty Intent Trigger Message"