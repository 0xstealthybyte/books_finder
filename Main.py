# Made By https://github.com/0xstealthybyte
import requests
from bs4 import BeautifulSoup
import os
def display_options():
    print("Choose a topic:")
    print("1. Science")
    print("2. Growth")
    print("3. Agriculture")
    print("4. Technology")
    print("5. History")
    print("6. Fiction")
    print("7. Philosophy")
    print("8. Other")
def get_topic_choice():
    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if choice in range(1, 9):
                return choice
            else:
                print("Invalid choice. Please choose a number between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number.")
def map_choice_to_topic(choice):
    topics = {
        1: "science",
        2: "growth",
        3: "agriculture",
        4: "technology",
        5: "history",
        6: "fiction",
        7: "philosophy",
        8: "other"
    }
    return topics[choice]
def search_books_online(topic, book_name):
    search_query = f"{book_name} filetype:pdf"
    duckduckgo_url = "https://html.duckduckgo.com/html/"  # DuckDuckGo's HTML search
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = {"q": search_query}

    print(f"Searching DuckDuckGo for books on '{book_name}' under topic '{topic}'...")

    try:
        response = requests.post(duckduckgo_url, headers=headers, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for link in soup.find_all('a', class_="result__url"):
        title = link.text.strip()
        url = link.get("href")

        if "pdf" in url.lower():  # Only get PDF links
            results.append((title, url))

    if not results:
        print("No books found for the given name under this topic.")
        return []

    print("\nFound books:")
    for idx, (title, url) in enumerate(results[:10], start=1):
        print(f"{idx}. {title}\n   Link: {url}\n")

    return results



def save_results_to_file(results, book_name):
    folder_path = f"./{book_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    filename = f"{folder_path}/{book_name}_results.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for idx, (title, link, snippet) in enumerate(results, start=1):
            file.write(f"{idx}. {title}\n   Snippet: {snippet}\n   Link: {link}\n\n")
    print(f"Results saved to {filename}")
def download_book(url, book_name, title):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        book_folder = f"./{book_name}"
        if not os.path.exists(book_folder):
            os.makedirs(book_folder)
        filename = f"{book_folder}/{title}.pdf"  
        filename = filename.replace("/", "_").replace("\\", "_")  
        with open(f"{book_folder}/{filename}", 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded: {title}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the book '{title}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading the book '{title}': {e}")
def download_books(results, book_name):
    for idx, (title, link) in enumerate(results, start=1):  # Only unpack two values
        print(f"Downloading book {idx}: {title}")
        download_book(link, book_name, title)
def main():
    while True:
        display_options()
        topic_choice = get_topic_choice()
        topic = map_choice_to_topic(topic_choice)
        if topic == "other":
            topic = input("Enter your custom topic: ")
        book_names = input("Enter the names of books or keywords to search for (comma-separated): ").split(",")
        for book_name in book_names:
            book_name = book_name.strip()
            results = search_books_online(topic, book_name)
            if results:
                action = input("\nWhat would you like to do next?\n1. Download Books\n2. Save Results to a File\n3. Quit\nChoose an option: ")

                if action == "1":
                    download_books(results, book_name)
                elif action == "2":
                    save_results_to_file(results, book_name)
                elif action == "3":
                    print("Exiting...")
                    return
                else:
                    print("Invalid choice. Please try again.")
        quit_choice = input("Do you want to search for more books? (yes/no): ").lower()
        if quit_choice != "yes":
            break
if __name__ == "__main__":
    main()

