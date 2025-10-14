import threading
import time
from Order_Placement import OrderPlacement, Cart, UserProfile, RestaurantMenu, PaymentMethod

results = []

def place_order_thread(index):
    cart = Cart()
    cart.add_item('Pizza', 10.0, 1)
    user_profile = UserProfile(delivery_address=f'123 Main St #{index}')
    menu = RestaurantMenu(available_items=['Pizza'])
    order_placement = OrderPlacement(cart, user_profile, menu)
    payment_method = PaymentMethod()
    start = time.time()
    result = order_placement.confirm_order(payment_method)
    end = time.time()
    elapsed = end - start
    results.append((index, result, elapsed))
    print(f"Order {index}: {result}, Time: {elapsed:.2f}s")

threads = []
for i in range(50):
    t = threading.Thread(target=place_order_thread, args=(i+1,))
    threads.append(t)
    t.start()
for t in threads:
    t.join()

# Summary
under_2s = sum(1 for _, _, elapsed in results if elapsed < 2.0)
print(f"\nOrders completed under 2 seconds: {under_2s}/50")
