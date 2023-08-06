import iso8601
import mimetypes
import magic
import urllib.error
import urllib.parse
import urllib.request

from tala.model.person_name import PersonName
from tala.model.semantic_object import OntologySpecificSemanticObject, SemanticObject
from tala.model.image import Image
from tala.model.webview import Webview
from tala.model.date_time import DateTime

BOOLEAN = "boolean"
INTEGER = "integer"
DATETIME = "datetime"
REAL = "real"
STRING = "string"
IMAGE = "image"
DOMAIN = "domain"
WEBVIEW = "webview"
PERSON_NAME = "person_name"


class Sort(SemanticObject):
    def __init__(self, name, dynamic=False):
        self._name = name
        self._dynamic = dynamic

    def get_name(self):
        return self._name

    @property
    def name(self):
        return self._name

    def is_dynamic(self):
        return self._dynamic

    def is_builtin(self):
        return False

    def is_boolean_sort(self):
        return self._name == BOOLEAN

    def is_datetime_sort(self):
        return self._name == DATETIME

    def is_person_name_sort(self):
        return self._name == PERSON_NAME

    def is_real_sort(self):
        return self._name == REAL

    def is_integer_sort(self):
        return self._name == INTEGER

    def is_string_sort(self):
        return self._name == STRING

    def is_domain_sort(self):
        return self._name == DOMAIN

    def is_image_sort(self):
        return self._name == IMAGE

    def is_webview_sort(self):
        return self._name == WEBVIEW

    def __str__(self):
        return "Sort(%r, dynamic=%r)" % (self._name, self._dynamic)

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, (self._name, self._dynamic))

    def __eq__(self, other):
        try:
            return (other.get_name() == self.get_name() and other.is_dynamic() == self.is_dynamic())
        except AttributeError:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.get_name(), self.is_dynamic()))

    def value_as_basic_type(self, value):
        return value

    def value_as_json_object(self, value):
        return {"value": self.value_as_basic_type(value)}

    def value_from_basic_type(self, basic_value):
        return basic_value

    @classmethod
    def from_value(cls, value):
        if cls._is_float_value(value):
            return RealSort()
        if cls._is_boolean_value(value):
            return BooleanSort()
        if cls._is_integer_value(value):
            return IntegerSort()
        if isinstance(value, Image):
            return ImageSort()
        if isinstance(value, Webview):
            return WebviewSort()
        if cls._is_string_value(value):
            return StringSort()
        if isinstance(value, DateTime):
            return DateTimeSort()
        if isinstance(value, PersonName):
            return PersonNameSort()
        raise UnsupportedValue("Expected a supported value but got '%s'" % value)

    @classmethod
    def _is_float_value(cls, value):
        return isinstance(value, float)

    @classmethod
    def _is_integer_value(cls, value):
        return isinstance(value, int)

    @classmethod
    def _is_boolean_value(cls, value):
        try:
            BooleanSort().normalize_value(value)
        except InvalidValueException:
            return False
        return True

    @classmethod
    def _is_string_value(cls, value):
        try:
            StringSort().normalize_value(value)
        except InvalidValueException:
            return False
        return True


class UnsupportedValue(Exception):
    pass


class BuiltinSort(Sort):
    def is_builtin(self):
        return True

    def normalize_value(self, value):
        return value


class InvalidValueException(Exception):
    pass


class RealSort(BuiltinSort):
    def __init__(self):
        BuiltinSort.__init__(self, REAL)

    def normalize_value(self, value):
        try:
            return float(value)
        except (ValueError, AttributeError, TypeError):
            raise InvalidValueException("Expected a real-number value but got '%s'." % value)


class IntegerSort(BuiltinSort):
    def __init__(self):
        BuiltinSort.__init__(self, INTEGER)

    def normalize_value(self, value):
        try:
            return int(value)
        except (ValueError, AttributeError, TypeError):
            raise InvalidValueException("Expected an integer value but got '%s'." % value)


class StringSort(BuiltinSort):
    def __init__(self):
        BuiltinSort.__init__(self, STRING)

    def normalize_value(self, value):
        if isinstance(value, str):
            return value
        else:
            raise InvalidValueException(
                "Expected a string value but got %s of type %s." % (value, value.__class__.__name__)
            )


class ImageSort(BuiltinSort):
    def __init__(self):
        BuiltinSort.__init__(self, IMAGE)

    def normalize_value(self, value):
        if isinstance(value, Image):
            if isinstance(value.url, str) and "http" in value.url and self._has_mime_type(value.url, "image"):
                return value
            else:
                raise InvalidValueException("Expected an image URL but got '%s'." % value.url)
        else:
            raise InvalidValueException("Expected an image object but got '%s'." % value)

    def _has_mime_type(self, value, expected_mime_type):
        mime_type = self._get_mime_type_from_url(value)
        if mime_type:
            return mime_type.startswith(expected_mime_type + "/")
        else:
            return False

    def _get_mime_type_from_url(self, url):
        path = urllib.parse.urlparse(url).path
        mime_type, mime_subtype = mimetypes.guess_type(path)
        if not mime_type:
            try:
                filepath, _ = urllib.request.urlretrieve(url)
            except IOError:
                return None

            mime_type = magic.from_file(filepath, mime=True)
        return mime_type

    def value_as_basic_type(self, value):
        return value.url

    def value_from_basic_type(self, url):
        return Image(url)


class WebviewSort(BuiltinSort):
    def __init__(self):
        BuiltinSort.__init__(self, WEBVIEW)

    def normalize_value(self, value):
        if isinstance(value, Webview):
            if isinstance(value.url, str) and "http" in value.url:
                return value
            else:
                raise InvalidValueException("Expected a webview URL but got '%s'." % value.url)
        else:
            raise InvalidValueException("Expected a webview object but got '%s'." % value)

    def value_as_basic_type(self, value):
        return value.url

    def value_from_basic_type(self, url):
        return Webview(url)


class BooleanSort(BuiltinSort):
    def __init__(self):
        BuiltinSort.__init__(self, BOOLEAN)

    def normalize_value(self, value):
        if value is True or value is False:
            return value
        else:
            raise InvalidValueException("Expected a boolean value but got '%s'." % value)


class DomainSort(BuiltinSort):
    def __init__(self):
        BuiltinSort.__init__(self, DOMAIN)


class DateTimeSort(BuiltinSort):
    def __init__(self):
        BuiltinSort.__init__(self, DATETIME)

    def normalize_value(self, value):
        if isinstance(value, DateTime):
            try:
                iso8601.parse_date(value.iso8601_string)
            except iso8601.ParseError:
                raise InvalidValueException(
                    "Expected a datetime value in ISO 8601 format but got '%s'." % value.iso8601_string
                )
            return value
        else:
            raise InvalidValueException("Expected a datetime object but got '%s'." % value)

    def value_as_basic_type(self, value):
        return value.iso8601_string

    def value_from_basic_type(self, iso8601_string):
        return DateTime(iso8601_string)


class PersonNameSort(BuiltinSort):
    def __init__(self):
        super(PersonNameSort, self).__init__(PERSON_NAME)

    def normalize_value(self, value):
        if isinstance(value, PersonName):
            return value
        else:
            raise InvalidValueException("Expected a person name object but got %s of type %s." % (
                value, value.__class__.__name__)
            )

    def value_as_basic_type(self, value):
        return value.string

    def value_from_basic_type(self, string):
        return PersonName(string)


class CustomSort(Sort, OntologySpecificSemanticObject):
    def __init__(self, ontology_name, name, dynamic=False):
        Sort.__init__(self, name, dynamic=dynamic)
        OntologySpecificSemanticObject.__init__(self, ontology_name)

    def __eq__(self, other):
        try:
            return (Sort.__eq__(self, other) and self.ontology_name == other.ontology_name)
        except AttributeError:
            return False

    def __hash__(self):
        return hash((self.ontology_name, Sort.__hash__(self)))


class BuiltinSortRepository(object):
    _repository = {
        BOOLEAN: BooleanSort(),
        INTEGER: IntegerSort(),
        DATETIME: DateTimeSort(),
        REAL: RealSort(),
        STRING: StringSort(),
        IMAGE: ImageSort(),
        DOMAIN: DomainSort(),
        WEBVIEW: WebviewSort(),
        PERSON_NAME: PersonNameSort(),
    }

    @classmethod
    def has_sort(cls, name):
        return name in cls._repository

    @classmethod
    def get_sort(cls, name):
        if cls.has_sort(name):
            return cls._repository[name]
        else:
            raise UndefinedSort("Expected a built-in sort but got '%s'." % name)


class UndefinedSort(Exception):
    pass
