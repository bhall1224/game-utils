# Vector Utils module `vector_utils.py`

## get_random_vector 

### args

- **scalar_mag: int = 1**

- **non_negative: bool = False**

### returns pygame.Vector2

Returns a `pygame.Vector2` with random values for x and y.  Scaled by given `scalar_mag`.  Uses only >=0 if `non_negative` is flagged

## apply

### args

- **vector (pygame.Vector2):** The vector to which changes are applied

- ***actions (pygame.Vector2):** Actions to apply.  (pygame.Vector2) -> pygame.Vector2

### returns pygame.Vector2

The `pygame.Vector2` after all actions have been applied



[back](../README.md)