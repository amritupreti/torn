import gspread
from google.oauth2.service_account import Credentials
from users import get_users_from_html

enemies_data = get_users_from_html("enemies.html")
friends_data = get_users_from_html("friends.html")

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
]

credentials = Credentials.from_service_account_file("google.json", scopes=scopes)

client = gspread.authorize(credentials)

sheet_id = "12UXvtIx9fo6GiaMd_NVlJcDLcdp3TWVKWnXwyvfhSJE"
workbook = client.open_by_key(sheet_id)

sheets = set(map(lambda sheet: sheet.title, workbook.worksheets()))

# Create sheets ["Enemies", "Friends", "Traders"]
for sheet_name in ["Enemies", "Friends", "Traders"]:
    if sheet_name not in sheets:
        workbook.add_worksheet(title=sheet_name, rows=100, cols=20)

def add_enemies():
    # Add data to the "Enemies" sheet
    enemies = workbook.worksheet("Enemies")

    # Check if the header row is present
    if enemies.row_values(1) != ["ID", "Name", "Attack"]:
        enemies.insert_row(["ID", "Name", "Attack"], 1)
        # Make the header row bold
        enemies.format("A1:C1", {"textFormat": {"bold": True}})

    # Check if enemies_data is not empty
    if not enemies_data:
        print("No enemies data found")
        return

    # Insert enemies data if not already present
    existing_ids = set(enemies.col_values(1)[1:])  # Exclude the header row

    new_enemies_count = 0

    for enemy in enemies_data:
        if enemy["id"] not in existing_ids:
            new_enemies_count += 1
            enemies.append_row([enemy["id"], enemy["name"], enemy["attack"]])
        else:
            print(f"Enemy {enemy['name']} already present in the sheet")

    print(f"Added {new_enemies_count} new enemies to the 'Enemies' sheet")


def add_friends():
    # Add data to the "Friends" sheet
    friends = workbook.worksheet("Friends")

    # Check if the header row is present
    if friends.row_values(1) != ["ID", "Name", "Attack"]:
        friends.insert_row(["ID", "Name", "Attack"], 1)
        # Make the header row bold
        friends.format("A1:C1", {"textFormat": {"bold": True}})

    # Check if friends_data is not empty
    if not friends_data:
        print("No friends data found")
        return

    # Insert friends data if not already present
    existing_ids = set(friends.col_values(1)[1:])  # Exclude the header row

    new_friends_count = 0

    for friend in friends_data:
        if friend["id"] not in existing_ids:
            new_friends_count += 1
            friends.append_row([friend["id"], friend["name"], friend["attack"]])
        else:
            print(f"Friend {friend['name']} already present in the sheet")

    print(f"Added {new_friends_count} new friends to the 'Friends' sheet")


add_enemies()
add_friends()
