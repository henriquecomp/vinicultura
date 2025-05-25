import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, status
from app.api.controllers.production_controller import get_production
from app.application.DTOs.production_response import ProductionResponse

# Mock para OAuth2PasswordBearer para evitar erros de dependência não resolvida
oauth2_scheme_mock = MagicMock(return_value="fake_token")


@pytest.fixture
def mock_production_service_instance():
    """Fixture para mockar a instância do ProductionService."""
    mock_service = MagicMock()
    # Simula o retorno do método get_production do serviço
    mock_service.get_production.return_value = [
        ProductionResponse(category="Vinho Tinto", name="Produto A", quantity=100.0),
        ProductionResponse(category="Vinho Branco", name="Produto B", quantity=200.0),
    ]
    return mock_service


def test_get_production_success(mock_production_service_instance):
    """
    Testa o endpoint get_production com sucesso.
    Verifica se check_access e o serviço são chamados corretamente.
    """

    # Cria os mocks de check_access e ProductionService
    with patch(
        "app.api.controllers.production_controller.check_access"
    ) as mock_check_access, patch(
        "app.api.controllers.production_controller.ProductionService",
        return_value=mock_production_service_instance,
    ) as mock_production_service_class:

        # Arrange
        fake_token = "valid_token"
        test_year = 2023

        # Act
        result = get_production(token=fake_token, year=test_year)

        # Assert
        # Verifica se check_access foi chamado com o token correto
        mock_check_access.assert_called_once_with(fake_token)

        # Verifica se ProductionService foi instanciado
        mock_production_service_class.assert_called_once_with()

        # Verifica se o método get_production do serviço foi chamado com o ano correto
        mock_production_service_instance.get_production.assert_called_once_with(
            test_year,
        )

        # Verifica se o resultado é o esperado (o que foi definido no mock_production_service_instance)
        assert len(result) == 2
        assert result[0].name == "Produto A"
        assert result[0].quantity == 100.0
        assert result[1].category == "Vinho Branco"


def test_get_production_unauthorized():
    """
    Testa o endpoint get_production quando check_access levanta HTTPException (token inválido).
    """

    # Cria os mocks de check_access e ProductionService
    with patch(
        "app.api.controllers.production_controller.check_access"
    ) as mock_check_access, patch(
        "app.api.controllers.production_controller.ProductionService"
    ) as mock_production_service_class: 

        # Arrange
        mock_check_access.side_effect = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
        fake_token = "invalid_token"
        test_year = 2023

        # Act
        with pytest.raises(HTTPException) as ex:
            get_production(token=fake_token, year=test_year)

        mock_check_access.assert_called_once_with(fake_token)
        mock_production_service_class.assert_not_called()

        # Verifica a exceção
        assert ex.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert ex.value.detail == "Invalid token"



def test_get_production_service_exception(mock_production_service_instance):
    """
    Testa o endpoint get_production quando o serviço levanta uma exceção.
    O controller deve repassar a exceção (ou tratar e levantar uma HTTPException).
    No código atual, ele repassa a exceção.
    """

    # Cria os mocks de check_access e ProductionService
    with patch(
        "app.api.controllers.production_controller.check_access"
    ) as mock_check_access, patch(
        "app.api.controllers.production_controller.ProductionService",
        return_value=mock_production_service_instance,
    ) as mock_production_service_class:

        # Arrange
        mock_production_service_instance.get_production.side_effect = Exception(
            "Erro no serviço"
        )
        fake_token = "valid_token"
        test_year = 2023

        # Act
        with pytest.raises(Exception, match="Erro no serviço"):
            get_production(token=fake_token, year=test_year)

        # Verifica se check_access foi chamado
        mock_check_access.assert_called_once_with(fake_token)

        # Verifica se ProductionService foi instanciado
        mock_production_service_class.assert_called_once_with()

        # Verifica se o método get_production do serviço foi chamado
        mock_production_service_instance.get_production.assert_called_once_with(
            test_year
        )
