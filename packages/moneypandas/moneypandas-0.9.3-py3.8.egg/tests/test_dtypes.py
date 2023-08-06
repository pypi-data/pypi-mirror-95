import pytest
from moneypandas import dtypes


def test_find_currency_data():
    """
    Testing the output from the method
    """
    result = dtypes.find_currency_data()
    expected = {
        '＄': 'ARS', '﹩': 'ARS', '$': 'ARS', '￡': 'FKP', '₭': 'LAK',
        '£': 'FKP', '￦': 'KPW', '￥': 'CNY', '﷼': 'IRR', '₾': 'GEL',
        '₽': 'RUB', '₼': 'AZN', '₺': 'TRY', '₹': 'INR', '₸': 'KZT',
        '₵': 'GHS', '₴': 'UAH', '₲': 'PYG', '₱': 'CUP', '₮': 'MNT',
        '€': 'EUR', '₫': 'VND', '₪': 'ILS', '₩': 'KPW', '₨': 'LKR',
        '₦': 'NGN', '₡': 'CRC', '៛': 'KHR', '฿': 'THB', '৳': 'BDT',
        '؋': 'AFN', '֏': 'AMD', '¥': 'CNY', '¢': 'GHS'
    }
    assert result == expected


def test_find_currency_data_type():
    "checking the type returned is a dictionary"
    expected_result = dict
    result = type(dtypes.find_currency_data())
    assert result == expected_result
