from scraper import Scraper
from utils import save_to_file
from config import URL, USER_NAME, PASSWORD, Attendence_url

def main():
    with Scraper(URL) as scraper:
        scraper.login(USER_NAME, PASSWORD)
        scraper.go_to_url(Attendence_url)
        
        table_data = scraper.get_table_data("items table table-striped table-bordered")
        save_to_file(table_data, "attendance.json")
    print("saved attendence data as attendence.json")

if __name__ == "__main__":
    main()
