# sdmenu

**sdmenu** is a simple way to query UC San Diego's HDH dining halls.

![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)

## Installation

```bash
$ pip install sdmenu
Successfully installed sdmenu-1.0.0
```

## Example

This example is based off the menu for [64 Degrees](https://hdh-web.ucsd.edu/dining/apps/diningservices/Restaurants/MenuItem/64), which you can find [here](https://hdh-web.ucsd.edu/dining/apps/diningservices/Restaurants/MenuItem/64).

```py
>>> from sdmenu import menu
>>> my_menu = menu()
<menu {'64 Degrees', 'Cafe Ventanas', 'Canyon Vista', ...}>

>>> items = my_menu.get('64 Degrees')
[<menu_item 'Avocado Toast'>, <menu_item 'Bacon Bobcat Sandwich'>, ...]

>>> items[0].price
3.5

>>> my_menu.has('64 Degrees', 'Hibachi Chicken')
True
```
