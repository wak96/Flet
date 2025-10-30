import flet as ft

# ---------- PRODUCT DATA ----------
PRODUCTS = [
    {"name": "Smartphone", "price": 899, "image": "https://cdn-icons-png.flaticon.com/512/992/992700.png"},
    {"name": "Laptop", "price": 1499, "image": "https://cdn-icons-png.flaticon.com/512/1063/1063198.png"},
    {"name": "Headphones", "price": 299, "image": "https://cdn-icons-png.flaticon.com/512/1041/1041916.png"},
    {"name": "Camera", "price": 799, "image": "https://cdn-icons-png.flaticon.com/512/2920/2920244.png"},
    {"name": "Watch", "price": 199, "image": "https://cdn-icons-png.flaticon.com/512/892/892458.png"},
]


# ---------- PRODUCT CARD ----------
class ProductCard(ft.Card):
    def __init__(self, product, on_view, on_add):
        super().__init__(
            elevation=2,
            content=ft.Container(
                padding=12,
                content=ft.Column(
                    [
                        ft.Image(product["image"], height=120, fit=ft.ImageFit.CONTAIN),
                        ft.Text(product["name"], weight=ft.FontWeight.BOLD, size=16),
                        ft.Text(f"${product['price']}", color=ft.Colors.GREEN, size=14),
                        ft.Row(
                            [
                                ft.ElevatedButton("View", on_click=lambda e: on_view(product)),
                                ft.IconButton(ft.Icons.ADD_SHOPPING_CART, on_click=lambda e: on_add(product)),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ]
                ),
            ),
        )


# ---------- MAIN APP ----------
class ECommerceApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.cart = []

        self.page.title = "🛒 Flet E-Commerce"
        self.page.theme_mode = ft.ThemeMode.LIGHT

        # Header
        self.header = ft.Row(
            [
                ft.Text("Flet E-Commerce", size=24, weight=ft.FontWeight.BOLD),
                ft.IconButton(ft.Icons.SHOPPING_CART, on_click=self.toggle_cart),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # Products grid
        self.products_grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=320,
            spacing=12,
            run_spacing=12,
        )

        # Cart panel (right side)
        self.cart_panel = ft.Container(
            bgcolor=ft.Colors.BLUE_50,
            padding=10,
            content=self.build_cart_view(),
            visible=False,
            width=300,
        )

        # Layout
        self.layout = ft.Row(
            [
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [
                            self.header,
                            self.products_grid,
                        ],
                        expand=True,
                    ),
                ),
                self.cart_panel,
            ],
            expand=True,
        )

        self.page.add(self.layout)
        self.populate_products(PRODUCTS)

    # ---------- Build Cart ----------
    def build_cart_view(self):
        if not self.cart:
            return ft.Column([ft.Text("Cart is empty", color=ft.Colors.GREY)])
        items = [
            ft.Row(
                [
                    ft.Text(p["name"]),
                    ft.Text(f"${p['price']}", color=ft.Colors.GREEN),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            for p in self.cart
        ]
        total = sum(p["price"] for p in self.cart)
        return ft.Column(
            items + [ft.Divider(), ft.Text(f"Total: ${total}", weight=ft.FontWeight.BOLD)],
            scroll=ft.ScrollMode.AUTO,
        )

    # ---------- Populate Products ----------
    def populate_products(self, products):
        self.products_grid.controls.clear()
        for p in products:
            card = ProductCard(p, self.open_product, self.add_to_cart)
            self.products_grid.controls.append(card)
        self.page.update()

    # ---------- Add to Cart ----------
    def add_to_cart(self, product):
        self.cart.append(product)
        self.cart_panel.content = self.build_cart_view()
        self.page.update()

    # ---------- View Product ----------
    def open_product(self, product):
        dlg = ft.AlertDialog(
            title=ft.Text(product["name"]),
            content=ft.Column(
                [
                    ft.Image(product["image"], height=150, fit=ft.ImageFit.CONTAIN),
                    ft.Text(f"Price: ${product['price']}"),
                    ft.Text("This is a demo product description."),
                ]
            ),
            actions=[ft.TextButton("Close", on_click=lambda e: self.page.close(dlg))],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    # ---------- Toggle Cart ----------
    def toggle_cart(self, e):
        self.cart_panel.visible = not self.cart_panel.visible
        self.page.update()


# ---------- MAIN ----------
def main(page: ft.Page):
    ECommerceApp(page)


if __name__ == "__main__":
    ft.app(target=main)
