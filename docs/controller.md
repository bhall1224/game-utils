# Controller module `controller.py`

## VectorAction

>Extends TypeDict

This is a way to map a named action to a controller ID

### properties

- **input_id (int):** This is the unique ID of one input source from the controller.  For example, this could be *pygame.K_ESCAPE* for input from the keyboard.

- **action_type (str):** Options are `button`, `axis`, or `hat`.

- **action_name (str):** This is the unique name of your action to use in your progams.  This allows you to abstract the controller input from the actions to which you refer in your games.

### examples

```python
# a mapping of joystick axis 0 to an action called X_AXIS
vector_action = {
    "input_id": 0,
    "action_type": "axis",
    "action_name": "X_AXIS"
}
```

## Controller

Abstract class for controller. Must implement `direction` method. Optional `rotation` and `action` methods

### properties

- **speed (int | float):**

- **direction (() -> pygame.Vector2):**

- **rotation ((str) -> pygame.Vector2):**

- **action ((str) -> float):**

## ControllerHandler

Helper class for getting controllers. Implement abstract method `_new_controller_instance`. Class method 'get_controllers' will use it to make new controller instances

### properties

- **_new_controller_instance ((joy, int, *VectorAction, **VectorAction) -> Controller):**

- **get_controllers ((int, int | float) -> list[Controller])**

[back](../README.md)