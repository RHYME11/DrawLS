# DrawLS

GOAL: to create different types of level schemes based on input .txt files.

## Python Library Required
- `os` (part of Python's standard library, no need to install)
- `datetime` (part of Python's standard library, no need to install)

## Grace File Generator
All generator codes are written in python and saved in <u>build/agr_generator</u>. 
**States and associated excitation energies are required in alll formats.**

### Generator Type
|   Generator   | Agr Format | # of Isotopes | Frame    | Axis     | Gamma    | E<sub>&gamma;</sub>| Br       | Notes | 
|---------------|------------|---------------|----------|----------|----------|--------------------|----------|-------|
| generator1.py | empty1.agr | 1             | &#10007; | &#10007; | &#10007; | &#10007;           | &#10007; | ![image](https://github.com/user-attachments/assets/9ced337a-b115-4a7c-a26b-5e729ddeda13) |


### Empty Format:
| Format Name | X-axis Range | Notes         |
|-------------|--------------|---------------|
| empty1.agr  | [-0.5,1.0]   | One isotope   |
| empty2.agr  |              | Data 4   |
| emoty3.agr  |              | Data 6   |


### Python Codes (<u>build/agr_generator</u>)


