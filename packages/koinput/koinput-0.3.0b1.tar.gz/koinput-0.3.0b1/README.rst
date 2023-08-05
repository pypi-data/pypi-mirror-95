.. image:: https://img.shields.io/pypi/v/koinput.svg
    :target: https://pypi.org/project/koinput/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/koinput.svg
    :target: https://pypi.org/project/koinput/
    :alt: Supported Python versions

.. contents:: Table of contents
   :depth: 3

koinput
=======

Maximal simplification of Input / Output for text programs.

`PyPI for releases <https://pypi.org/project/koinput/>`_ |
`Github for source <https://github.com/k0perX-X/koinput>`_

Installation
============

Requirements `colorama <https://pypi.org/project/colorama/>`_ library.

.. code-block:: bash

    pip install koinput

How to use
==========

Inputs
------

The library has two types of inputs:

* int_input
* float_input

They have the same settings and differ only in the type of output.

Explanation of input parameters
+++++++++++++++++++++++++++++++

.. code-block:: python

	def int_input(input_suggestion="", greater=float('-inf'), less=float('inf'), console_style=colorama.Fore.RESET,
		      error_message='Invalid number format.\n', error_message_style=colorama.Fore.RED,
		      input_is_greater_than_less_error="The number is greater than acceptable.\n",
		      input_is_less_than_greater_error="The number is less than acceptable.\n",
		      input_is_less_error_style=None, input_is_greater_error_style=None,
		      strictly_greater=True, strictly_less=True):


``input_suggestion=""``
	Input suggestion that will be displayed when the function is run.

``greater=float('-inf'), less=float('inf')``
	The range in which the entered number should be included.

``strictly_greater=True, strictly_less=True``
	Controlling the mathematical strictly of comparisons.

``console_style=colorama.Fore.RESET``
	Sets the base display style for the terminal. I recommend using the colorama library for easier style customization. You can also use standard sequences (example: "\x1b[39m").

``error_message='Invalid number format.\n'``
	Error message when converting input to number.

``error_message_style=colorama.Fore.RED``
	Error message style.

``input_is_greater_than_less_error="The number is greater than acceptable.\n"``
	The message issued when the number is greater than allowed.

``input_is_less_than_greater_error="The number is less than acceptable.\n"``
	The message issued when the number is less than allowed.

``input_is_less_error_style=None, input_is_greater_error_style=None``
	Out of range error styles.

Usage example
+++++++++++++

.. code-block:: python

    def area_triangle(base, height):
        return 0.5 * base * height

    print(area_triangle(float_input(input_suggestion='Enter the base of the triangle: '),
                        float_input(input_suggestion='Введите высоту треугольника: ')))

.. code-block:: python

	mas = [randint(0, 999) for i in range(int_input(input_suggestion="Enter the size of the array: "))]

Menu
----

The menu class is used to quickly create a text menu based on existing functions.

First, you need to create an instance of the class:

.. code-block:: python

	from koinput import Menu

	menu = Menu()

The next step is to add function calls to the menu. This can be done in 2 ways: using a decorator or a function.

.. code-block:: python

	@menu.add_to_menu_dec('Name shown in the menu', *arguments_passed_to_the_function)
	def z2(a, b, c):
		def area_circle(radius):
			return math.pi * radius ** 2

		print(area_circle(float_input(input_suggestion='Введите радиус круга: ')))

	OR

	def z2(a, b, c):
		def area_circle(radius):
			return math.pi * radius ** 2

		print(area_circle(float_input(input_suggestion='Введите радиус круга: ')))

	menu.add_to_menu('Name shown in the menu', z2, *arguments_passed_to_the_function)

Use the show_menu command to display the menu.

.. code-block:: python

	menu.show_menu(title=None, title_style=None, number_of_leading_spaces_title=2, console_style=Fore.RESET,
		       order_of_items=None, number_of_leading_spaces=4, separator=' - ', items_style=None,
		       input_suggestion='Select a menu item: ', enable_menu_item_exit=True, menu_item_exit='Exit',
		       exit_offer='Press Enter to exit...'):

``title=None``
	Menu title.

``title_style=None``
	Sets the title display style. I recommend using the colorama library for easier style customization. You can also use standard sequences (example: "\x1b[39m").

``number_of_leading_spaces_title=2``
	Sets the number of spaces before the menu title.

``console_style=Fore.RESET``
	Sets the base display style for the terminal. I recommend using the colorama library for easier style customization. You can also use standard sequences (example: "\x1b[39m").

``number_of_leading_spaces=4``
	Sets the number of spaces before the menu items.

``separator=' - '``
	Separator between number and menu item name.

``items_style=None``
	Sets the menu item display style.

``input_suggestion='Select a menu item: '``
	Input suggestion at the end of the menu.

``enable_menu_item_exit=True``
	Enabling the menu item exit. If False, then after selecting one of the items the menu will close.

``menu_item_exit='Exit'``
	The name of the menu exit item.

``exit_offer='Press Enter to exit...'``
	Exit message.

``order_of_items=None``
	Custom order of issuing menu items. It is either a tuple of int or a tuple of str. A tuple of int must contain the ordinal numbers of items starting from 0 (the numbers are given in the order in which they are declared). The str tuple must contain the names of the menu items in the order they appear.

Change the function of output from the menu.

This is necessary when you do not need an exit confirmation or when you exit you need to launch another menu or some function.

Example with disabling the exit confirmation:

.. code-block:: python

	@menu.reassign_menu_exit()
	def menu_exit(exit_offer):
		def f():
			pass

		return f

Example with displaying another menu:

.. code-block:: python

	@menu.reassign_menu_exit()
	def menu_exit(exit_offer):
		def f():
			menu2.show_menu(title='MENU', title_colour=colorama.Fore.BLUE, enable_menu_item_exit=False)

		return f

Usage example
+++++++++++++

.. code-block:: python

	import math
	from koinput import float_input, Menu
	import colorama

	menu = Menu()


	@menu.add_to_menu_dec('Площадь треугольника')
	def z1():
		def area_triangle(base, height):
			return 0.5 * base * height

		print(area_triangle(float_input(input_suggestion='Введите основание треугольника: '),
				    float_input(input_suggestion='Введите высоту треугольника: ')))


	@menu.add_to_menu_dec('Площадь круга')
	def z2():
		def area_circle(radius):
			return math.pi * radius ** 2

		print(area_circle(float_input(input_suggestion='Введите радиус круга: ')))


	@menu.add_to_menu_dec('Расстояние от точки до точки')
	def z3():
		def distance(x1, y1, x2, y2):
			return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

		print(distance(float_input(input_suggestion='Введите X первой точки: '),
			       float_input(input_suggestion='Введите Y первой точки: '),
			       float_input(input_suggestion='Введите X второй точки: '),
			       float_input(input_suggestion='Введите Y второй точки: ')))


	def z4():
		def capitalize_word(word):
			return word[0].upper() + word[1::]

		def capitalize_string(s):
			ss = s.split()
			for word in ss:
				s = s.replace(word, capitalize_word(word))
			return s

		print('Введите строку для изменения: ')
		print(capitalize_string(input()))


	@menu.reassign_menu_exit()
	def menu_exit(exit_offer):
		def f():
			pass

		return f


	def main():
		menu.add_to_menu('Capitalize', z4)
		menu.show_menu(title='МЕНЮ', title_colour=colorama.Fore.BLUE)


	if __name__ == '__main__':
		main()


