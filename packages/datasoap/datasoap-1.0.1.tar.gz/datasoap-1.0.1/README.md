# datasoap

## What is it?

datasoap is a supplementary library for pandas that processes dataframes derived from CSV files. The module checks cell data for correct numerical formatting and converts mismatched data to the correct data type (ex. str > float64).

## Main Features

- Strips unnecessary characters from numerical data fields in pandas dataframes to ensure consistent data formatting
- Provides before and after representations of dataframes to allow for comparison

## Repository

Source code is hosted on: [github.com/snake-fingers/data-soap](https://github.com/Snake-Fingers/datasoap)

## Dependencies

pandas - Python package that provides fast, flexible, and expressive data structures designed to make working with “relational” or “labeled” data both easy and intuitive.

## Installation

```
poetry add datasoap
```

## Documentation

Documentation to come.

## Background

datasoap originated from a Code Fellows 401 Python midterm project. The project team includes Alex Angelico, Grace Choi, Robert Carter, Mason Fryberger, and Jae Choi. After working with a few painful datasets using, we wanted to create a library that allows users to more efficiently manipulate clean datasets extracted from CSVs that may have inconsistent formatting.
