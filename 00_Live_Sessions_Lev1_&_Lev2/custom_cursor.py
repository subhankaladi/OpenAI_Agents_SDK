
# from agents import Agent, Runner, function_tool
# from dotenv import load_dotenv

# load_dotenv()

# @function_tool(strict_mode=True)
# def create_files_and_folders(file_name:str = None, folder_name:str = None):
#     pass


# main_agent = Agent(
#     name="Assistant",
#     instructions="you are helpful assistant.",
#     tools=[create_files_and_folders]
# )

# result = Runner.run_sync(
#     main_agent,
#     "hello",
# )

# print(result.final_output)





from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import os

load_dotenv()


# # Test kar ke dekho
# with open("test.txt", "w", encoding="utf-8") as f:
#     f.write("Hello سلام 🚀")

# with open("test.txt", "r", encoding="utf-8") as f:
#     print(f.read())  # Probably works fine!


@function_tool(strict_mode=True)
def create_files_and_folders(
    file_name: str = None, 
    folder_name: str = None, 
    content: str = None,
    file_path: str = None
):
    """
    Creates files and folders with optional content
    
    Args:
        file_name: Name of file to create (with extension)
        folder_name: Name of folder to create
        content: Content to add to the file
        file_path: Full path including filename for existing files
    """
    try:
        result_messages = []
        
        # Create folder if specified
        if folder_name:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                result_messages.append(f"Folder '{folder_name}' created successfully")
            else:
                result_messages.append(f"Folder '{folder_name}' already exists")
        
        # Create file if specified
        if file_name:
            # If folder is specified, create file inside that folder
            if folder_name:
                full_path = os.path.join(folder_name, file_name)
            else:
                full_path = file_name
            
            with open(full_path, 'w', encoding='utf-8') as f:
                if content:
                    f.write(content)
                else:
                    f.write("")  # Create empty file
            
            result_messages.append(f"File '{full_path}' created successfully")
            
            if content:
                result_messages.append(f"Content added to '{full_path}'")
        
        # Add content to existing file if file_path is specified
        elif file_path and content:
            if os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                result_messages.append(f"Content updated in existing file '{file_path}'")
            else:
                result_messages.append(f"File '{file_path}' does not exist")
        
        return "\n".join(result_messages)
        
    except Exception as e:
        return f"Error: {str(e)}"



main_agent = Agent(
    name="File Assistant",
    instructions="""You are a helpful file management assistant. You can:
    
    1. Create files and folders
    2. Add content to files (including HTML, CSS, JavaScript, Python, etc.)
    3. Update existing files with new content
    
    When user asks for HTML files (like todolist), you should generate appropriate HTML, CSS, and JavaScript code yourself. Be creative and make functional, beautiful interfaces.
    
    Examples of what you can do:
    - "create file todo.html with todolist code" - Generate complete HTML todolist with styling
    - "create folder 'projects'" - Creates a folder
    - "create file app.py in projects folder" - Creates Python file in projects folder  
    - "add code to existing file main.js" - Updates existing file with new content
    
    Always generate complete, functional code when requested. Always confirm what files/folders were created and provide helpful information.""",
    tools=[create_files_and_folders]
)



result = Runner.run_sync(
    main_agent, 
    "create projects folder"
)
print(result.final_output)

# # Test the agent
# if __name__ == "__main__":
#     # Test 1: Simple greeting
#     print("=== Test 1: Greeting ===")
#     result = Runner.run_sync(main_agent, "hello")
#     print(result.final_output)
    
#     print("\n=== Test 2: Create TodoList ===")
#     # Test 2: Create todolist file
#     result = Runner.run_sync(
#         main_agent, 
#         "create file todo.html and add HTML code of todolist"
#     )
#     print(result.final_output)
    
#     print("\n=== Test 3: Create Folder ===")
#     # Test 3: Create folder
#     result = Runner.run_sync(main_agent, "create folder 'my_projects'")
#     print(result.final_output)
    
#     print("\n=== Test 4: Create File in Folder ===")
#     # Test 4: Create file in folder  
#     result = Runner.run_sync(
#         main_agent,
#         "create file app.js in my_projects folder with some JavaScript code"
#     )
#     print(result.final_output)


