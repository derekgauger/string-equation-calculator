"""
Author: Derek Gauger
Date: 07/27/2022
Purpose: Bitnine Apache AGE 2022 Internship Program Coding Round
Description:
This is a calculator for addition and subtraction equations. It allows for parentheses, multi-layered parentheses,
and negative numbers. There is an upper and lower bound on the numbers at 100,000,000 and -100,000,000 respectively.
On the coding assignment sheet, it says to make the program exit on press of the escape key and the '0' key.
I decided against adding a pip library dependency to this project, so to exit do one of the following:
 - Leave the input empty
 - Put just a '0' in the input
 - Type 'esc' in the input
 - type 'escape' in the input
"""
import re


# This method takes in an equation and finds the numbers and symbols associated with that equation
# A ValueError exception is raised when violating the -100 mil - 100 mil bounds.
# Returns two lists - Numbers: List of numbers in the equation, Symbols: List of symbols in the equation
def get_numbers_and_symbols(equation):

    numbers = re.findall(r'(-?\w+)', equation)
    symbols = re.findall(r'-?\d+\s*([+-])', equation)

    for number in numbers:
        if int(number) > 100000000 or int(number) < -100000000:
            raise ValueError("Input numbers cannot exceed 100,000,000")

    return numbers, symbols


# The method for calculating the value of the numbers and symbols given as an argument
# It keeps a running total for the calculated value
# Returns the calculated_value variable that contains the total value
def calculate(numbers, symbols):

    # Set the original value to the first number in the equation
    calculated_value = int(numbers[0])

    # for loop for calculating the values
    for i in range(1, len(numbers)):

        num = int(numbers[i])
        operation = symbols[i - 1]

        if operation == '+':
            calculated_value += num
        elif operation == '-':
            calculated_value -= num

    return calculated_value


# main method for parsing the parenthesis
def parse_parentheses(equation):
    # Gets the indices of the parentheses at the lowest level possible
    open_para, closed_para = find_next_parentheses(equation)

    # If the parentheses indices are 0, it means there are no more parentheses in the equation
    if open_para == 0 and closed_para == 0:
        return equation

    # Create a substring that represents the equation inside the parentheses
    parentheses_substring = equation[open_para:closed_para + 1]

    # Get the numbers and symbols from the parentheses equation
    numbers, symbols = get_numbers_and_symbols(parentheses_substring)

    # Calculate the value of the sub equation
    calculated_value = calculate(numbers, symbols)

    # Replace the parentheses equation with that of the calculated value to make a new more readable equation
    new_equation = equation.replace(parentheses_substring, str(calculated_value))

    # Call this method again with the new equation until we get an equation without parentheses
    return parse_parentheses(new_equation)


# Get the pair of parentheses
# Returns the indices of the next open and close parenthesis for evaluating
def find_next_parentheses(equation):

    open_para_index = 0
    close_para_index = 0

    # Find the last open parenthesis
    for i in range(len(equation)):

        if equation[i] == "(":
            open_para_index = i

    # Find the next close parenthesis after the last open parenthesis
    for i in range(open_para_index, len(equation)):

        if equation[i] == ")":
            close_para_index = i
            break

    return open_para_index, close_para_index


# Parses the equation given
# Returns the equations calculated resultant value
def parse_input(equation):

    check_equation(equation)

    # Deals with parentheses and keeps calculating values until there are no longer any parentheses
    equation = parse_parentheses(equation)

    # Gets the numbers and symbols in the final equation
    numbers, symbols = get_numbers_and_symbols(equation)

    # Calculate the resulting value for outputting
    result = calculate(numbers, symbols)

    return result


def check_equation(equation):
    open_para_count = equation.count('(')
    close_para_count = equation.count(')')

    if open_para_count != close_para_count:
        raise ArithmeticError("There must be an equal number of '(' and ')' in the equation")

    for char in equation:
        if not char.isdigit() and (char != "(" or char != ")"):
            raise ArithmeticError("Invalid character '{}' in equation".format(char))


# Main method
def main():

    while True:
        equation = input("Input: ")
        # Round-a-bout way of not having to add a pip library dependency to the project
        if equation.lower() == '0' or equation == "" or equation.lower() == 'esc' or equation.lower() == 'escape':
            break

        result = parse_input(equation)
        print("Output: {}\n".format(result))


main()
