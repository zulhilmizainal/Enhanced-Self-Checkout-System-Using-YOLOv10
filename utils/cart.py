cart_items = []

def add_to_cart(item_name, price):
    for item in cart_items:
        if item["name"] == item_name:
            item["qty"] += 1
            item["amount"] = item["qty"] * item["price"]
            return
    cart_items.append({
        "no": len(cart_items) + 1,
        "name": item_name,
        "qty": 1,
        "price": price,
        "amount": price
    })

def clear_cart():
    cart_items.clear()

def get_cart():
    return cart_items
