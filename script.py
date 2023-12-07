from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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
    WebDriverWait(driver, 5).until(EC.url_changes(blog_url))

    # Find all post links with class 'postLinks'
    post_links = driver.find_elements(By.CLASS_NAME, 'postLinks')
    
    # Iterate over the post links
    for index, post_link in enumerate(post_links):
        if index % 2 == 0:  # Process only even indices 
                post_link.click()

                # Wait for the page to load and find the textarea with name 'body'
                body_textarea = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME, 'body'))
                )

                # Modify the content in the textarea
                current_content = body_textarea.get_attribute('value')
                
                soup = BeautifulSoup(current_content, 'html.parser')
                
                nofollow_elements = soup.find_all(attrs={'rel': 'nofollow'})

                for element in nofollow_elements:
                    print(f"rel=nofollow is found {element} on this number: {index + 1}")


                # Wait for the save to complete 
                WebDriverWait(driver, 5).until(EC.url_changes(blog_url))

                # Go back to the previous page
                driver.back()
                
                post_links = driver.find_elements(By.CLASS_NAME, 'postLinks')
                

                
                

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    # Replace these with your actual login details and blog URL
    admin_username = 'username'
    admin_password = 'password'
    blog_url = 'link'

    login_and_update_posts(admin_username, admin_password, blog_url)
