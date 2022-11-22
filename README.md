# flipkart-web-scrapper

Web scraping is a technique using which the webpages from the internet are fetched and parsed to understand and extract specific information similar to a human being. 
Hence, web scrappers are applications/bots, which automatically send requests to websites and then extract the desired information from the website output. 


This is web scrapping project. Which scrapping the data about product from flipkart website and show it on the webpage.

# Application Architecture
![image](https://user-images.githubusercontent.com/24702773/203055006-6667ef39-6734-4f16-849a-73708a93dc92.png)


# Tech Stack Used
1. Python 
2. Selenium 
3. MongoDB


# How to run?

# Step 1: Clone the repository
git clone https://github.com/amitsatpute/flipkart-web-scrapper.git

# Step 2- Create a conda environment after opening the repository
conda create -n scrapper python=3.9.0 -y
conda activate scrapper

# Step 3 - Install the requirements
pip install -r requirements.txt

# step 4 - setup the MONGODB URL
Goto constant folder then env_variable.py file there put your MONGODB URL

# Step 5 - Run the application server
python app.py


## Demo

# Landing Page
![image](https://user-images.githubusercontent.com/24702773/203227262-35861dde-d97b-47fc-b8a4-39bf36435ce4.png)

# Product list page
![image](https://user-images.githubusercontent.com/24702773/203227470-cc07c983-8319-4b89-bc4f-e7e3654e99fa.png)

# Product Review page
![image](https://user-images.githubusercontent.com/24702773/203228993-c02e7e6a-fb6b-45cc-961b-6b7bb3c1a079.png)

