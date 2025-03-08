# Physics module

```yaml
physics.py:
    PhysicsBody:
        "Applies physics to a GameSprite"
        - force: (pygame.Vector2, float) -> pygame.Vector2
            "applies acceleration to this body's mass over time"
        - move: (float) -> pygame.Vector2
            "displace this body over time"
        - on_collide: (PhysicsBody)
            "V`= (V(m-s) + U2s)/(m+s) for initial magnitudes Vm(self) and Us(other)"
        - momentum: () -> pygame.Vector2
            "This body's current momentum"
        - normal_force: () -> pygame.Vector3
            "(0, 0, mg)"
        - friction_force: () -> pygame.Vector3
            "fs * N if not in motion, else fk * N. Gives (0, 0, fN)"
```

---
[back](../README.md)