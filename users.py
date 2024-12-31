from bs4 import BeautifulSoup

def get_users_from_html(html_file):
        # Parse the HTML file
    try :
        with open(html_file, "r") as file:
            soup = BeautifulSoup(file, "html.parser")
    except FileNotFoundError:
        print(f"File {html_file} not found")
        return []

    # Find all user elements
    users = []

    for li in soup.find_all("li", {"data-id": True}):
        # Extract user ID from the href attribute
        user_link = li.find("a", {"class": "user name"})
        if user_link and "href" in user_link.attrs:
            href = user_link["href"]
            # Extract the XID from the URL (e.g., XID=105045)
            user_id = href.split("XID=")[-1]
        else:
            user_id = None

        # Extract username
        user_name = user_link.text.strip() if user_link else None

        if user_id and user_name:
            users.append({"id": user_id, "name": user_name, "attack": f"https://www.torn.com/loader.php?sid=attack&user2ID={user_id}"})

    return users