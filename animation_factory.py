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

            # Reset ListenAnimation state when reusing
            if hasattr(cls._instances[class_name], "message"):
                cls._instances[class_name].message = None
                cls._instances[class_name].listening = False
                if hasattr(cls._instances[class_name], "start_listening"):
                    cls._instances[class_name].start_listening()

            # Reset TalkAnimation state when reusing
            if hasattr(cls._instances[class_name], "message_sent"):
                cls._instances[class_name].current_message = None
                cls._instances[class_name].current_message_index = 0
                cls._instances[class_name].last_message_time = __import__("time").time()
                cls._instances[class_name].last_message = None
                cls._instances[class_name].message_sent = False
                cls._instances[class_name].tts_started = False
                cls._instances[class_name].message_chosen = False

        return cls._instances[class_name]

    @classmethod
    def clear_instances(cls):
        """Clear all cached instances"""
        cls._instances.clear()
