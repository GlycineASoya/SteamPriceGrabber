class Game:
    uid: int
    title: str
    isFree: bool
    priceList: dict
    discountPrice: int
    discount: str
    platforms: tuple

    def __init__(self,
                 uid: int = 0,
                 title: str = "",
                 isFree: bool = False,
                 priceList: dict = None,
                 discountPrice: int = 0,
                 discount: str = "",
                 platforms: tuple = {}):
        self.uid = uid
        self.title = title
        self.isFree = isFree
        self.priceList = priceList
        self.discountPrice = discountPrice
        self.discount = discount
        self.platforms = platforms

    def printValues(self):
        print("UID: %d, "
              "Title: %s, "
              "Is free: %s, "
              "Price: %s, "
              "Discount Price: %d, "
              "Discount: %s, "
              "Platforms: %s" % (
                  self.uid,
                  self.title,
                  self.isFree,
                  self.priceList,
                  self.discountPrice,
                  self.discount,
                  self.platforms
              ))
