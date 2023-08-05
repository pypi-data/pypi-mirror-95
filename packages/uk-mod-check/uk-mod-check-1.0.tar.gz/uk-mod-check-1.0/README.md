# A python library for checking the validitiy of UK bank account details

Example usage:

```python
import uk_mod_check

assert uk_mod_check.validate( 40004, 78111815) == uk_mod_check.ValidationResult(result=True, known_sort_code=True, substitute_sort_code=None)
assert uk_mod_check.validate(309070, 12345668) == uk_mod_check.ValidationResult(result=True, known_sort_code=True, substitute_sort_code=309634)
```
