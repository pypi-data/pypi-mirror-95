import re

from tala.model.semantic_object import SemanticObject, OntologySpecificSemanticObject
from tala.utils.as_semantic_expression import AsSemanticExpressionMixin


class Individual(OntologySpecificSemanticObject, AsSemanticExpressionMixin):
    def __init__(self, ontology_name, value, sort):
        OntologySpecificSemanticObject.__init__(self, ontology_name)
        if sort.is_string_sort():
            value = self._strip_quotes(value)
        self.value = value
        self.sort = sort

    def getValue(self):
        return self.value

    def getSort(self):
        return self.sort

    def is_individual(self):
        return True

    def is_positive(self):
        return True

    def __eq__(self, other):
        try:
            if other.is_positive():
                return self.getValue() == other.getValue() and self.getSort() == other.getSort()
            else:
                return False
        except AttributeError:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.value, self.sort))

    def __str__(self):
        sort = self.getSort()
        if sort.is_string_sort():
            return '"%s"' % self.getValue()
        else:
            return str(self.getValue())

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, (self.getValue(), self.getSort()))

    def negate(self):
        return NegativeIndividual(self.ontology_name, self.value, self.sort)

    def _strip_quotes(self, string):
        m = re.search('^"([^"]*)"$', string)
        if m:
            string_content = m.group(1)
            return string_content
        else:
            return string

    def value_as_json_object(self):
        return self.sort.value_as_json_object(self.value)


class NegativeIndividual(Individual):
    def negate(self):
        return Individual(self.ontology_name, self.value, self.sort)

    def __str__(self):
        return "~%s" % self.getValue()

    def __eq__(self, other):
        try:
            if other.is_positive():
                return False
            else:
                otherValue = other.getValue()
                return self.getValue() == otherValue
        except AttributeError:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return super(NegativeIndividual, self).__hash__()

    def is_positive(self):
        return False


class Yes(SemanticObject, AsSemanticExpressionMixin):
    YES = "yes"

    def is_positive(self):
        return True

    def is_yes(self):
        return True

    def __str__(self):
        return Yes.YES

    def __eq__(self, other):
        try:
            return self.YES == other.YES
        except:  # noqa: E722
            return False

    def __ne__(self, other):
        try:
            return self.YES != other.YES
        except:  # noqa: E722
            return False

    def __hash__(self):
        return hash(str(self))


class No(SemanticObject, AsSemanticExpressionMixin):
    NO = "no"

    def is_positive(self):
        return False

    def is_no(self):
        return True

    def __str__(self):
        return No.NO

    def __eq__(self, other):
        try:
            return self.NO == other.NO
        except:  # noqa: E722
            return False

    def __ne__(self, other):
        try:
            return self.NO != other.NO
        except:  # noqa: E722
            return False

    def __hash__(self):
        return hash(str(self))
