import os

def join_path(path,folder_file):
    return os.path.join(path,folder_file)

def get_path():
    return os.getcwd()

def get_upload_path():
    return join_path(join_path(get_path(),"server"),"upload")

def get_templates_path():
    return join_path(join_path(get_path(),"server"),"templates")
