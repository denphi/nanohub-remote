"""
Projects Filesystem Usage Example

This script demonstrates how to use the Projects API with nanohubremote,
including listing available projects, selecting one by ID, and performing
file system operations: list, create folder, create file, edit file,
print file contents, and delete the file.
"""

import nanohubremote as nr

# Authentication
auth_data = {
    'grant_type': 'personal_token',
    'token': ''
}

with nr.Project(auth_data) as project:

    # Step 1: List available projects
    print("=" * 60)
    print("Available Projects")
    print("=" * 60)

    response = project.requestGet('projects/list')
    projects_data = response.json()
    projects = projects_data.get('projects', [])

    if not projects:
        print("No projects found.")
        exit(1)

    for p in projects:
        print(f"  ID: {p['id']}  |  Name: {p.get('title', p.get('alias', 'N/A'))}")

    # Step 2: Select a project by ID
    print()
    project_id = input("Enter the project ID to use: ").strip()

    fs = project.files(project_id)

    # Step 3: List files in the root directory
    print("\n" + "=" * 60)
    print("Step 1: List files in root directory '/'")
    print("=" * 60)

    files = fs.listdir("/")
    print(f"Contents of '/': {files}")

    # Step 4: Create a folder
    folder_name = "/example_folder"
    print("\n" + "=" * 60)
    print(f"Step 2: Create folder '{folder_name}'")
    print("=" * 60)

    fs.makedir(folder_name)
    print(f"Folder '{folder_name}' created.")
    print(f"Contents of '/': {fs.listdir('/')}")

    # Step 5: Create a file inside the folder
    file_path = f"{folder_name}/hello.txt"
    print("\n" + "=" * 60)
    print(f"Step 3: Create file '{file_path}'")
    print("=" * 60)

    with fs.openbin(file_path, "w") as f:
        f.write(b"Hello from nanohubremote!\nThis is the initial content.\n")
    print(f"File '{file_path}' created.")

    # Step 6: Edit (overwrite) the file
    print("\n" + "=" * 60)
    print(f"Step 4: Edit file '{file_path}'")
    print("=" * 60)

    with fs.openbin(file_path, "w") as f:
        f.write(b"Hello from nanohubremote!\nThis content has been updated.\n")
    print(f"File '{file_path}' updated.")

    # Step 7: Print the file contents
    print("\n" + "=" * 60)
    print(f"Step 5: Print file '{file_path}'")
    print("=" * 60)

    with fs.openbin(file_path, "r") as f:
        content = f.read().decode("utf-8")
    print(content)

    # Step 8: Delete the file
    print("=" * 60)
    print(f"Step 6: Delete file '{file_path}'")
    print("=" * 60)

    fs.remove(file_path)
    print(f"File '{file_path}' deleted.")
    print(f"Contents of '{folder_name}': {fs.listdir(folder_name)}")

    # Cleanup: remove the folder
    fs.removedir(folder_name)
    print(f"Folder '{folder_name}' removed.")
    print(f"Contents of '/': {fs.listdir('/')}")

print("\n" + "=" * 60)
print("Example completed!")
print("=" * 60)
