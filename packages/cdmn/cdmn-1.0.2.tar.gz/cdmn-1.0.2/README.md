# cDMN

## Welcome to the cDMN solver's code repository.

cDMN stands for Constraint Decision and Model Notation.
It is an extension to the [DMN](https://www.omg.org/spec/DMN/About-DMN/) standard, managed by the Object Management Group (OMG).
cDMN combines the readability and straighforwardness of DMN and the expressiveness and flexibility of constraint reasoning.
For more specific details, please visit our [cDMN documentation](https://cdmn.readthedocs.io/en/latest/notation.html).

## Examples

Example implementations can also be found in the [cDMN documentation](https://cdmn.readthedocs.io/en/latest/examples.html).

## Installation and usage

The full installation and usage guide for the cDMN solver can be found [here](https://cdmn.readthedocs.io/en/latest/solver.html).
In short for Linux: after cloning this repo, install the Python dependencies.

```
git clone https://gitlab.com/EAVISE/cdmn/cdmn-solver
cd cdmn-solver
pip3 install -r requirements.txt
```

After this, you can run the solver. Example usage is as follows:

```
python3 -O solver.py Name_Of_XLSX.xlsx -n "Name_Of_Sheet" -o output_name.idp
```
