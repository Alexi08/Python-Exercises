import requests
from bs4 import BeautifulSoup
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

headers = """Place internet access user agent here"""


def send_email(information):
    sender_email = """Email Username Here"""
    password = """Email Password Here"""
    receiver_email = """Receiver Email Username Here"""

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Test Email"


    body = (
        f"Here are the new listings.\nParameters are:\n- Predetermined area\n- Maximum rent of £1200\n- Minimum 2 beds\n- Must be a house(detateched, semi-detached, terrace or bungalo)\n")
    for item in information.items():
        string = item[0]
        string2 = item[1]
        result = " ".join([string, string2])
        body = "\n".join([body, result])
    message.attach(MIMEText(body, 'plain'))


    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print('Email sent successfully!')



def write_to_text(dictionary):
    with open('properties', 'r') as file:
        existing_keys = set(line.strip().split(':')[0] for line in file)
    values_to_send = {}
    with open('properties', 'a') as file:
        for key, value in dictionary.items():
            if key not in existing_keys:
                values_to_send[key] = value
                file.write(f'{key}: {value}\n')
                print("Key was NOT detected, will upload and write to txt file")
            elif key in existing_keys:
                print("Key was already detected")

    if not values_to_send == {}:
        send_email(values_to_send)
    elif values_to_send == {}:
        print("No values to email")


def get_property_info(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    property_listings = soup.find_all(class_='l-searchResult is-list')


    rightmove_base_url = "https://www.rightmove.co.uk"

    titles = []
    links = []
    for listing in property_listings:
        title_element = listing.find(class_='propertyCard-address')
        if title_element:
            titles.append(title_element.text.strip())
        link_to_site = listing.find('a', class_='propertyCard-priceLink propertyCard-rentalPrice')
        if link_to_site:
            href_tag = link_to_site["href"]
            final_link = "".join([rightmove_base_url, href_tag])
            links.append(final_link)

    properties = {}
    if len(titles) == len(links):
        for number in range(len(titles)):
            properties[titles[number]] = links[number]

    return properties


# Example usage
url = """Place URL for rightmove with pre-configured searches. Example URL:
         https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87508&maxBedrooms=2&maxPrice=5000&propertyTypes=detached%2Cpark-home%2Csemi-detached%2Cterraced&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="""
property_info = get_property_info(url)
write_to_text(property_info)
