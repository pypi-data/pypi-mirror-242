import os


##Read files::
def ReadText(file_name):
    try:
        with open(file_name, 'r') as file:
            text_content = file.read()
        return text_content
    
    except FileNotFoundError:
        print(f"\nError: File doesn't exist at {file_name}\n")
        return None
    
    except Exception as e:
        print(f"\nError: An unexpected error occurred - {e}\n")
        return None
    
    
##Write files::
def WriteText(file_name, contents):
    try:
        with open(file_name, 'w') as file:
            file.write(contents)
        print(f"\nText written to {file_name}\n")
        
    except Exception as e:
        print(f"\nError: An unexcepted error occured, {e} \n")
        
        
##Update files::
def UpdateText(file_name, update_contents):
    try:
        with open(file_name, 'r') as file:
            exist_content = file.read()
            
        uploaded = exist_content + update_contents
        
        with open(file_name, 'w') as file:
            file.write(uploaded)
        print(f"\nText  successfully uploated in {file_name} \n")
    
    except Exception as e:
        print(f"\nError: An unexpected error occurred - {e}\n")
        
        
##Delete a files::
def DeleteFiles(file_name):
    try:
        os.remove(file_name)
        print(f"\nFile {file_name} successfully deleted.\n")
    
    except Exception as e:
        print(f"\nError: An unexpected error occurred - {e}\n")
        
        
##Create files::
def CreateFiles(file_name, create):
    try:
        with open(file_name, 'w') as file:
            file.write(create)
        print(f"File {file_name} successfully created.")
        
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
