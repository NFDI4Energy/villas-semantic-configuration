@echo off

docker run --rm -v "%~dp0:/local" redocly/cli bundle /local/api-spec/openapi.yaml -o /local/villas-semantic-configuration/src/vsc/openapi.yaml

docker run --rm -v "%~dp0:/local" openapitools/openapi-generator-cli:v7.27.0 generate ^
    -g python-fastapi ^
    -o /local/vsc-api ^
    -c /local/generate-python-api-config.yaml
