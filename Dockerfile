FROM python:3.11-slim as base
RUN adduser --disabled-password reflex

FROM base as runtime
RUN apt-get update \
    && apt-get install -y gcc g++ python3-dev curl \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs unzip \
    && rm -rf /var/lib/apt/lists/*


#FROM runtime as build
WORKDIR /app
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .

RUN pip install --no-cache-dir wheel \
    && pip install --no-cache-dir -r requirements.txt

ENV PATH="/app/venv/bin:$PATH"


#FROM build as init
FROM runtime as init

WORKDIR /app
ENV BUN_INSTALL="/app/.bun"
#COPY --from=build /app/ /app/
COPY --from=runtime /app/ /app/
RUN reflex init


FROM init

COPY --chown=reflex --from=init /app/ /app/
USER reflex
WORKDIR /app

CMD ["reflex", "init"]
#CMD ["reflex", "run", "--env", "prod"]
CMD ["reflex","run"]

EXPOSE 3000
EXPOSE 8000
