##############################################
### HERE TO TEST FUNCTIONS IN utils BLOCKS ###
##############################################

# Using pytest assertions
def add(a,b):
    return a+b

def test_addition():
    result = add(1, 2)
    assert result == 3, f"Expected 3, but got {result}"
