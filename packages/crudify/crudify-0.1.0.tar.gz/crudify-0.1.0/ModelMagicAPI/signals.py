# ModelMagicAPI/signals.py

from django.apps import apps
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .utils import auto_discover_and_create_apis
from .utils import router as autoapi_router
from .exceptions import InvalidModelNameError

@receiver(post_migrate)
def discover_models(sender, **kwargs):
    """
    Signal handler to discover and create APIs for specified models after migrations.

    :param sender: The sender of the signal (AppConfig instance).
    :param kwargs: Additional keyword arguments.
    """
    if sender.name == 'ModelMagicAPI':
        user_models = getattr(settings, 'AUTO_API_USER_MODELS', None)

        try:
            if user_models:
                # Convert model names to actual model classes
                models_to_generate_apis = []
                for model in user_models:
                    model_class = apps.get_model(model)
                    if not model_class:
                        raise InvalidModelNameError(model)
                    models_to_generate_apis.append(model_class)
            else:
                # Exclude auto-created models
                models_to_generate_apis = [
                    model for model in apps.get_models(include_auto_created=False)
                ]

            # Discover and create APIs
            router = auto_discover_and_create_apis(models=models_to_generate_apis)
            autoapi_router.registry.extend(router.registry)
        except InvalidModelNameError as e:
            # Log or handle the error as needed
            raise
        except Exception as e:
            # Log or raise a more specific exception based on your requirements
            # For example:
            # logger.error(f"Error in discover_models: {e}")
            # raise CustomDiscoverModelsError("Failed to discover and create APIs.")

            # Or re-raise the exception if you want to see the traceback during development
            raise

    else:
        # Ignore the signal if it's not from 'ModelMagicAPI'
        pass
