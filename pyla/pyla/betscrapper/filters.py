import django_filters
import pyla.betscrapper.models as bet_models


class MatchesFilter(django_filters.FilterSet):
    CHOICES = (
        ('from lowest', 'From lowest'),
        ('from highest', 'From highest')
    )
    ordering = django_filters.ChoiceFilter(label='Odds', choices=CHOICES, method='filter_by_order')
    paginate_by = 1
    class Meta:
        model = bet_models.BetMatch
        fields = {'bookmaker': ['icontains'],
                  'date': ['icontains'],
                  'liga': ['icontains'],
                  }

    def filter_by_order(self, queryset, name, value):
        expression = 'odds' if value == 'from lowest' else '-odds'

        return queryset.order_by(expression)
