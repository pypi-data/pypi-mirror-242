# OpenID Connect Hub

The `oidc_hub` package provides a user-friendly web interface for managing OpenID identities. As an Identity Provider (IdP), this Django application allows users to manage their OpenID credentials and authenticate with these seamlessly.

## Features

- User-Friendly Interface: A clean and intuitive web interface for users to manage their OpenID identities effortlessly.

- OpenID Authentication: Serve as an OpenID Identity Provider, enabling users to utilize their OpenID credentials for authentication across various services.

- Identity Management: Users can create, update, and delete OpenID identities easily through the web interface.

- Security: Implement secure OpenID authentication practices to ensure the safety and privacy of user identities.

## Installation


```shell
pip install oidc_hub
```

### Configuration

Add `oidc_hub` and `oidc_provider` to your `INSTALLED_APPS` in the Django project's settings:

```python
INSTALLED_APPS = [
  # ...
  "oidc_provider",
  "oidc_hub",
  "django.contrib.staticfiles",
  # ...
]
```

### Migrations

Run migrations to create the required database tables:

```shell
oidc_hub migrate
```

## Webserver

#### Development

Start the Django development server.

```shell
oidc_hub runserver
```

#### Production

Start the multi-threaded Gunicorn server.

```shell
oidc_hub run
```

## License

This project is licensed under the AGPLv3 License - see the [LICENSE.md](LICENSE.md) file for details.
