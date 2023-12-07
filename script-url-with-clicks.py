from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def remove_black_spans(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all black spans 
    black_spans = soup.find_all('span', {'style': re.compile(r'color:\s*#000000;|color:\s*#000;')})

    # Remove each black span and its surrounding HTML
    for span in black_spans:
        # Unwrap the span itself
        span.unwrap()

    # Return the modified HTML
    return str(soup)

def login_and_update_posts(admin_username, admin_password, blog_url):
    # Set up the WebDriver 
    driver = webdriver.Chrome(executable_path="chromedriver-win64/chromedriver.exe")
    
    # Open the blog URL
    driver.get(blog_url)

    # Find and fill in the login form
    username_field = driver.find_element(By.NAME, 'username')
    password_field = driver.find_element(By.NAME, 'password')
    submit_button = driver.find_element(By.NAME, 'loginsubmit')

    username_field.send_keys(admin_username)
    password_field.send_keys(admin_password)
    submit_button.click()

    # Wait for the login to complete 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'postLinks')))

    # Find all post links with class 'postLinks'
    post_links = driver.find_elements(By.CLASS_NAME, 'postLinks')
    
    # Iterate over the post links
    for index, post_link in enumerate(post_links):
        if index % 2 == 0:  # Process only even indices 
            try: 
                post_link.click()

                # Wait for the page to load and find the textarea with name 'body'
                body_textarea = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME, 'body'))
                )

                # Modify the content in the textarea
                current_content = body_textarea.get_attribute('value')
                modified_content = remove_black_spans(current_content)

                # Update the content in the textarea
                body_textarea.clear()
                body_textarea.send_keys(modified_content)

                # Find and click the save button with name 'submit'
                save_button = driver.find_element(By.NAME, 'submit')
                save_button.click()

                # Wait for the save to complete 
                WebDriverWait(driver, 5).until(EC.url_changes(blog_url))

                # Go back to the previous page
                driver.back()
                driver.back()
                
                post_links = driver.find_elements(By.CLASS_NAME, 'postLinks')
                
            except ValueError:
                print(f"Problem happened in this id: {index}") 
                
                 # Go back to the previous page
                driver.back()
                
                post_links = driver.find_elements(By.CLASS_NAME, 'postLinks')
                
                

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    # Replace these with your actual login details and blog URL
    admin_username = 'staff'
    admin_password = 'sd35g3tvrf'
    blog_url = 'https://member.gemtracks.com/guides/outsource/'

    login_and_update_posts(admin_username, admin_password, blog_url)
