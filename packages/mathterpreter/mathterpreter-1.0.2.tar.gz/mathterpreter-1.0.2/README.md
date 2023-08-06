# mathterpreter

#### A lightweight and basic maths interpreter

## Example usage

Basic usage

```python
from mathterpreter import interpret

print(interpret("54-3*(2+1)-3"))
```

Step by step
```python
from mathterpreter import Lexer, Parser

lexer = Lexer("54-3*(2+1)-3")
tokens = lexer.tokenize()
parser = Parser(tokens)
tree = parser.parse()
result = tree.evaluate()
print(result)
```

Command line
```shell script
python3 -m mathterpreter 54-3*(2+1)-3
# or
echo 54-3*(2+1)-3 | python3 -m mathterpreter
```
