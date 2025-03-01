import json
import datetime

tasks = []
completed_tasks = []
deleted_tasks = []

name = input("Please Enter your name: ")

def welcome_message():
    print(f"Hello {name}. Welcome to your To-Do List Manager👋. How can I help you today?")

def show_menu():
    print("\nWhat do you want to do?")
    print("1. Add a task")
    print("2. View active tasks")
    print("3. View completed tasks")
    print("4. View deleted tasks")
    print("5. Mark a task as done")
    print("6. Delete a task")
    print("7. Edit task name")
    print("8. Exit")

def get_user_choice():
    return input("\nEnter a number (1-8): ")

def save_tasks(filename, task_list):
    with open(filename, "w") as f:
        json.dump(task_list, f, indent=4)

def load_tasks(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

tasks = load_tasks("Active.txt")
completed_tasks = load_tasks("Completed.txt")
deleted_tasks = load_tasks("Deleted.txt")

def add_task():
    task_name = input("Enter the task: ")
    task_id = max([t["task_id"] for t in tasks], default=0) + 1
    task = {
        "task_id": task_id,
        "task_name": task_name,
        "task_status": "Active",
        "time_created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "time_finished": None
    }
    tasks.append(task)
    save_tasks("Active.txt", tasks)
    print(f"\nTask with details: {{ Task ID: {task['task_id']}, Name: {task['task_name']}, Status: {task['task_status']}, Created: {task['time_created']}, Finished: {'Not completed' if not task['time_finished'] else task['time_finished']} }} Successfully added!")

def view_tasks(task_list, title):
    print(f"\n{title} Tasks:")
    if not task_list:
        print("No tasks available.")
    else:
        for task in task_list:
            print(f"""ID: {task['task_id']}, Name: {task['task_name']}, Status: {task['task_status']}, Created: {task['time_created']}, Finished: {task['time_finished']}""")

def view_active_tasks():
    view_tasks(tasks, "Active")

def view_completed_tasks():
    view_tasks(completed_tasks, "Completed")

def view_deleted_tasks():
    view_tasks(deleted_tasks, "Deleted")

def mark_task_done():
    view_active_tasks()
    try:
        task_number = int(input("Enter the task ID to mark as complete: "))
        for task in tasks:
            if task["task_id"] == task_number:
                tasks.remove(task)
                task["task_status"] = "Completed"
                task["time_finished"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                completed_tasks.append(task)
                save_tasks("Active.txt", tasks)
                save_tasks("Completed.txt", completed_tasks)
                print(f"Task '{task['task_name']}' marked as completed!")
                return
        print("Invalid task ID!")
    except ValueError:
        print("Please enter a valid number.")

def delete_task():
    view_active_tasks()
    try:
        task_number = int(input("Enter the task ID to delete: "))
        for task in tasks:
            if task["task_id"] == task_number:
                tasks.remove(task)
                task["task_status"] = "Deleted"
                deleted_tasks.append(task)
                save_tasks("Active.txt", tasks)
                save_tasks("Deleted.txt", deleted_tasks)
                print(f"Task '{task['task_name']}' has been deleted!")
                return
        print("Invalid task ID!")
    except ValueError:
        print("Please enter a valid number.")

def edit_task_name():
    view_active_tasks()
    try:
        task_number = int(input("Enter the task ID to edit: "))
        for task in tasks:
            if task["task_id"] == task_number:
                new_name = input("Enter the new task name: ")
                task["task_name"] = new_name
                save_tasks("Active.txt", tasks)
                print(f"Task ID {task_number} name updated to '{new_name}'!")
                return
        print("Invalid task ID!")
    except ValueError:
        print("Please enter a valid number.")

def exit_program():
    save_tasks("Active.txt", tasks)
    save_tasks("Completed.txt", completed_tasks)
    save_tasks("Deleted.txt", deleted_tasks)
    print(f"Goodbye {name}😞! Your tasks activities for today have been saved.\nSee you soon!")
    exit()

def user_input_process(user_choice):
    if user_choice == "1":
        add_task()
    elif user_choice == "2":
        view_active_tasks()
    elif user_choice == "3":
        view_completed_tasks()
    elif user_choice == "4":
        view_deleted_tasks()
    elif user_choice == "5":
        mark_task_done()
    elif user_choice == "6":
        delete_task()
    elif user_choice == "7":
        edit_task_name()
    elif user_choice == "8":
        exit_program()
    else:
        print("Invalid choice! Choose a number between 1-8.")

def main():
    welcome_message()
    show_menu()
    while True:
        choice = get_user_choice()
        user_input_process(choice)
        print("_" * 100)
        again = input("\nIs there anything else you want to do again? (yes/no): ").strip().lower()
        if again not in ["yes", "yeah", "y"]:
            exit_program()
        else:
            show_menu()

if __name__ == "__main__":
    main()