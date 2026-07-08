import random
import string

def generate_strong_passwords(text):
    
    # Input Validation: 
    if not text:
        text = "Secure"

    passwords_list = []

    # STYLE 1:
    # Convert to lowercase and replace common characters with look-alike symbols
    style1 = text.lower()
    style1 = style1.replace("a", "@")
    style1 = style1.replace("s", "$")
    style1 = style1.replace("i", "!")
    style1 = style1.replace("o", "0")
    
    # Append a random 2-digit number (10-99) and a hash symbol for extra security
    random_num = random.randint(10, 99)
    style1 = style1 + str(random_num) + "#"
    passwords_list.append(style1)


    # STYLE 2
    # Capitalize the first letter for readability
    random_abc = ""
    
    for i in range(3): 
        random_abc += random.choice(string.ascii_letters)
    
    # Combine:
    style2 = text.capitalize() + "@" + random_abc
    passwords_list.append(style2)


    # STYLE 3:
    # Use Uppercase text combined with a larger number and random symbol
    random_num_big = random.randint(100, 999) 
    random_sym = random.choice("!@#$%")       
    
    # Use f-string to format the final password 
    style3 = f"{text.upper()}_{random_num_big}{random_sym}"
    passwords_list.append(style3)

    return passwords_list