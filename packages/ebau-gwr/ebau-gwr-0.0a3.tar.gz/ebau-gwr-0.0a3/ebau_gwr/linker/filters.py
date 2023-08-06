import json

from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django_filters import Filter, FilterSet
from django_filters.constants import EMPTY_VALUES
from rest_framework.exceptions import ValidationError

from . import models


class JSONValueFilter(Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        valid_lookups = qs.model._meta.get_field(self.field_name).get_lookups()

        try:
            value = json.loads(value)
        except json.decoder.JSONDecodeError:
            raise ValidationError("JSONValueFilter value needs to be json encoded.")

        for expr in value:
            if expr in EMPTY_VALUES:  # pragma: no cover
                continue
            if not all(("key" in expr, "value" in expr)):
                raise ValidationError(
                    'JSONValueFilter value needs to have a "key" and "value" and an '
                    'optional "lookup" key.'
                )

            lookup_expr = expr.get("lookup", self.lookup_expr)
            if lookup_expr not in valid_lookups:
                raise ValidationError(
                    f'Lookup expression "{lookup_expr}" not allowed for field '
                    f'"{self.field_name}". Valid expressions: '
                    f'{", ".join(valid_lookups.keys())}'
                )
            # "contains" behaves differently on JSONFields as it does on TextFields.
            # That's why we annotate the queryset with the value.
            # Some discussion about it can be found here:
            # https://code.djangoproject.com/ticket/26511
            if isinstance(expr["value"], str):
                qs = qs.annotate(
                    field_val=KeyTextTransform(expr["key"], self.field_name)
                )
                lookup = {f"field_val__{lookup_expr}": expr["value"]}
            else:
                lookup = {
                    f"{self.field_name}__{expr['key']}__{lookup_expr}": expr["value"]
                }
            qs = qs.filter(**lookup)
        return qs


class GWRLinkFilterSet(FilterSet):
    context = JSONValueFilter(field_name="context")

    class Meta:
        model = models.GWRLink
        fields = ["eproid", "local_id", "context"]
