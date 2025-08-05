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
