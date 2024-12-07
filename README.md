# DrawLS

GOAL: to create different types of level schemes based on input .txt files.

## Python Library Required
- `os` (part of Python's standard library, no need to install)
- `datetime` (part of Python's standard library, no need to install)

## Grace File Generator
All generator codes are written in python and saved in <u>build/agr_generator</u>.</br> 
**States and associated excitation energies are required in alll formats.**

### Generator Type
| # of Isotopes | Format | Frame    | Axis     | EX              | Jpi            |Gamma    | E<sub>&gamma;</sub>| Br       | Notes | 
|---------------|--------|----------|----------|-----------------|----------------|---------|--------------------|----------|
| 1             | 1      | &#10007; | &#10007; | &#10004;(Right) | &#10004;(Left) data/P29.dat|&#10007; |&#10007;            | &#10007; | ![image](https://github.com/user-attachments/assets/9ced337a-b115-4a7c-a26b-5e729ddeda13) |
| 2             | 1      | &#10007; | &#10007; | &#10004;(1@Right,2@Left) | &#10004;(1@Left,2@Right) data/P29.dat|&#10007; |&#10007;            | &#10007; | ![image](https://github.com/user-attachments/assets/9ced337a-b115-4a7c-a26b-5e729ddeda13) |


### Python Codes (<u>build/agr_generator</u>)


