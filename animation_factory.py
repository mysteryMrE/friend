from mirror_mirror import MirrorMirror
from pet_states.listen import ListenAnimation
from pet_states.talk import TalkAnimation


class AnimationFactory:
    """Factory to create and reuse animation instances"""

    _pet = None

    @classmethod
    def set_pet(cls, pet):
        """Set the pet instance for the factory"""
        cls._pet = pet

    _instances = {}

    _mirror_mirror = MirrorMirror()

    @classmethod
    def setup_listen(cls):
        """Setup the listen animation"""
        if "ListenAnimation" in cls._instances:
            print("ListenAnimation already set up, skipping setup")
            return
        cls._instances["ListenAnimation"] = ListenAnimation()
        cls._instances["ListenAnimation"].cycle = 0

    @classmethod
    def get_animation(cls, animation_class):
        """Get a reusable animation instance"""
        # Always check for answers
        answer = None
        if (
            "ListenAnimation" in cls._instances
            and cls._instances["ListenAnimation"].has_last_message()
        ):
            listen_message = cls._instances["ListenAnimation"].get_last_message()
            answer = cls._mirror_mirror.get_answer(listen_message)
        if answer:
            if cls._mirror_mirror.is_directed_to_state():
                animation_class = cls._mirror_mirror.get_directed_state()
            else:
                animation_class = TalkAnimation
        elif "TalkAnimation" in cls._instances and cls._mirror_mirror.is_rebound():
            print("Hijacking TalkAnimation to ListenAnimation due to rebound")
            animation_class = ListenAnimation

        # animation_class = cls.handle_directed_transition(animation_class)
        # animation_class = cls.handle_talk_listen_transition_hijack(animation_class)
        class_name = animation_class.__name__
        if class_name not in cls._instances:
            if (
                class_name == "HideAnimation"
                or class_name == "LieDownAnimation"
                or class_name == "DieAnimation"
            ):
                cls._instances[class_name] = animation_class(cls._pet)
            else:
                cls._instances[class_name] = animation_class()
            # Reset cycle to 0 for fresh start
            cls._instances[class_name].cycle = 0
            if class_name == "TalkAnimation":
                cls._instances["TalkAnimation"].current_message = answer
        else:
            # Reset the cycle for reuse
            cls._instances[class_name].cycle = 0
            # Reset ListenAnimation state when reusing
            if hasattr(cls._instances[class_name], "message"):
                print("Reusing ListenAnimation instance, resetting state")
                cls._instances[class_name].message = None
                cls._instances[class_name].listening = False
                if hasattr(cls._instances[class_name], "start_listening"):
                    cls._instances[class_name].start_listening()

            # Reset TalkAnimation state when reusing
            if hasattr(cls._instances[class_name], "message_sent"):
                cls._instances[class_name].current_message = answer
                cls._instances[class_name].current_message_index = 0
                cls._instances[class_name].last_message_time = __import__("time").time()
                cls._instances[class_name].last_message = None
                cls._instances[class_name].message_sent = False
                cls._instances[class_name].tts_started = False
                cls._instances[class_name].message_chosen = False

            if class_name == "LieDownAnimation":
                cls._instances[class_name].adjust_frames("animation_factory")

        return cls._instances[class_name]

    @classmethod
    def clear_instances(cls):
        """Clear all cached instances"""
        cls._instances.clear()

    @classmethod
    def handle_directed_transition(cls, animation_class):
        bool_val, directed_state = cls._mirror_mirror.is_directed_to_state()
        if bool_val:
            print(f"Handling directed transition for class: {animation_class.__name__}")
            cls._instances[
                "ListenAnimation"
            ].get_last_message()  # delete last message, the message was used to determine the directed state, no need to get back to talking state
            return directed_state
        return animation_class

    @classmethod
    def handle_talk_listen_transition_hijack(cls, animation_class):
        print(f"Handling transition for class: {animation_class.__name__}")
        if (
            "ListenAnimation" in cls._instances
            and cls._instances["ListenAnimation"].has_last_message()
        ):
            print("Hijacking ListenAnimation to TalkAnimation   due to last message")
            return TalkAnimation
        elif "TalkAnimation" in cls._instances and cls._mirror_mirror.is_rebound():
            print("Hijacking TalkAnimation to ListenAnimation due to rebound")
            return ListenAnimation
        else:
            return animation_class

    @classmethod
    def handle_listen_talk_transition(cls):
        if (
            "ListenAnimation" in cls._instances
            and cls._instances["ListenAnimation"].has_last_message()
        ):
            listen_message = cls._instances["ListenAnimation"].get_last_message()
            answer = cls._mirror_mirror.get_answer(listen_message)
            if answer:
                cls._instances["TalkAnimation"].current_message = answer
                print(
                    f"Reusing TalkAnimation instance, giving listen message: {answer}"
                )
            else:
                print("Reusing TalkAnimation instance, no message from ListenAnimation")
