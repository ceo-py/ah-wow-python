import os

def get_realms_with_character(wow_directory: str) -> list:
    realms_with_character = []
    for realm in os.listdir(wow_directory):
        realm_path = os.path.join(wow_directory, realm)
        if os.path.isdir(realm_path):
            realms_with_character.append(realm)

    return [c.replace("'","").replace(" ", "-").lower() for c in realms_with_character]

