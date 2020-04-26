class Game:
    uid: str
    title: str
    price: str
    discountPrice: str
    discount: str
    platforms: tuple

    def __init__(self,
                 uid: int = 0,
                 title: str = "",
                 price: str = "",
                 discountPrice: str = "",
                 discount: str = "",
                 platforms: tuple = {}):
        self.uid = uid
        self.title = title
        self.price = price
        self.discountPrice = discountPrice
        self.discount = discount
        self.platforms = platforms

    def printValues(self):
        print("App " +
              self.uid + ": <" +
              self.title + ">, price <" +
              self.price + ">, discount <" +
              self.discount + ">, discount price <" +
              self.discountPrice + ">")
