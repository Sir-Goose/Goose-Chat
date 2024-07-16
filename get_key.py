def get_api_key():
    try:
        with open('key.txt', 'r') as file:
            api_key = file.read().strip()
        return api_key
    except FileNotFoundError:
        print(f"Error: The file was not found.")
        return None
    except IOError:
        print(f"Error: Unable to read the file'.")
        return None
