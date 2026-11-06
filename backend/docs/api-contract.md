# API contract

## Authentication

### Register

`POST /api/auth/register`

Request:

```json
{"name":"Test Student","email":"student@example.com","password":"password123"}
```

Response `201 Created`:

```json
{
  "access_token":"<jwt>",
  "token_type":"bearer",
  "user":{"id":"<uuid>","name":"Test Student","email":"student@example.com","created_at":"2026-01-01T12:00:00"}
}
```

### Login

`POST /api/auth/login`

Request:

```json
{"email":"student@example.com","password":"password123"}
```

Response `200 OK` has the same `TokenResponse` shape as registration.

### Current user

`GET /api/auth/me` requires `Authorization: Bearer <jwt>`.

Response `200 OK`:

```json
{"id":"<uuid>","name":"Test Student","email":"student@example.com","created_at":"2026-01-01T12:00:00"}
```

## Error codes

Errors use FastAPI's default shape: `{"detail":"message"}`.

- `401 Unauthorized`: missing, invalid, or expired token; invalid login credentials.
- `404 Not Found`: requested resource does not exist.
- `409 Conflict`: email is already registered.
- `422 Unprocessable Entity`: invalid request input.
