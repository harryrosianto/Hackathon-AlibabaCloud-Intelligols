from models.product import ProductBase, ProductFullBase
from util.partial import optional


class ProductCreateSch(ProductBase):
    pass

class ProductSch(ProductFullBase):
    pass

@optional
class ProductUpdateSch(ProductBase):
    pass