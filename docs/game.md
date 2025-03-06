# Game module

```yaml
controller.py:
    VectorAction:
        Mapping of controller ID to action
        - input_id: int
        - action_type: str
        - action_name: str
    Controller:
        Abstract class for controller
        Must implement 'direction' method
        Optional rotation and action methods
        - speed: int | float
        - direction: () -> pygame.Vector2
        - rotation: (str) -> pygame.Vector2
        - action: (str) -> float
    ControllerHandler:
        Helper class for getting controllers
        Implement abstract method _new_controller_instance
        Class method 'get_controllers' will use it to make new controller instances
        - _new_controller_instance: (joy, int, *VectorAction, **VectorAction) -> Controller
        - get_controllers: (int, int | float) -> list[Controller]
```

---

[back](../README.md)