import json
import datetime

from pathlib import Path

from tala.nl.languages import SUPPORTED_RASA_LANGUAGES


class ConfigNotFoundException(Exception):
    def __init__(self, message, config_path):
        self._config_path = config_path
        super(ConfigNotFoundException, self).__init__(message)

    @property
    def config_path(self):
        return self._config_path


class BackendConfigNotFoundException(ConfigNotFoundException):
    pass


class DddConfigNotFoundException(ConfigNotFoundException):
    pass


class DeploymentsConfigNotFoundException(ConfigNotFoundException):
    pass


class UnexpectedConfigEntriesException(Exception):
    pass


class UnexpectedRASALanguageException(Exception):
    pass


class MissingMandatoryConfigEntryException(Exception):
    pass


class AbstractConfigFieldDefinition(object):
    @property
    def optional(self):
        raise NotImplementedError()


class OptionalConfigField(AbstractConfigFieldDefinition):
    def __init__(self, default_value):
        self._default_value = default_value

    @property
    def optional(self):
        return True

    @property
    def default_value(self):
        return self._default_value


class MandatoryConfigField(AbstractConfigFieldDefinition):
    @property
    def optional(self):
        return False


class Config(object):
    def __init__(self, path=None):
        path = path or self.default_name()
        self._path = Path(path)

    @property
    def _absolute_path(self):
        return Path.cwd() / self._path

    @classmethod
    def default_config(cls, **kwargs):
        def get_value(key, field_definition):
            if key in kwargs:
                return kwargs[key]
            elif field_definition.optional:
                return field_definition.default_value
            else:
                raise MissingMandatoryConfigEntryException(
                    f"Expected mandatory entry '{key}' but it is missing among entries {list(kwargs.keys())}.")
        return {key: get_value(key, field_definition) for key, field_definition in cls.fields().items()}

    def read(self):
        if not self._path.exists():
            self._handle_non_existing_config_file()
        self._potentially_update_and_backup_config()
        config = self._config_from_file()
        config = self._potentially_update_with_values_from_parent(config)
        self._raise_exception_if_mandatory_field_is_missing(config)
        self._set_default_values_for_missing_optional_entries(config)
        return config

    def _handle_non_existing_config_file(self):
        self._raise_config_not_found_exception()

    def _write(self, config):
        self._write_to_file(config, self._path)

    @classmethod
    def write_default_config(cls, path=None, **kwargs):
        path = path or cls.default_name()
        cls._write_to_file(cls.default_config(**kwargs), Path(path))

    def _write_backup(self, config):
        path = Path(self.back_up_name())
        self._write_to_file(config, path)

    @staticmethod
    def _write_to_file(config, path):
        with path.open(mode="w") as f:
            string = json.dumps(config, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
            f.write(str(string))

    def _config_from_file(self):
        with self._path.open(mode="r") as f:
            return json.load(f)

    def _raise_exception_if_mandatory_field_is_missing(self, config):
        for key, field_definition in self.fields().items():
            if not field_definition.optional and key not in config:
                raise MissingMandatoryConfigEntryException(
                    f"Expected mandatory entry '{key}' in '{self._path}' but it is missing among entries "
                    f"{list(config.keys())}.")

    def _potentially_update_and_backup_config(self):
        config = self._config_from_file()
        config = self._potentially_update_with_values_from_parent(config)
        expected_entries = set(self.fields().keys())
        expected_entries.add("overrides")
        unexpected_entries = sorted(set(config.keys()).difference(expected_entries))
        if unexpected_entries:
            self._write_backup(config)
            self._write(config)
            raise UnexpectedConfigEntriesException(
                f"Parameters {unexpected_entries} are unexpected in '{self._absolute_path}'. "
                f"The config was updated and the previous config was backed up in '{self.back_up_name()}'.")

    def _potentially_update_with_values_from_parent(self, config):
        parent_path = config.get("overrides")
        if parent_path:
            config = self._update_with_values_from_parent(config, parent_path)
        return config

    def _update_with_values_from_parent(self, config, parent_path):
        parent_config_object = self.__class__(parent_path)
        parent_config = parent_config_object.read()
        parent_config.update(config)
        return parent_config

    def _set_default_values_for_missing_optional_entries(self, config):
        for key, field_definition in self.fields().items():
            if field_definition.optional and key not in config:
                config[key] = field_definition.default_value

    def back_up_name(self):
        return "{}.backup".format(self._path)

    @staticmethod
    def default_name():
        raise NotImplementedError()

    @staticmethod
    def fields():
        raise NotImplementedError()

    def _raise_config_not_found_exception(self):
        raise NotImplementedError()


class BackendConfig(Config):
    DEFAULT_RERANK_AMOUNT = 0.2
    DEFAULT_INACTIVE_SECONDS_ALLOWED = datetime.timedelta(hours=2).seconds
    DEFAULT_RESPONSE_TIMEOUT = 2.5

    @staticmethod
    def default_name():
        return "backend.config.json"

    @staticmethod
    def fields():
        return {
            "ddds": MandatoryConfigField(),
            "active_ddd": MandatoryConfigField(),
            "supported_languages": MandatoryConfigField(),
            "asr": OptionalConfigField(default_value="none"),
            "use_recognition_profile": OptionalConfigField(default_value=False),
            "repeat_questions": OptionalConfigField(default_value=True),
            "use_word_list_correction": OptionalConfigField(default_value=False),
            "rerank_amount": OptionalConfigField(default_value=BackendConfig.DEFAULT_RERANK_AMOUNT),
            "inactive_seconds_allowed": OptionalConfigField(
                default_value=BackendConfig.DEFAULT_INACTIVE_SECONDS_ALLOWED),
            "response_timeout": OptionalConfigField(default_value=BackendConfig.DEFAULT_RESPONSE_TIMEOUT)
        }

    def _set_default_values_for_missing_optional_entries(self, config):
        if "use_word_list_correction" not in config:
            config["use_word_list_correction"] = (config.get("asr") == "android")
        super(BackendConfig, self)._set_default_values_for_missing_optional_entries(config)

    @classmethod
    def write_default_config(cls, ddd_name, path=None, language="eng"):
        path = path or cls.default_name()
        ddd_name = ddd_name or ""
        cls._write_to_file(cls.default_config(
            ddds=[ddd_name],
            active_ddd=ddd_name,
            supported_languages=[language]),
            Path(path))

    def _raise_config_not_found_exception(self):
        raise BackendConfigNotFoundException(
            "Expected backend config '{}' to exist but it was not found.".format(self._absolute_path),
            self._absolute_path
        )


class DddConfig(Config):
    @staticmethod
    def default_name():
        return "ddd.config.json"

    @staticmethod
    def fields():
        return {
            "use_rgl": MandatoryConfigField(),
            "use_third_party_parser": OptionalConfigField(default_value=False),
            "device_module": OptionalConfigField(default_value=None),
            "word_list": OptionalConfigField(default_value="word_list.txt"),
            "rasa_nlu": OptionalConfigField(default_value={}),
        }

    def _raise_config_not_found_exception(self):
        raise DddConfigNotFoundException(
            "Expected DDD config '{}' to exist but it was not found.".format(self._absolute_path), self._absolute_path
        )

    def read(self):
        config = super(DddConfig, self).read()
        self._validate_rasa_nlu_language(config["rasa_nlu"])
        self._validate_rasa_nlu(config["rasa_nlu"])
        return config

    def _validate_rasa_nlu_language(self, config):
        for language in list(config.keys()):
            if language not in SUPPORTED_RASA_LANGUAGES:
                raise UnexpectedRASALanguageException(
                    "Expected one of the supported RASA languages {} in DDD config '{}' but got '{}'.".format(
                        SUPPORTED_RASA_LANGUAGES, self._absolute_path, language
                    )
                )

    def _validate_rasa_nlu(self, config):
        def message_for_missing_entry(parameter, language):
            return "Parameter '{parameter}' is missing from 'rasa_nlu.{language}' in DDD config '{file}'." \
                .format(parameter=parameter, language=language, file=self._absolute_path)

        def message_for_unexpected_entries(parameters, language):
            return "Parameters {parameters} are unexpected in 'rasa_nlu.{language}' of DDD config '{file}'." \
                .format(parameters=parameters, language=language, file=self._absolute_path)

        for language, rasa_nlu in list(config.items()):
            if "url" not in rasa_nlu:
                raise UnexpectedConfigEntriesException(message_for_missing_entry("url", language))
            if "config" not in rasa_nlu:
                raise UnexpectedConfigEntriesException(message_for_missing_entry("config", language))
            unexpecteds = set(rasa_nlu.keys()) - {"url", "config"}
            if any(unexpecteds):
                raise UnexpectedConfigEntriesException(message_for_unexpected_entries(list(unexpecteds), language))


class DeploymentsConfig(Config):
    @staticmethod
    def default_name():
        return "deployments.config.json"

    @staticmethod
    def fields():
        return {
            "dev": OptionalConfigField(default_value="https://127.0.0.1:9090/interact")
        }

    def _raise_config_not_found_exception(self):
        message = "Expected deployments config '{}' to exist but it was not found.".format(self._absolute_path)
        raise DeploymentsConfigNotFoundException(message, self._absolute_path)

    def _potentially_update_and_backup_config(self):
        pass

    def get_url(self, candidate_deployment):
        if not self._path.exists():
            return candidate_deployment
        config = self.read()
        if candidate_deployment in config:
            return config[candidate_deployment]
        return candidate_deployment


class OverriddenDddConfig(object):
    def __init__(self, ddd_name, path):
        self._ddd_name = ddd_name
        self._path = path

    @property
    def ddd_name(self):
        return self._ddd_name

    @property
    def path(self):
        return self._path
