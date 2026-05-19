from telethon.sync import TelegramClient
from telethon import functions

api_id = 123
api_hash = 'hash'

output_filename = "chats2.txt" # Output file
target_folder_name = "qqq"  # Folder name for parsing
usernames = []

with TelegramClient('session_name', api_id, api_hash) as client:
    folders_response = client(functions.messages.GetDialogFiltersRequest())
    filters = getattr(folders_response, 'filters', [])

    target_folder = None
    for folder in filters:
        if hasattr(folder, 'title'):
            folder_title = getattr(folder.title, 'text', None)
            if folder_title == target_folder_name:
                target_folder = folder
                break

    if not target_folder:
        print(f"Папка с названием '{target_folder_name}' не найдена.")  # Folder with [folder name] not found
        exit()

    dialogs = client.get_dialogs()

    included_peer_ids = set()
    for peer in target_folder.include_peers:
        peer_id = getattr(peer, 'channel_id', None) or getattr(peer, 'user_id', None) or getattr(peer, 'chat_id', None)
        if peer_id:
            included_peer_ids.add(peer_id)

    for dialog in dialogs:
        peer_id = getattr(dialog.entity, 'id', None)
        if peer_id in included_peer_ids:
            username = getattr(dialog.entity, 'username', None)
            if username:
                usernames.append(f"@{username}")

with open(output_filename, "w", encoding="utf-8") as f:
    f.write("chats = [\n")
    for username in usernames:
        f.write(f"\"{username}\",\n")
    f.write("]\n")

print(f"{len(usernames)} юзернеймов сохранено в {output_filename}") # OK! [num] usernames saved in [filename]
