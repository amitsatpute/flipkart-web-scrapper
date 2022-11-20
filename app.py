# doing necessary imports
from flask import Flask, render_template, request
from selenium import webdriver
from flipkart_scrapping import FlipkratScrapper
from webdriver_manager.chrome import ChromeDriverManager
from logger import getLog
from exception import ScrapperException
from flask_cors import cross_origin
import pandas as pd
import sys,os
from entity.config_entity import DataIngestionConfig
from constant.application import APP_HOST,APP_PORT

flipkart_logger = getLog('flipkart.py')

app = Flask(__name__)  # initialising the flask app with the name 'app'

# For selenium driver implementation on heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")

@app.route('/', methods=['POST',
                         'GET'])  # A GET message is send, and the server returns data & The data received by the POST method is not cached by the server.
@cross_origin()
def index():
    if request.method == 'POST':

        searchString = request.form['productName'].replace(" ", "")  # obtaining the search string entered in the form
        try:
            flipkart_scrapper_object = FlipkratScrapper(executable_path=ChromeDriverManager().install(),
                                                        chrome_options=chrome_options)
            flipkart_scrapper_object.openUrl("https://www.flipkart.com/")
            flipkart_logger.info("Url hitted")

            flipkart_scrapper_object.login_popup_handle()
            flipkart_logger.info("login popup handled")

            flipkart_scrapper_object.searchProduct(searchString=searchString)
            flipkart_logger.info(f"Search begins for {searchString}")

            flipkart_product_list = flipkart_scrapper_object.getProductList()
            flipkart_logger.info(f"got products list")


            dataframe = pd.DataFrame(flipkart_product_list)

            product_list_file_path = DataIngestionConfig().product_list_file_path
            
            # creating folder
            dir_path = os.path.dirname(product_list_file_path)
            os.makedirs(dir_path, exist_ok=True)

            flipkart_scrapper_object.saveDataFrameToFile(file_name=product_list_file_path, dataframe=dataframe)
            flipkart_logger.info("Data saved in scrapper file")

            return render_template('home.html', f_data=flipkart_product_list)
        except Exception as e:
            raise  ScrapperException(e,sys)
    else:
        return render_template('index.html')


@app.route('/productDetails', methods=['POST'])
@cross_origin()
def productDetails():
    if request.method == "POST":
        flipkartProductLink = request.form['flipkartProductDetailLink']
        expected_review = request.form['expected_review']
        try:
            flipkart_scrapper_object = FlipkratScrapper(executable_path=ChromeDriverManager().install(),
                                                        chrome_options=chrome_options)
            flipkartProductDetails = flipkart_scrapper_object.getProductDetails(flipkartProductLink,expected_review)
            flipkart_logger.info(f"got product details")

            return render_template('productdetails.html', f_data=flipkartProductDetails)

        except Exception as e:
            raise  ScrapperException(e,sys)

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
