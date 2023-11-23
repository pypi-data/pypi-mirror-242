from django.apps import AppConfig


class VotingConfig(AppConfig):
    name = "modules.voting"
    verbose_name = "2. Голосования"
    plug_in = True

    def ready(self) -> None:
        from .signals import signaling_for_create_vote, get_instanse_before_save, signaling_for_delete_vote
            
