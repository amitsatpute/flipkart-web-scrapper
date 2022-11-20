class FlipkartObjectRepository:

    def __init__(self):
        print()

    def getLoginCloseButton(self):
        login_close_button = "/html[1]/body[1]/div[2]/div[1]/div[1]/button[1]"
        return login_close_button

    def getInputSearchArea(self):
        search_inputarea = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/form[1]/div[1]/div[1]/input[1]"
        return search_inputarea

    def getSearchButton(self):
        search_button = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/form[1]/div[1]/button[1]"
        return search_button

    def getProductsListByClass(self):
        product_list = "_13oc-S"
        return product_list

    def getProductName(self):
        product_name = "_4rR01T"
        product_name1 ="B_NuCI"
        return product_name,product_name1

    def getPrice(self):
        price = "_30jeq3"
        price1 = "_30jeq3._16Jk6d"
        return price,price1

    def getProductLink(self):
        product_link ="_1fQZEK" #_2rpwqI _1fQZEK
        product_link1 = "_2rpwqI"
        return product_link,product_link1

    def getProductImage(self):
        img_link = "_396cs4._3exPp9"
        img_link1 = "_396cs4._2amPTt._3qGmMb._3exPp9"
        return img_link,img_link1

    def getDiscountPercentageByClass(self):
        discount_percentage = "_3Ay6Sb"
        return discount_percentage

    def getOfferByClass(self):
        offer = "_2ZdXDB"
        return offer

    def getOriginalPriceByClass(self):
        originalPrice = "_3I9_wc"
        return originalPrice

    def getAvailableOffers(self):
        offers = "_3j4Zjq"
        offers1 = "rd9nIL"
        return offers, offers1

    def getMoreOffers(self):
        more_offer = "IMZJg1"
        more_offer1 = "_1JIkBw"
        return more_offer, more_offer1

    def getComment(self):
        comment = "_2-N8zT"
        comment1= "t-ZTKy"
        return comment,comment1

    def getTotalReviewPage(self):
        total_page = "col.JOpGWq"
        return total_page

    def gettotalReviewCount(self):
        totalReview = "row._2afbiS"
        return totalReview

    def getReview(self):
        review = "_2_R_DZ"
        review1 = "col._2wzgFH.K0kLPL"
        return review,review1

    def getRating(self):
        rating = "_3LWZlK._1BLPMq"
        return rating

    def reviewAvailable(self):
        reviewAvailable = "_2c2kV-"
        return reviewAvailable