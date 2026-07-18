from numpy.random import normal, rand, choice
from pygame import Vector3



class PhysicsBody:
    """Applies physics to a GameSprite"""
    
    GRAVITY_METRIC = 9.8

    def __init__(
        self,
        mass: float,
        position: Vector3,
        /,
        friction: float = 0.0,
        elasticity: float = 0.0,
        slip: float | None = None,
        velocity: Vector3 = Vector3(0.0, 0.0, 0.0),
        gravity: Vector3 | None = None
    ):
        """Initialize a configured physics body for a sprite.
        This class will hold physics data about the object, and apply
        other vectors to it.  Access to properties are given, but only
        properties velocity and position are read-write access.  All others
        are read-only.  A constant for gravity is given as a float for 9.8 m/s^2

        Args:
            mass (float, optional): The mass of this body.
            position (Vector3): The initial position of this body
            friction (float, optional): Coefficient for static friction. Defaults to 0.0 (no friction)
            elasticity (float, optional): Energy loss from collisions. Defaults to 0.0 (no elasticity)
            slip (float, optional): Change in resistance for kinetic friction. Defaults to 0.0 (no slip)
            velocity (Vector3, optional): Initial velocity of this body. Defaults to (0.0, 0.0, 0.0).
        """
        self.__mass = mass
        self.__position = position.copy()
        
        # Elasticity l, given as 0 means no friction should be applied.
        # If no elasticity, this should not affect the loss of energy.
        # Used for calculating loss of energy in collisions, 1 has no effect
        self.__elasticity = 1.0 - elasticity

        # calculate kinetic friction
        # same principle as elasticity for friction and slip
        self.__static_friction = 1.0 - friction
        slip = 1.0 - slip
        slip = normal(loc=slip)
        self.__kinetic_friction = self.__static_friction * slip

        # set or generate initial velocity,
        # and a default acceleration vector for gravity
        self.__velociy = velocity.copy()
        self.__gravity = gravity or Vector3(0.0, 0.0, self.GRAVITY_METRIC)

    def apply_force(self, acceleration: Vector3, dtime: float) -> Vector3:
        """Apply an acceleration to this body's mass over time.  Updates this body's velocity and
        returns the force applied

        Args:
            acceleration (Vector3): The three-dimensional vector for the acceleration
            dtime (float): The change in time

        Returns:
            Vector3: The force applied to this body
        """
        new_velocity = acceleration * dtime
        new_force = acceleration * self.mass

        if new_force.magnitude() > self.friction_force().magnitude():
            self.__velociy += new_velocity
        else:
            self.__velociy -= self.__velociy * self.friction_force().magnitude() * dtime

        return new_force

    def move(self, dtime: float) -> Vector3:
        """Apply this body's velocity to its position over time, which updates
        this body's position vector.

        Args:
            dtime (float): The change in time

        Returns:
            Vector3: The new position of this body
        """
        new_position = self.__velociy * dtime
        self.__position += new_position

        return new_position

    def on_collide(self, other):
        """Calculates collision with other physics body,
        and loss of energy from this body's elasticity.

        For V, m for this body's velocity and mass; and U, s for other body's 
        velocity and mass; final velocity is given by:

        Vf = (Vi(m - s) + 2Us)/(m + s) * l

        Where Vi is this body's initial velocity, and l this body's elasticity

        Args:        
            other (object): The object with which this body has collided
        """
        if not isinstance(other, PhysicsBody):
            return

        # Vf = (Vi(m - s) + 2Us)/(m + s)
        # Vi * (m - s)
        self.__velociy *= self.__mass - other.mass()

        # + 2Us
        self.__velociy += 2 * other.momentum()

        # / (m + s)
        self.__velociy /= self.__mass + other.mass()

        # energy loss, if any
        self.__velociy *= self.__elasticity

    def momentum(self) -> Vector3:
        """This body's current momentum

        Returns:
            Vector3: Vm of this body
        """
        return self.__velociy * self.mass

    def normal_force(self) -> Vector3:
        """The normal force of this body

        Returns:
            Vector3: The force of gravity * the mass of this body
        """
        return self.__mass * self.__gravity

    def friction_force(self) -> Vector3:
        """fs * N if not in motion, else fk * N

        Returns:
            Vector3: (0, 0, fN)
        """
        return (
            self.__static_friction * self.normal_force()
            if self.__velociy.magnitude() == 0.0
            else self.__kinetic_friction * self.normal_force()
        )

    def mass(self) -> float:
        return self.__mass

    def velocity(self) -> Vector3:
        return self.__velociy

    def position(self) -> Vector3:
        return self.__position

    def static_friction(self):
        return self.__static_friction

    def kinetic_friction(self):
        return self.__kinetic_friction

    def elasticity(self):
        return self.__elasticity
    
    def set_position(self, new_pos: Vector3):
        self.__position = new_pos

    def set_velocity(self, new_vel: Vector3):
        self.__velociy = new_vel

    def __str__(self) -> str:
        return str(self.__position)
    
def get_random_vector(scalar_mag: float = 1.0, non_negative: bool = False) -> Vector3:
    def rand_sign() -> int:
        return choice([-1, 1]) if not non_negative else 1

    return Vector3(
        x=rand() * rand_sign() * scalar_mag,
        y=rand() * rand_sign() * scalar_mag,
        z=rand() * rand_sign() * scalar_mag
    )