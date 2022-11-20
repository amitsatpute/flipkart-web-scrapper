from selenium import webdriver
from object_repository import FlipkartObjectRepository
from selenium.webdriver.common.by import By
import pandas as pd
from exception import ScrapperException
import sys, os
from mongoDB_operations import MongoDBManagement
from constant.database import DATABASE_NAME, COLLECTION_NAME
from entity.config_entity import DataIngestionConfig


class FlipkratScrapper:

    def __init__(self, executable_path, chrome_options):
        """
        This function initializes the web browser driver
        :param executable_path: executable path of chrome driver.
        """
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        except Exception as e:
            raise ScrapperException(e, sys)
    
    def getCurrentWindowUrl(self):
        """
        This function returns the url of current window
        """
        try:
            current_window_url = self.driver.current_url
            return current_window_url
        except Exception as e:
            raise ScrapperException(e, sys)

    def getLocatorsObject(self):
        """
        This function initializes the Locator object and returns the locator object
        """
        try:
            locators = FlipkartObjectRepository()
            return locators
        except Exception as e:
            raise ScrapperException(e, sys)

    def openUrl(self, url):
        """
        Thius function open the particular url passed.
        :param url: URL to be opened.
        :return:
        """
        try:
            if self.driver:
                self.driver.get(url)
                return True
            else:
                return False
        except Exception as e:
            raise ScrapperException(e, sys)

    def wait(self):
        """
        This function waits for the given time
        """
        try:
            self.driver.implicitly_wait(3)
        except Exception as e:
            raise ScrapperException(e, sys)

    def login_popup_handle(self):
        """
        This function handle/closes the login popup displayed.
        """
        try:
            self.wait()
            locator = self.getLocatorsObject()
            self.findElementByXpath(xpath=locator.getLoginCloseButton()).click()
            return True
        except Exception as e:
            raise ScrapperException(e, sys)

    def findElementByXpath(self, xpath):
        """
        This function finds the web element using xpath passed
        :param Xpath:
        :return:
        """
        try:
            element = self.driver.find_element(By.XPATH, value=xpath)
            return element
        except Exception as e:
            raise ScrapperException(e, sys)

    def searchProduct(self, searchString):
        """
        This function helps to search product using search string provided by the user
        """
        try:
            locator = self.getLocatorsObject()
            searchButton = locator.getSearchButton()
            inputArea = locator.getInputSearchArea()
            search_box_path = self.findElementByXpath(inputArea)
            search_box_path.send_keys(searchString)
            search_button = self.findElementByXpath(searchButton)
            search_button.click()
            return True
        except Exception as e:
            # self.driver.refresh()
            raise ScrapperException(e, sys)

    def convertListToStr(self, list):
        """
        This function convert single list value to string
        :param list:
        :return: str value
        """
        try:
            str1 = ' '.join(str(i.text) for i in list)
            return str1
        except Exception as e:
            # self.driver.refresh()
            raise ScrapperException(e, sys)

    def findElementsByClass(self, element, classpath):
        """
        This function finds web elements using Classpath provided
        """
        try:
            if element is None:
                result = self.driver.find_elements(By.CLASS_NAME, value=classpath)
                return result
            else:
                result = element.find_elements(By.CLASS_NAME, value=classpath)
                return result
        except Exception as e:
            raise ScrapperException(e, sys)

    def findElementByClass(self, element, classpath):
        """
        This function finds web element using Classpath provided
        """
        try:
            if element is None:
                result = self.driver.find_element(By.CLASS_NAME, value=classpath)
                return result
            else:
                result = element.find_element(By.CLASS_NAME, value=classpath)
                return result
        except Exception as e:
            raise ScrapperException(e, sys)

    def getProductLink(self, element):
        """
        This function will return product link
        :return:
        """
        try:
            locator = self.getLocatorsObject()
            if locator.getProductLink()[0] in self.driver.page_source:
                return self.findElementByClass(element=element, classpath=locator.getProductLink()[0])
            else:
                return self.findElementByClass(element=element, classpath=locator.getProductLink()[1])
        except Exception as e:
            raise ScrapperException(e, sys)

    def getProductList(self):
        """
        This function helps to retrieve the Product list
        :return:
        """
        try:
            products_list = []
            locator = self.getLocatorsObject()
            all_elements_path = locator.getProductsListByClass()

            for element in self.findElementsByClass(element=None, classpath=all_elements_path):
                product_name = self.convertListToStr(
                    self.findElementsByClass(element=element, classpath=locator.getProductName()[0]))
                price = self.convertListToStr(
                    self.findElementsByClass(element=element, classpath=locator.getPrice()[0]))
                original_price = self.convertListToStr(
                    self.findElementsByClass(element=element, classpath=locator.getOriginalPriceByClass()))
                discount_percentage = self.convertListToStr(
                    self.findElementsByClass(element=element, classpath=locator.getDiscountPercentageByClass()))
                offer = self.convertListToStr(
                    self.findElementsByClass(element=element, classpath=locator.getOfferByClass()))
                product_link = self.getProductLink(element)
                product_image = self.findElementByClass(element=element, classpath=locator.getProductImage()[0])

                product_detail = {"product_name": product_name, "product_price": price,
                                  "product_link": product_link.get_attribute('href'),
                                  "product_image": product_image.get_attribute('src'), "original_price": original_price,
                                  "discount_percentage": discount_percentage, "product_offer": offer}

                products_list.append(product_detail)

            return products_list

        except Exception as e:
            raise ScrapperException(e, sys)

    def checkMoreOffer(self, more_offers):
        """
        This function checks whether more offer links is provided for the product or not.
        """
        try:
            if more_offers in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise ScrapperException(e, sys)

    def clickOnMoreOffer(self, more_offers, more_offers1):
        """
        This function clicks on more offer button.
        """
        try:
            status = self.checkMoreOffer(more_offers)

            if status:
                more_offer = self.findElementByClass(element=None, classpath=more_offers1)
                more_offer.click()
                return True
            else:
                return False
        except Exception as e:
            raise ScrapperException(e, sys)

    def getAvailableOffer(self):
        """
        This function returns offers available
        """
        try:
            locator = self.getLocatorsObject()
            prod_offers = locator.getAvailableOffers()[0]
            prod_offers1 = locator.getAvailableOffers()[1]
            more_offers = locator.getMoreOffers()[0]
            more_offers1 = locator.getMoreOffers()[1]

            status = self.checkMoreOffer(more_offers)
            if status:
                self.clickOnMoreOffer(more_offers, more_offers1)
            if prod_offers1 in self.driver.page_source:
                offers_list = self.findElementsByClass(element=None, classpath=prod_offers)
                offer_details = [i.text for i in offers_list]
            else:
                offer_details = "No Offer For the product"
            return offer_details
        except Exception as e:
            raise ScrapperException(e, sys)

    def removeSpecialChar(self, str):
        """
        This function will Remove Special Char
        :param string: return int
        :return:
        """
        try:
            string = str.split(" ")[3]
            value = ''.join(letter for letter in string if letter.isalnum())
            return value
        except Exception as e:
            raise ScrapperException(e, sys)

    def checkReviewsAvailable(self, available_review):
        """
        This function checks whether more offer links is provided for the product or not.
        """
        try:
            if available_review in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise ScrapperException(e, sys)

    def getReviewsToDisplay(self, expected_review):
        """
        This function return the product reviews
        """
        try:
            locator = self.getLocatorsObject()
            available_review = locator.reviewAvailable()
            status = self.checkReviewsAvailable(available_review=available_review)
            if status:
                viewAllReview = locator.getTotalReviewPage()
                review_list = []
                element = self.findElementsByClass(element=None, classpath=viewAllReview)
                for i in element:
                    reviewPage_link = i.find_element(By.XPATH, value="a[1]").get_attribute('href')

                self.openUrl(reviewPage_link)
                count = 1
                user_count = 0
                while count <= 1000:
                    count = count + 1

                    new_url = reviewPage_link + "&page=" + str(count)

                    review = self.findElementsByClass(element=None, classpath=locator.getReview()[1])
                    if locator.getComment()[0] in self.driver.page_source:
                        for i in review:
                            if len(review_list) < int(expected_review):
                                rating = self.findElementByClass(element=i, classpath=locator.getRating()).text
                                comment_header = self.findElementByClass(element=i, classpath=locator.getComment()[0]).text
                                comment = self.findElementByClass(element=i, classpath=locator.getComment()[1]).text

                                result = {'rating': rating, 'comment_header':comment_header, 'comment': comment}

                                review_list.append(result)
                                
                            else:
                                return review_list

                        self.openUrl(new_url)

        except Exception as e:
            raise ScrapperException(e, sys)

    def getProductDetails(self, productLink, expected_review):
        """
        This function retrieve product details
        :param productLink:
        :return: productDetails
        """
        try:
            mongoClient = MongoDBManagement()
            self.openUrl(productLink)
            locator = self.getLocatorsObject()
            prod_name = locator.getProductName()[1]
            prod_price = locator.getPrice()[1]
            prod_img = locator.getProductImage()[1]
            product_name = self.findElementByClass(element=None, classpath=prod_name).text
            product_price = self.findElementByClass(element=None, classpath=prod_price).text
            original_price = self.convertListToStr(
                self.findElementsByClass(element=None, classpath=locator.getOriginalPriceByClass()))
            discount_percentage = self.convertListToStr(
                self.findElementsByClass(element=None, classpath=locator.getDiscountPercentageByClass()))

            product_offers = self.getAvailableOffer()
            product_image = self.findElementByClass(element=None, classpath=prod_img).get_attribute('src')

            rows = mongoClient.findfirstRecord(db_name=DATABASE_NAME,
                                               collection_name=COLLECTION_NAME,
                                               query={'product_name': product_name})

            if rows is not None:
                reviews = rows['reviews']
                if int(expected_review) != len(reviews):
                    total_reviews = self.getReviewsToDisplay(expected_review)
                    mongoClient.updateOneRecord(db_name=DATABASE_NAME,
                                                collection_name=COLLECTION_NAME,
                                                query_search_string={'product_name': product_name},
                                                query_new_record={'reviews': total_reviews})
                else:
                    total_reviews = reviews
            else:
                total_reviews = self.getReviewsToDisplay(expected_review)
                record = {'product_name': product_name, 'reviews': total_reviews}
                mongoClient.insertRecord(db_name=DATABASE_NAME,
                                         collection_name=COLLECTION_NAME,
                                         record=record)

            result = {"product_name": product_name, "product_price": product_price, "product_offers": product_offers,
                      "product_image": product_image, "comments": total_reviews, "original_price": original_price,
                      "discount_percentage": discount_percentage, "product_link": productLink}

            self.createDataFrame(result)

            return result

        except Exception as e:
            raise ScrapperException(e, sys)

    def createDataFrame(self, data):
        """
        Thin function will create DataFrame
        :param data:
        :return:
        """
        try:
            result = []
            product_name = data['product_name']
            product_price = data['product_price']
            original_price = data['original_price']
            discount_percentage = data['discount_percentage']
            comments = data['comments']

            for i in comments:
                data = {"product_name": product_name, "product_price": product_price, "original_price": original_price,
                        "discount_percentage": discount_percentage, 'rating': i['rating'],'comment_header':i['comment_header'], 'comment': i['comment']}
                result.append(data)

            dataframe = pd.DataFrame(result)
            review_store_file_path = DataIngestionConfig().review_store_file_path
            # creating folder
            dir_path = os.path.dirname(review_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            self.saveDataFrameToFile(file_name=review_store_file_path, dataframe=dataframe)
            return result
        except Exception as e:
            raise ScrapperException(e, sys)

    def saveDataFrameToFile(self, dataframe, file_name):
        """
        This function saves dataframe into filename given
        """
        try:
            dataframe.to_csv(file_name, index=False, header=True)
        except Exception as e:
            raise ScrapperException(e, sys)

    def closeConnection(self):
        """
        This function closes the connection
        """
        try:
            self.driver.close()
        except Exception as e:
            raise ScrapperException(e, sys)
