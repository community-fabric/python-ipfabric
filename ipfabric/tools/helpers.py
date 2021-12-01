def create_regex(string):
    regex = '^'
    upper_string = string.upper()
    for i in upper_string:
        if i.isalpha():
            regex += f"[{i}{i.lower()}]"
        else:
            regex += i
    regex += '$'
    return regex