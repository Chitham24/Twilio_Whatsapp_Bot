def log_to_file(message):
    with open("message_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{message}\n")