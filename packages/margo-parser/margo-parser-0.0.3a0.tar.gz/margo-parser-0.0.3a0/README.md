# Margo note syntax

## What is Margo?

Margo is a syntax for adding features to computational notebook within code comments. For example, when using notebooks as source code modules, we need a simple way to ignore cells we do not want exported from the notebook. In a Python code cell, this might look like:

```python
# :: ignore-cell ::

print("This cell will not be exported by any code that imports this notebook.")
```

This statement is called a "note" in Margo. It is composed of the following parts:

`# ::` - **The Margo note prefix** differentiates this from a standard Python comment. This prefix is not part of the Margo syntax. It will vary from programming language to programming language, and it is up to the application that extracts Margo code to define how Margo notes are formatted. This double-colon syntax is the recommend method for prefixing Margo notes in Python. In TypeScript, it might look like `// ::`

`ignore-cell` - **The Margo note statement** is the substance of the Margo note. This statement might be understood by an application to not do anything with the cell. However, this specific statement is just an example. The Margo syntax does not reserve any keywords. It is up to application developers to do this for their own applications. For features where there is shared understanding of meaning, the developer community should reach a consensus about reserving keywords.

`::` - **The Margo endblock,** like the semicolon in C, signifies the end of a statement and it is required.

## Two types of statements

Statements fall into two categories: directives, and declarations.

### Directives

Directives are statements that have one fixed semantic meaning, such as `ignore-cell` in the example above. The keyword and its meaning are up to the application developer.

### Declarations

Declarations assign values to keywords, and they can be formatted a number of ways. Here is a basic example.

```python
# :: cell-id : "define-add-function" ::

def add(a, b):
    return a + b
```

The Margo note at the top of the above example cell declares the value of `cell-id` to be equal to `["define-add-function"]`. Note that this is an array of length 1, not a string.

We can generally describe the declaration syntax as:

`# :: NAME [ FORMAT ]: {VALUE}`

The **name** may contain alphanumeric characters as well as underscore and dash characters.

The **value** may be formatted several ways. The example above is called **Margo Value Format,** but values may also be defined as valid JSON or YAML strings as well.

The optional **format** specifier is not required in the example above. When absent, Margo Value Format is assumed. It can be set to `json` or `yaml` or `raw`.

#### Margo Value Format

Margo Value Format values are JSON arrays without the encapsulating square brackets `[` `]`. They may contain JSON scalar values: string, number, true, false and null. They may not contain collections (arrays or objects).

#### JSON and YAML formats

More complex structured data may be passed as JSON or YAML by using the format specifier. Other formats may be added in the future.

Let's imagine we want to use a notebook as a task in a data processing workflow, and we need to know what external files it requires as inputs, and what files it will generate.

```python
# :: notebook.task_interface [json]: '{
# :: "inputs": [
# ::    "populations.csv",
# ::    "virus-totals.csv"
# :: ],
# :: "outputs": [
# ::    "cases-per-capita.csv"
# :: ]}' ::
```

The same example in YAML would look like:

```python
# :: notebook.task_interface [yaml]:
# ::   inputs:
# ::     - populations.csv
# ::     - virust-totals.csv
# ::   outputs:
# ::     - cases-per-capita.csv
```

A more compact approach might be to stick to the Margo Value Format, making use of the fact that dots are allowed in the declaration name:

```python
# :: notebook.task_interface.inputs = "population.csv", "virus-totals.csv" ::
# :: notebook.task_interface.outputs = "cases-per-capita.csv" ::
```

#### Raw (plain text) format

Finally, unstructured data may be provided as a string. Let's envision a case where we want to specify all of the software dependencies for a notebook:

```python
# :: requirements.txt [raw]: '
# :: requests==2.2.5
# :: beautifulsoup4==4.9.3
# :: nltk==3.5
# :: ' ::
```

Note that no special characters are required to add line breaks to strings in Margo notes.
