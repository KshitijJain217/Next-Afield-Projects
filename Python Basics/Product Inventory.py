
# Product Inventory Management System
# Demonstrates OOP and Encapsulation in Python

class Product:
    """Represents a single product with encapsulated data."""

    def __init__(self, product_id, name, price, quantity):
        self.__product_id = product_id   # Private: can't be accessed directly
        self.__name = name               # Private
        self.__price = price             # Private
        self.__quantity = quantity       # Private

    # --- Getters ---
    def get_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    # --- Setters (with basic validation) ---
    def set_name(self, name):
        if name.strip():
            self.__name = name
        else:
            print("  [!] Name cannot be empty.")

    def set_price(self, price):
        if price >= 0:
            self.__price = price
        else:
            print("  [!] Price cannot be negative.")

    def set_quantity(self, quantity):
        if quantity >= 0:
            self.__quantity = quantity
        else:
            print("  [!] Quantity cannot be negative.")

    def display(self):
        """Prints a formatted summary of the product."""
        print(f"  ID: {self.__product_id:<5} | "
              f"Name: {self.__name:<20} | "
              f"Price: ₹{self.__price:<8.2f} | "
              f"Qty: {self.__quantity}")


class Inventory:

    def __init__(self):
        self._products = {}       # Protected: stores products by ID
        self._next_id = 1         # Protected: auto-increments product ID

    def add_product(self, name, price, quantity):

        product = Product(self._next_id, name, price, quantity)
        self._products[self._next_id] = product
        print(f"\n  ✓ Product '{name}' added with ID {self._next_id}.")
        self._next_id += 1

    def view_all(self):

        if not self._products:
            print("\n  [!] Inventory is empty.")
            return
        print("\n  " + "-" * 65)
        print("  PRODUCT INVENTORY")
        print("  " + "-" * 65)
        for product in self._products.values():
            product.display()
        print("  " + "-" * 65)

    def search_product(self, keyword):

        found = [p for p in self._products.values()
                 if keyword.lower() in p.get_name().lower()]
        if found:
            print(f"\n  Search results for '{keyword}':")
            for p in found:
                p.display()
        else:
            print(f"\n  [!] No products found matching '{keyword}'.")

    def update_product(self, product_id, name=None, price=None, quantity=None):

        product = self._products.get(product_id)
        if not product:
            print(f"\n  [!] Product with ID {product_id} not found.")
            return
        if name:
            product.set_name(name)
        if price is not None:
            product.set_price(price)
        if quantity is not None:
            product.set_quantity(quantity)
        print(f"\n  ✓ Product ID {product_id} updated successfully.")

    def delete_product(self, product_id):

        if product_id in self._products:
            removed = self._products.pop(product_id)
            print(f"\n  ✓ Product '{removed.get_name()}' deleted.")
        else:
            print(f"\n  [!] Product ID {product_id} not found.")


def main():
    inventory = Inventory()
    print("\n  ==============================")
    print("   INVENTORY MANAGEMENT SYSTEM ")
    print("  ==============================")

    while True:
        print("\n  1. Add Product")
        print("  2. View All Products")
        print("  3. Search Product")
        print("  4. Update Product")
        print("  5. Delete Product")
        print("  6. Exit")

        choice = input("\n  Enter your choice (1-6): ").strip()

        if choice == "1":
            name = input("  Product name: ").strip()
            price = float(input("  Price (₹): "))
            qty = int(input("  Quantity: "))
            inventory.add_product(name, price, qty)

        elif choice == "2":
            inventory.view_all()

        elif choice == "3":
            keyword = input("  Enter product name to search: ").strip()
            inventory.search_product(keyword)

        elif choice == "4":
            pid = int(input("  Enter Product ID to update: "))
            name = input("  New name (press Enter to skip): ").strip() or None
            price_input = input("  New price (press Enter to skip): ").strip()
            price = float(price_input) if price_input else None
            qty_input = input("  New quantity (press Enter to skip): ").strip()
            qty = int(qty_input) if qty_input else None
            inventory.update_product(pid, name, price, qty)

        elif choice == "5":
            pid = int(input("  Enter Product ID to delete: "))
            inventory.delete_product(pid)

        elif choice == "6":
            print("\n  Goodbye! Exiting system.\n")
            break

        else:
            print("\n  [!] Invalid choice. Please enter 1–6.")


if __name__ == "__main__":
    main()