import pytest
from hamcrest import assert_that, has_length, equal_to, not_, contains_string

from trood.api.custodian.client import Client


@pytest.mark.integration
def test_like_operator(client, two_records):
    """
    Filter records with "like" operator
    """
    fist_record_name_substring = 'odo'
    assert_that(two_records[0].name, contains_string(fist_record_name_substring))
    assert_that(two_records[1].name, not_(contains_string(fist_record_name_substring)))
    records = client.records.query('person').filter(name__like='%{}%'.format(fist_record_name_substring))
    assert_that(records, has_length(1))
    assert_that(records[0].get_pk(), equal_to(two_records[0].get_pk()))



class TestRqlSeries:
    @pytest.mark.integration
    def test_eq_operator(self, client, two_records):
        """
        Filter records with "eq" operator
        """
        fist_record_name = 'Feodor'
        assert_that(two_records[0].name, equal_to(fist_record_name))
        assert_that(two_records[1].name, not_(equal_to(fist_record_name)))
        records = client.records.query('person').filter(name__eq=fist_record_name)
        assert_that(records, has_length(1))
        assert_that(records[0].get_pk(), equal_to(two_records[0].get_pk()))

    @pytest.mark.integration
    def test_in_operator(self, client, two_records):
        """
        Filter records with "in" operator
        """
        second_record_name = 'Victor'
        assert_that(two_records[0].name, not_(equal_to(second_record_name)))
        assert_that(two_records[1].name, equal_to(second_record_name))
        records = client.records.query('person').filter(name__in=['Valentine', second_record_name])
        assert_that(records, has_length(1))
        assert_that(records[0].get_pk(), equal_to(two_records[1].get_pk()))

    @pytest.mark.integration
    def test_ne_operator(self, client, two_records):
        """
        Filter records with "ne" operator
        """
        fist_record_name = 'Feodor'
        assert_that(two_records[0].name, equal_to(fist_record_name))
        assert_that(two_records[1].name, not_(equal_to(fist_record_name)))
        records = client.records.query('person').filter(name__ne=fist_record_name)
        assert_that(records, has_length(1))
        assert_that(records[0].get_pk(), equal_to(two_records[1].get_pk()))

    @pytest.mark.integration
    def test_gt_operator(self, client, two_records):
        """
        Filter records with "gt" operator
        """
        age_value = 30
        assert_that(two_records[0].age < age_value)
        assert_that(two_records[1].age > age_value)
        records = client.records.query('person').filter(age__gt=age_value)
        assert_that(records, has_length(1))
        assert_that(records[0].get_pk(), equal_to(two_records[1].get_pk()))

    @pytest.mark.integration
    def test_ge_operator(self, client, two_records):
        """
        Filter records with "ge" operator
        """
        age_value = 20
        assert_that(two_records[0].age == age_value)
        assert_that(two_records[1].age > age_value)
        records = client.records.query('person').filter(age__ge=age_value)
        assert_that(records, has_length(2))

    @pytest.mark.integration
    def test_lt_operator(self, client, two_records):
        """
        Filter records with "lt" operator
        """
        age_value = 30
        assert_that(two_records[0].age < age_value)
        assert_that(two_records[1].age > age_value)
        records = client.records.query('person').filter(age__lt=age_value)
        assert_that(records, has_length(1))
        assert_that(records[0].get_pk(), equal_to(two_records[0].get_pk()))

    @pytest.mark.integration
    def test_le_operator(self, client, two_records):
        """
        Filter records with "le" operator
        """
        age_value = 20
        assert_that(two_records[0].age == age_value)
        assert_that(two_records[1].age > age_value)
        records = client.records.query('person').filter(age__le=age_value)
        assert_that(records, has_length(1))
