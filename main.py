from task_manager import TaskManager
from ai_service import create_simple_task

def print_menu():

    print("\n--- Task manager intelligent ---")
    print("1.- Add task")
    print("2.- Add complex task (with IA)")
    print("3.- List tasks")
    print("4.- Complete task")
    print("5.- Remove task")
    print("6.- Exit")

def main():
    manager = TaskManager();
    while True:
        print_menu()
        try:
            choice = int(input("Select an option: "))
            match choice:
                case 1:
                    description = input("Task description: ")
                    manager.add_task(description)
                case 2:
                    description = input("Task description: ")
                    subtasks = create_simple_task(description)
                    for subtask in subtasks:
                        if not subtask.startswith("Error:"):
                            manager.add_task(subtask)
                        else:
                            print(subtask)
                            break
                case 3:
                    manager.list_tasks()
                case 4:
                    task_id = int(input("Task id to complete: "))
                    manager.complete_task(task_id)
                case 5:
                    task_id = int(input("Task id to remove: "))
                    manager.delete_task(task_id)
                case 6:
                    print ("Exit!")
                    break
                case _:
                    print ("Incorrect option. Select another option.")
        except ValueError:
            print ("Incorrect option. Select another option.")

if __name__ == "__main__":
    main()