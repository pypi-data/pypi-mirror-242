import typer, requests
from typing_extensions import Annotated
from rich import print

app = typer.Typer()


@app.command()
def token(
    client_id: Annotated[str, typer.Argument(envvar="X_FHIR_CLIENT_ID")],
    secret_key: Annotated[str, typer.Argument(envvar="X_FHIR_SECRET_KEY")],
):
    # https://docs.aws.amazon.com/dcv/latest/sm-dev/request.html

    body = {
        "grant_type": "client_credentials",
        "scope": 'm2m/read'
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(
        url='https://akello-test-prefix.auth.us-east-1.amazoncognito.com/oauth2/token',
        data=body,
        auth=(client_id, secret_key),
        headers=headers
    )
    print(response.json())
    return response.json()["access_token"]


def run():
    app()