import argparse
import multiprocessing
import threading
import time
import random
import string


def process_segment(segment, result_queue):
    # Function to process a segment: convert characters to uppercase and count occurrences
    char_count = {}
    for char in segment:
        if char.isalpha():
            char_count[char] = char_count.get(char, 0) + 1
    result_queue.put(char_count)

def parallel_text_processing(file_path, num_processes):
    # Function for parallel text file processing
    # Read the text file
    with open(file_path, 'r') as file:
        text = file.read()

    # Determine segment size
    segment_size = len(text) // num_processes

    # Divide text into segments
    segments = [text[i:i+segment_size] for i in range(0, len(text), segment_size)]

    # Create a multiprocessing Queue for results
    result_queue = multiprocessing.Queue()

    # Create and start processes for parallel processing
    processes = []
    for segment in segments:
        process = multiprocessing.Process(target=process_segment, args=(segment, result_queue))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Collect results from the queue
    total_char_count = {}
    while not result_queue.empty():
        char_count = result_queue.get()
        for char, count in char_count.items():
            total_char_count[char] = total_char_count.get(char, 0) + count

    return total_char_count

def generate_test_file(file_path, size_mb):
    # Generate a test text file with random characters
    num_chars = size_mb * 1024 * 1024  # Convert size from MB to bytes
    with open(file_path, 'w') as file:
        for _ in range(num_chars):
            file.write(random.choice(string.ascii_lowercase))
class ProcessManager:
    def __init__(self):
        self.processes = {}
        self.next_process_id = 1

    def create_process(self, process_name):
        # Create a new process with a unique ID
        process_id = self.next_process_id
        self.next_process_id += 1
        self.processes[process_id] = {'name': process_name, 'threads': {}}
        print(f"Process '{process_name}' created with ID {process_id}")

    def list_processes(self):
        # List all active processes
        print("Active Processes:")
        for process_id, process_info in self.processes.items():
            print(f"ID: {process_id}, Name: {process_info['name']}, Threads: {len(process_info['threads'])}")

    def kill_process(self, process_id):
        # Terminate a process and all its threads
        if process_id in self.processes:
            del self.processes[process_id]
            print(f"Process with ID {process_id} terminated")
        else:
            print(f"Error: Process with ID {process_id} not found")

    def display_process_details(self, process_id):
        # Display detailed information about a process and its threads
        if process_id in self.processes:
            process_info = self.processes[process_id]
            print(f"Process ID: {process_id}, Name: {process_info['name']}")
            print("Associated Threads:")
            for thread_id, thread_info in process_info['threads'].items():
                print(
                    f"Thread ID: {thread_id}, Name: {thread_info['name']}, Status: {thread_info.get('status', 'Active')}")
        else:
            print(f"Error: Process with ID {process_id} not found")

    def suspend_process(self, process_id):
        # Suspend a process
        if process_id in self.processes:
            self.processes[process_id]['status'] = 'Suspended'
            print(f"Process with ID {process_id} suspended")
        else:
            print(f"Error: Process with ID {process_id} not found")

    def resume_process(self, process_id):
        # Resume a suspended process
        if process_id in self.processes and self.processes[process_id].get('status') == 'Suspended':
            self.processes[process_id]['status'] = 'Active'
            print(f"Process with ID {process_id} resumed")
        else:
            print(f"Error: Process with ID {process_id} not suspended or not found")

class ThreadManager:
    def __init__(self, process_manager):
        self.process_manager = process_manager
        self.threads = {}
        self.next_thread_id = 1

    def create_thread(self, thread_name, process_id):
        # Create a new thread associated with a process
        thread_id = self.next_thread_id
        self.next_thread_id += 1
        if process_id in self.process_manager.processes:
            self.process_manager.processes[process_id]['threads'][thread_id] = {'name': thread_name}
            print(f"Thread '{thread_name}' created with ID {thread_id} in Process ID {process_id}")
        else:
            print(f"Error: Process with ID {process_id} not found")

    def suspend_thread(self, process_id, thread_id):
        # Suspend a thread in a process
        if process_id in self.process_manager.processes and thread_id in self.process_manager.processes[process_id][
            'threads']:
            self.process_manager.processes[process_id]['threads'][thread_id]['status'] = 'Suspended'
            print(f"Thread with ID {thread_id} suspended in Process ID {process_id}")
        else:
            print(f"Error: Thread with ID {thread_id} not found in Process ID {process_id}")

    def resume_thread(self, process_id, thread_id):
        # Resume a suspended thread in a process
        if process_id in self.process_manager.processes and thread_id in self.process_manager.processes[process_id][
            'threads']:
            self.process_manager.processes[process_id]['threads'][thread_id]['status'] = 'Active'
            print(f"Thread with ID {thread_id} resumed in Process ID {process_id}")
        else:
            print(f"Error: Thread with ID {thread_id} not found in Process ID {process_id}")



def shared_memory_ipc(data):
    # Function for shared memory IPC
    data.value += 1  # Increment the shared value
    print(f"Shared Memory: Incremented Value = {data.value}")

def message_passing_ipc(queue):
    # Function for message passing IPC
    message = "Hello from Child Process!"
    queue.put(message)
    print("Message Passing: Message sent from Child Process")



def main():
    process_manager = ProcessManager()
    thread_manager = ThreadManager(process_manager)  # Pass the ProcessManager instance to ThreadManager

    while True:
        print("\nOptions:")
        print("1. Create Process")
        print("2. List Processes")
        print("3. Display Process Details")
        print("4. Suspend Process")
        print("5. Resume Process")
        print("6. Create Thread")
        print("7. Suspend Thread")
        print("8. Resume Thread")
        print("9. Shared Memory IPC")
        print("10. Message Passing IPC")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            process_name = input("Enter process name: ")
            process_manager.create_process(process_name)
        elif choice == '2':
            process_manager.list_processes()
        elif choice == '3':
            process_id = int(input("Enter process ID to display details: "))
            process_manager.display_process_details(process_id)
        elif choice == '4':
            process_id = int(input("Enter process ID to suspend: "))
            process_manager.suspend_process(process_id)
        elif choice == '5':
            process_id = int(input("Enter process ID to resume: "))
            process_manager.resume_process(process_id)
        elif choice == '6':
            thread_name = input("Enter thread name: ")
            process_id = int(input("Enter process ID to create thread in: "))
            thread_manager.create_thread(thread_name, process_id)
        elif choice == '7':
            process_id = int(input("Enter process ID: "))
            thread_id = int(input("Enter thread ID to suspend: "))
            thread_manager.suspend_thread(process_id, thread_id)
        elif choice == '8':
            process_id = int(input("Enter process ID: "))
            thread_id = int(input("Enter thread ID to resume: "))
            thread_manager.resume_thread(process_id, thread_id)
        elif choice == '9':
            # Shared Memory IPC test
            shared_value = multiprocessing.Value('i', 0)  # Shared memory value
            process_ipc = multiprocessing.Process(target=shared_memory_ipc, args=(shared_value,))
            process_ipc.start()
            process_ipc.join()
        elif choice == '10':
            # Message Passing IPC test
            message_queue = multiprocessing.Queue()  # Message passing queue
            process_ipc2 = multiprocessing.Process(target=message_passing_ipc, args=(message_queue,))
            process_ipc2.start()
            process_ipc2.join()
        elif choice == '11':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    # Test parallel text processing
    file_path = "example.txt"
    parallel_text_processing(file_path)

if __name__ == "__main__":
    # Generate a test file (example.txt) with a specified size (10 MB)
    file_path = "example.txt"
    size_mb = 10  # Size of the test file in MB
    generate_test_file(file_path, size_mb)
    print(f"Test file '{file_path}' generated with size {size_mb} MB.")

    # Perform parallel text processing on the test file with 4 processes
    start_time = time.time()
    num_processes = 4  # Number of processes for parallel processing
    char_count_result = parallel_text_processing(file_path, num_processes)
    end_time = time.time()

    # Print results
    print("Character Count Result:", char_count_result)
    print("Execution Time:", end_time - start_time, "seconds")
    main()
