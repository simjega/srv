from os import getenv

from backend.env import Environment
from backend.secrets_util import get_secret

SECRETS_MANAGER_PREFIX = 'SECRETS_MANAGER_KEY_'
PREFIX_LEN = len(SECRETS_MANAGER_PREFIX)


def resolve(env_key, default=None, override=None):
    if override:
        return override

    env_value = getenv(env_key)
    if env_value:
        return env_value

    return default


def resolve_secret(env, env_key_for_secrets_manager_key, override=None):
    if override:
        return override

    secrets_manager_key_name = getenv(env_key_for_secrets_manager_key)
    if secrets_manager_key_name:
        return get_secret(secrets_manager_key_name)

    if env in [Environment.PRODUCTION, Environment.QA]:
        raise SecretKeyNameIsNone

    # fallback to non-secrets manager based env values in test / dev environments
    normal_key = env_key_for_secrets_manager_key[PREFIX_LEN:]
    normal_value = getenv(normal_key)

    if normal_value:
        return normal_value

    raise SecretKeyNameIsNone


def resolve_flask_env(env):
    if env == Environment.PRODUCTION or env == Environment.QA:
        return 'production'
    elif env == Environment.DEVELOPMENT:
        return 'development'
    elif env == Environment.TEST:
        return 'testing'
    else:
        raise FailedToResolveConfig


class FailedToResolveConfig(Exception):
    pass


class SecretKeyNameIsNone(Exception):
    pass
