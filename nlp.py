import re

def check_nlp_patterns(password):
    warnings = []
    
    # change password to small letters for easy matching
    lower_pass = password.lower()

    # try to read common words from file, otherwise use backup list
    forbidden_words = [] 
    try:
        with open('common_words.txt', 'r') as f:
            forbidden_words = f.read().splitlines()        
    except FileNotFoundError:
        forbidden_words = ['sarwat', 'admin', 'password', 'khan', 'ali', 'love', 'pakistan']

    # check if any common word exists inside the password
    for word in forbidden_words:
        if len(word) > 3 and word in lower_pass:
            warnings.append(f"Contains common name/word: '{word}'")
            break 

    # find years like 1990 or 2005 using regex pattern
    if re.search(r'(19|20)\d{2}', password):
        warnings.append("Contains birth year pattern (Predictable)")

    # check if password is less than 8 characters
    if len(password) < 8:
        warnings.append("Password is too short")

    # check if password contains only numbers
    if password.isdigit():
        warnings.append("Contains only numbers (Weak)")

    # send all found warnings back
    return warnings