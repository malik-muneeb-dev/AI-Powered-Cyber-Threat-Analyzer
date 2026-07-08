def calculate_crack_time(password):
    #total no of characters that can generate password
    pool_size = 0
    if any(c.islower() for c in password): pool_size += 26  
    if any(c.isupper() for c in password): pool_size += 26  
    if any(c.isdigit() for c in password): pool_size += 10  
    if any(c in "!@#$%^&*()-_=+[]{};:,.<>?/|" for c in password): pool_size += 32 

    # Prevent calculation errors if the password contains unknown characters
    if pool_size == 0: pool_size = 1

    # Calculate Total Combinations: Formula = Pool_Size ^ Password_Length
    total_combinations = pool_size ** len(password)

    # Define hacking speeds (Guesses per Second) for different hardware scenarios
    speed_cpu = 100_000_000              # 100 Million/sec 
    speed_gpu = 100_000_000_000          # 100 Billion/sec 
    speed_cluster = 100_000_000_000_000  # 100 Trillion/sec 

    # Calculate Time required 
    time_cpu = total_combinations / speed_cpu
    time_gpu = total_combinations / speed_gpu
    time_cluster = total_combinations / speed_cluster

    return {
        "cpu": format_time(time_cpu),
        "gpu": format_time(time_gpu),
        "cluster": format_time(time_cluster),
        # Calculate a score (0-100) based on GPU time for the meter display
        "score_100": min(int(time_gpu / 10000), 100) 
    }

def format_time(seconds):
   
    #convert raw seconds into human-readable formats 

    if seconds < 1: 
        return "Ins"        # Instant
    if seconds < 60:
        return f"{int(seconds)} sec"
    if seconds < 3600:
        return f"{int(seconds/60)} min"        # 1 Hour = 3600 sec
    if seconds < 86400:
        return f"{int(seconds/3600)} hrs"     # 1 Day = 86400 sec
    if seconds < 31536000:
        return f"{int(seconds/86400)} days" # 1 Year approx 31.5M sec
    if seconds < 3153600000:
        return f"{int(seconds/31536000)} years"
    
    return "Centuries"