ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}-slim

RUN adduser --disabled-password --gecos '' appuser
USER appuser

WORKDIR /src

COPY ilovepdf /src/ilovepdf
COPY samples /src/samples
COPY tests /src/tests
COPY requirements_test.txt /src/
COPY requirements_dev.txt /src/
COPY requirements.txt /src/
COPY setup.cfg /src/
COPY pyproject.toml /src/
COPY pytest.ini /src/


RUN pip install --upgrade pip \
    && pip install -r requirements_test.txt \
    && rm -rf ~/.cache/pip

ENV PYTHONPATH=/src
ENV PATH="$PATH:/home/appuser/.local/bin"

CMD pip install -e . \
    && pip list \
    && python -c "import sys; print('--- sys.path ---'); print(sys.path)" \
    && python -c "import ilovepdf; print('--- ilovepdf import OK ---', ilovepdf)" \
    && pytest tests/unit \
    && pytest tests/integration
