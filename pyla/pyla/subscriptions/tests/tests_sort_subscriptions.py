from django import test as django_test


def sort_subscription_by_len_of_features(subscriptions):
    subscriptions_features_new = {}
    while subscriptions:
        lowest_key = list(subscriptions.keys())[0]
        for key, value in subscriptions.items():
            if len(value) < len(subscriptions[lowest_key]):
                lowest_key = key
        new_value = subscriptions[lowest_key]
        subscriptions.pop(lowest_key)
        subscriptions_features_new[lowest_key] = new_value
    return subscriptions_features_new


class TestSort(django_test.TestCase):

    def test_if_correct_sort__expect_correct_list(self):
        sort_dict = {
            'middle': ['1', '2', '3'],
            'last': ['1', '2', '3', '4'],
            'first': ['1', '2'],
        }
        result = sort_subscription_by_len_of_features(sort_dict)
        expected = {
            'first': ['1', '2'],
            'middle': ['1', '2', '3'],
            'last': ['1', '2', '3', '4']
                    }
        self.assertEqual(expected, result)
