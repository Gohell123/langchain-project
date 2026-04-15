from langchain.tools import tool

@tool
def get_product_price(product_name: str) -> float:
    """
    Get correct prices for the listed products.
    Always use this tool if user asks for product price.
    Supported Products: 
    -Laptop
    -Headphone
    -keyboard

    Return the exact price
    """
    product_name = product_name.lower().strip()

    # Normalize common variations
    if "laptop" in product_name:
        product_name = "laptop"
    elif "headphone" in product_name:
        product_name = "headphone"
    elif "keyboard" in product_name:
        product_name = "keyboard"

    price = {"laptop":1299.99,"headphone":99.55,"keyboard":55.30}
    return price.get(product_name, -1.0)

@tool
def get_product_discount(price: float, discount_tier: str) -> float:
    """
    Always use this tool to calculate the discounts on Products as per the tier provided by the User.

    Apply discount tier: 
    -bronze
    -silver
    -gold

    """

    discount_tier=discount_tier.lower().strip()
    if "gold" in discount_tier:
        discount_tier="gold"
    elif "silver" in discount_tier:
        discount_tier="silver"
    elif "bronze"in discount_tier:
        discount_tier="bronze"
    else:
        pass
    
    discount_percent = {"bronze":5,"silver":10,"gold":15}
    discount = discount_percent.get(discount_tier, 0)
    return round(price * (1-discount/100), 2)