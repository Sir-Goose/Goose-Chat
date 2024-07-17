def get_api_key():
    try:
        with open('key.txt', 'r') as file:
            api_key = file.read().strip()
        return api_key
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file key.txt was not found.") from None
    except IOError:
        raise IOError("Error: Unable to read the file key.txt.") from None
