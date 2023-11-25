from magictype import annotate_types

print('--- Magic Type ---')
print('Pass a code as str to annotate_types(code_here) and be happy :]')

# Test the function with a script
script = """def foo(bar:str, baz, qux=4):
    x = bar + baz
    return [4.3,2]
foo(3.2, "2.0", "3.4")
"""
print(annotate_types(script))