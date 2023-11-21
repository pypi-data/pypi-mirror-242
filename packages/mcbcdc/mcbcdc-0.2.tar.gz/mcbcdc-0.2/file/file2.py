
def read_file(file_name):
    file_path = f'data/{file_name}'
    with open(file_path, 'r') as file:
        content = file.read()
    return content
