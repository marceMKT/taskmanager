from task_manager import TaskManager

def print_menu():

    print("\n--- Task manager intelligent ---")
    print("1.- Add task")
    print("2.- List tasks")
    print("3.- Complete task")
    print("4.- Remove task")
    print("5.- Exit")

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
                    manager.list_tasks()
                case 3:
                    task_id = int(input("Task id to complete: "))
                    manager.complete_task(task_id)
                case 4:
                    task_id = int(input("Task id to remove: "))
                    manager.delete_task(task_id)
                case 5:
                    print ("Exit!")
                    break
                case _:
                    print ("Incorrect option. Select another option.")
        except ValueError:
            print ("Incorrect option. Select another option.")

if __name__ == "__main__":
    main()