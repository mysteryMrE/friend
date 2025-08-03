# animation_factory.py
from pet_animations.idle import IdleAnimation
from pet_animations.idle_to_sleep import IdleToSleepAnimation
from pet_animations.sleep import SleepAnimation
from pet_animations.sleep_to_idle import SleepToIdleAnimation
from pet_animations.talk import TalkAnimation
from pet_animations.walk_left import WalkLeftAnimation
from pet_animations.walk_right import WalkRightAnimation


class AnimationFactory:
    """Factory to create and reuse animation instances"""

    _instances = {}

    @classmethod
    def get_animation(cls, animation_class):
        """Get a reusable animation instance"""
        class_name = animation_class.__name__
        if class_name not in cls._instances:
            cls._instances[class_name] = animation_class()
            # Reset cycle to 0 for fresh start
            cls._instances[class_name].cycle = 0
        else:
            # Reset the cycle for reuse
            cls._instances[class_name].cycle = 0
        return cls._instances[class_name]

    @classmethod
    def clear_instances(cls):
        """Clear all cached instances"""
        cls._instances.clear()
