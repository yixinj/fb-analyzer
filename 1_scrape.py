def convert_html_to_soup(path):
    """
    Converts an HTML file to a BeautifulSoup object (so one conversation)
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(open(path, encoding="utf-8"), "html.parser")
    return soup


def clean_soup(soup):
    """
    Extracts all messages (and conversation headers in the case of group conversations) from the conversation
    """
    all_messages = soup.findAll("div", {"class": "pam"})
    # FIXME: Delete first message for lazy solution to group conversations
    all_messages.pop(0)
    return all_messages


def preprocess_raw_html(path):
    """
    Preprocesses raw HTML to a series of messages
    """
    return clean_soup(convert_html_to_soup(path))


def get_all_paths():
    import os
    PATH_TO_INBOX = 'inbox'
    # All folders in inbox
    ALL_FOLDERS = [
        os.path.join(PATH_TO_INBOX, o) for o in os.listdir(PATH_TO_INBOX)
        if os.path.isdir(os.path.join(PATH_TO_INBOX, o))
    ]
    APPEND_TO_PATH = "\message_1.html"
    ALL_PATHS = [path + APPEND_TO_PATH for path in ALL_FOLDERS]
    return ALL_PATHS


def test(path, save_file_name):
    messages = preprocess_raw_html(path)

    import csv
    with open("csv/" + save_file_name + '.csv', mode='w') as file:
        message_writer = csv.writer(file,
                                    delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
        for i in messages:
            l = i.findAll("div")
            try:
                sender = l[0].contents[0]
                message = l[4].contents[0]
                timestamp = l[7].contents[0]
                message_writer.writerow([sender, message, timestamp])
            except:
                pass

    # l = messages[1].findAll("div")
    # sender = l[0].contents[0]
    # message = l[4].contents[0]
    # timestamp = l[7].contents[0]
    # print(sender, message, timestamp)


def big_test():
    count = 0
    ALL_PATHS = get_all_paths()
    print("total number of conversations:", len(ALL_PATHS))
    for path in ALL_PATHS[0:5]:
        messages = preprocess_raw_html(path)
        count += len(messages)
    print("total messages in selected conversations:", count)


def search_path(query):
    import re
    ALL_PATHS = get_all_paths()
    r = re.compile(query)
    l = list(filter(r.match, ALL_PATHS))  # Read Note
    return (l)


test(search_path(".*FirstLast")[0], "Initials")
