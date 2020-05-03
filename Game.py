class Game:
    uid: int
    title: str
    isFree: bool
    price: int
    discountPrice: int
    discount: str
    platforms: tuple

    def __init__(self,
                 uid: int = 0,
                 title: str = "",
                 isFree: bool = False,
                 price: int = 0,
                 discountPrice: int = 0,
                 discount: str = "",
                 platforms: tuple = {}):
        self.uid = uid
        self.title = title
        self.isFree = isFree
        self.price = price
        self.discountPrice = discountPrice
        self.discount = discount
        self.platforms = platforms

    def printValues(self):
        print("UID: %d, "
              "Title: %s, "
              "Is free: %s, "
              "Price: %d, "
              "Discount Price: %d, "
              "Discount: %s, "
              "Platforms: %s" % (
                  self.uid,
                  self.title,
                  self.isFree,
                  self.price,
                  self.discountPrice,
                  self.discount,
                  self.platforms
              ))
