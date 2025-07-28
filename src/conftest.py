import random
import string

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient


@pytest.fixture
def mocked_file() -> SimpleUploadedFile:
    return SimpleUploadedFile(
        f"mocked_file_{''.join(random.choices((string.ascii_letters + string.digits), k=18))}.txt",  # nosec
        b"Este e o conteudo de teste do arquivo.",  # Conteúdo em bytes
        content_type="text/plain",
    )


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
