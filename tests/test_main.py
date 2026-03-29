import pytest
from src.main import main


def test_main_invalid_mode():
    with pytest.raises(ValueError):
        main("modo_invalido")