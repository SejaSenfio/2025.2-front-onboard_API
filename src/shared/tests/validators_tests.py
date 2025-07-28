import pytest

from shared.validators import (
    validate_cnpj,
    validate_latitude,
    validate_longitude,
    validate_mac_address,
    validate_non_empty_string,
)


class TestsCnpjValidator:
    @pytest.mark.parametrize(
        "cnpj",
        [
            "11.518.191/000102",
            "11518191000102",
            "11518191/000102",
        ],
    )
    def test_should_raise_value_error_when_cnpj_is_invalid(self, cnpj):
        with pytest.raises(ValueError) as exc:
            validate_cnpj(cnpj)
        assert "CNPJ inválido" in str(exc)

    def test_should_return_valid_cnpj(self):
        cnpj = "11.518.191/0001-02"
        assert validate_cnpj(cnpj) == cnpj


class TestLatitudeLongitudeValidators:
    @pytest.mark.parametrize(
        "latitude",
        [
            100,
            -100,
            "100",
        ],
    )
    def test_should_raise_value_error_when_latitude_is_invalid(self, latitude):
        with pytest.raises(ValueError) as exc:
            validate_latitude(latitude)
        assert "Latitude inválida, por favor informe um valor de latitude" in str(exc)

    def test_should_return_valid_latitude(self):
        latitude = 10
        assert validate_latitude(latitude) == latitude

    @pytest.mark.parametrize(
        "longitude",
        [
            200,
            -200,
            "200",
        ],
    )
    def test_should_raise_value_error_when_longitude_is_invalid(self, longitude):
        with pytest.raises(ValueError) as exc:
            validate_longitude(longitude)
        assert "Longitude inválida, por favor informe um valor de longitude" in str(exc)

    def test_should_return_valid_longitude(self):
        longitude = 20
        assert validate_longitude(longitude) == longitude


class TestMacAddressValidator:
    def test_should_raise_value_error_when_mac_address_is_invalid(self):
        mac_address = "001122334455"
        with pytest.raises(ValueError) as exc:
            validate_mac_address(mac_address)
        assert "Endereço MAC inválido" in str(exc.value)

    def test_should_return_valid_mac_address(self):
        mac_address = "00:11:22:33:44:55"
        assert validate_mac_address(mac_address) == mac_address

    @pytest.mark.parametrize(
        "mac_address, expected",
        [
            ("001122334455", "00:11:22:33:44:55"),
            ("00:11:22:33:44:55", "00:11:22:33:44:55"),
        ],
    )
    def test_should_format_mac_address(self, mac_address, expected):
        assert validate_mac_address(mac_address, autofix=True) == expected

    def test_should_raise_value_error_when_mac_address_its_invalid_and_autofix(self):
        mac_address = "00112233445"
        with pytest.raises(ValueError) as exc:
            validate_mac_address(mac_address, autofix=True)
        assert str(exc.value) == "Endereço MAC inválido"


class TestsStringPropertyValidator:
    def test_should_return_valid_string(self):
        string = "Test"
        assert validate_non_empty_string(string) == string

    @pytest.mark.parametrize(
        "string",
        [
            None,
            "",
        ],
    )
    def test_should_raise_value_error_when_string_is_invalid(self, string):
        with pytest.raises(ValueError) as exc:
            validate_non_empty_string(string)
        assert "String vazia ou nula." in str(exc)
