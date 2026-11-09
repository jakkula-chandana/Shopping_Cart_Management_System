import random
import math
from datetime import datetime
from abc import ABC, abstractmethod
# 1. Product Class

class Product:
    def __init__(self, pid, name, price, category, stock):
        self.pid = pid
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock

    def display(self):
        print(f"{self.pid:<8} {self.name:<15} "
              f"Rs.{self.price:<10.2f} {self.category:<15} {self.stock}")


# 2. Discount Class (Abstraction)

class Discount(ABC):

    @abstractmethod
    def calculate(self, amount):
        pass


# 3. Inheritance and Polymorphism

class PercentageDiscount(Discount):

    def calculate(self, amount):
        return amount * 0.10


class FixedDiscount(Discount):

    def calculate(self, amount):
        return 100 if amount >= 1000 else 0


# 4. Shopping Cart Class (Encapsulation)

class ShoppingCart:
    def __init__(self):
        self.__items = {}

    def add_item(self, product, quantity):
        if quantity <= 0:
            print("Invalid quantity!")
            return

        if quantity > product.stock:
            print("Insufficient stock!")
            return

        if product.pid in self.__items:
            self.__items[product.pid]["quantity"] += quantity
        else:
            self.__items[product.pid] = {
                "product": product,
                "quantity": quantity
            }

        product.stock -= quantity
        print("Product added successfully!")

    def remove_item(self, pid):
        if pid in self.__items:
            item = self.__items.pop(pid)
            item["product"].stock += item["quantity"]
            print("Product removed!")
        else:
            print("Product not found!")

    def update_item(self, pid, quantity):
        if pid not in self.__items:
            print("Product not found!")
            return

        if quantity <= 0:
            print("Invalid quantity!")
            return

        item = self.__items[pid]
        product = item["product"]
        difference = quantity - item["quantity"]

        if difference > product.stock:
            print("Insufficient stock!")
            return

        product.stock -= difference
        item["quantity"] = quantity
        print("Quantity updated!")

    def display_cart(self):
        if not self.__items:
            print("Cart is empty!")
            return

        print("\n--- Shopping Cart ---")

        for item in self.__items.values():
            product = item["product"]
            quantity = item["quantity"]

            print(product.name, "x", quantity,
                  "=", product.price * quantity)

    def total_amount(self):
        total = 0

        for item in self.__items.values():
            total += item["product"].price * item["quantity"]

        return total

    def get_items(self):
        return self.__items

    def clear_cart(self):
        for item in self.__items.values():
            item["product"].stock += item["quantity"]

        self.__items.clear()


# 5. Main Shopping System

class ShoppingSystem:

    def __init__(self):
        self.products = [
            Product(101, "Laptop", 55000, "Electronics", 10),
            Product(102, "Mobile", 20000, "Electronics", 15),
            Product(103, "Headphones", 1500, "Accessories", 20),
            Product(104, "Keyboard", 800, "Accessories", 25),
            Product(105, "Mouse", 500, "Accessories", 30),
            Product(106, "Shoes", 2500, "Fashion", 12),
            Product(107, "T-Shirt", 700, "Fashion", 20),
            Product(108, "Bag", 1200, "Fashion", 15)
        ]

        self.cart = ShoppingCart()

        # Tuple and Set
        self.categories = ("Electronics", "Accessories", "Fashion")
        self.searched_categories = set()

    def show_products(self):
        print("\n--- Available Products ---")
        print("ID      Name            Price       Category        Stock")

        for product in self.products:
            product.display()

    def search_product(self):
        keyword = input("Enter product name/category: ").lower()
        found = False

        for product in self.products:
            if (keyword in product.name.lower()
                    or keyword in product.category.lower()):

                product.display()
                self.searched_categories.add(product.category)
                found = True

        if not found:
            print("Product not found!")

    def find_product(self, pid):
        for product in self.products:
            if product.pid == pid:
                return product

        return None

    def add_product(self):
        try:
            pid = int(input("Enter product ID: "))
            product = self.find_product(pid)

            if product:
                quantity = int(input("Enter quantity: "))
                self.cart.add_item(product, quantity)
            else:
                print("Invalid product ID!")

        except ValueError:
            print("Please enter valid numbers!")

    def update_product(self):
        try:
            pid = int(input("Enter product ID: "))
            quantity = int(input("Enter new quantity: "))
            self.cart.update_item(pid, quantity)

        except ValueError:
            print("Please enter valid numbers!")

    def remove_product(self):
        try:
            pid = int(input("Enter product ID: "))
            self.cart.remove_item(pid)

        except ValueError:
            print("Enter a valid product ID!")

    def checkout(self):
        items = self.cart.get_items()

        if not items:
            print("Your cart is empty!")
            return

        self.cart.display_cart()
        subtotal = self.cart.total_amount()
        discount_amount = 0

        print("\nSubtotal: Rs.", subtotal)

        if subtotal >= 1000:
            print("1. 10% Discount")
            print("2. Rs.100 Fixed Discount")
            print("3. No Discount")

            choice = input("Choose discount: ")

            # Polymorphism
            discount = None

            if choice == "1":
                discount = PercentageDiscount()
            elif choice == "2":
                discount = FixedDiscount()

            if discount:
                discount_amount = discount.calculate(subtotal)

        final_amount = math.ceil(subtotal - discount_amount)

        order_id = random.randint(10000, 99999)
        date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        print("\n======= FINAL BILL =======")
        print("Order ID:", order_id)
        print("Date:", date)
        print("Subtotal: Rs.", subtotal)
        print("Discount: Rs.", discount_amount)
        print("Final Amount: Rs.", final_amount)
        print("==========================")

        self.save_bill(order_id, date, items,
                       subtotal, discount_amount, final_amount)

        self.cart.clear_cart()

    def save_bill(self, order_id, date, items,
                  subtotal, discount, final_amount):
        try:
            with open("shopping_bills.txt", "a") as file:
                file.write("\n--- Shopping Bill ---\n")
                file.write(f"Order ID: {order_id}\n")
                file.write(f"Date: {date}\n")

                for item in items.values():
                    product = item["product"]
                    quantity = item["quantity"]

                    file.write(
                        f"{product.name} x {quantity} = "
                        f"Rs.{product.price * quantity}\n"
                    )

                file.write(f"Subtotal: Rs.{subtotal}\n")
                file.write(f"Discount: Rs.{discount}\n")
                file.write(f"Final Amount: Rs.{final_amount}\n")

            print("Bill saved successfully!")

        except OSError:
            print("Unable to save bill!")

    def previous_bills(self):
        try:
            with open("shopping_bills.txt", "r") as file:
                print("\n--- Previous Bills ---")
                print(file.read())

        except FileNotFoundError:
            print("No previous bills found!")


# 6. Main Function

def main():
    shop = ShoppingSystem()

    while True:
        print("\n===== SHOPPING CART MANAGEMENT =====")
        print("1. View Products")
        print("2. Search Products")
        print("3. Add to Cart")
        print("4. View Cart")
        print("5. Update Quantity")
        print("6. Remove Product")
        print("7. Checkout")
        print("8. View Previous Bills")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            shop.show_products()

        elif choice == "2":
            shop.search_product()

        elif choice == "3":
            shop.add_product()

        elif choice == "4":
            shop.cart.display_cart()

        elif choice == "5":
            shop.update_product()

        elif choice == "6":
            shop.remove_product()

        elif choice == "7":
            shop.checkout()

        elif choice == "8":
            shop.previous_bills()

        elif choice == "9":
            print("Thank you for shopping!")
            break

        else:
            print("Invalid choice! Try again.")


# Program Starting Point

if __name__ == "__main__":
    main()