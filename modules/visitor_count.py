import os

def get_visitor_count():
    file_path = os.path.join("data", "visitor_count.txt")
    if not os.path.exists(file_path):
        with open(file_path,"w") as f:
            f.write("0")

    with open(file_path,"r") as f:
        count = int(f.read().strip())

    return count

def increment_visitor_count():
    file_path = os.path.join("data", "visitor_count.txt")
    count = get_visitor_count() + 1

    with open(file_path, "w") as f:
        f.write(str(count))

    return count