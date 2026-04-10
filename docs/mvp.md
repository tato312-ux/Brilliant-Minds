# Especificación del MVP Backend – DocSimplify AI

## Alcance del MVP

Versión mínima viable centrada exclusivamente en backend y agentes:  

- Autenticación y gestión de usuarios  
- Subida, listado y eliminación de documentos  
- Pipeline RAG automático  
- Chat conversacional con el Agente de Adaptación Multimodal (AAM)  
- Presets de accesibilidad y explicaciones calmadas

## Endpoints FastAPI (v1)

**Base URL:** `/api/v1`

### Auth

| Método | Endpoint         | Descripción         | Request Body                | Response       |
| ------ | ---------------- | ------------------- | --------------------------- | -------------- |
| POST   | `/auth/register` | Registro de usuario | `{ email, password, name }` | Token + userId |
| POST   | `/auth/login`    | Login               | `{ email, password }`       | Token + userId |

### Users

| Método | Endpoint    | Descripción             | Request Body                  | Response           |
| ------ | ----------- | ----------------------- | ----------------------------- | ------------------ |
| GET    | `/users/me` | Obtener mi perfil       | -                             | Perfil completo    |
| PATCH  | `/users/me` | Actualizar preferencias | `{ readingLevel, tone, ... }` | Perfil actualizado |

### Documents

| Método | Endpoint                  | Descripción                | Request Body / Query | Response                           |
| ------ | ------------------------- | -------------------------- | -------------------- | ---------------------------------- |
| POST   | `/documents`              | Subir documento (PDF/Word) | Multipart form-data  | `{ documentId, filename, status }` |
| GET    | `/documents`              | Listar mis documentos      | -                    | Lista de documentos                |
| DELETE | `/documents/{documentId}` | Eliminar documento         | documentId (path)    | `{ status: "deleted" }`            |

### Chats (interacción principal con el agente)

| Método | Endpoint                   | Descripción              | Request Body                | Response                                                                |
| ------ | -------------------------- | ------------------------ | --------------------------- | ----------------------------------------------------------------------- |
| POST   | `/chats`                   | Crear nueva conversación | `{ title? }`                | `{ chatId }`                                                            |
| POST   | `/chats/{chatId}/messages` | Enviar mensaje al agente | `{ message, documentIds? }` | `{ simplifiedText, explanation, audioUrl, beeLineOverlay, wcagReport }` |

## Agentes en el MVP

**Agente Principal**  

- Nombre: ejemplo `AdaptationAgent` (AAM)  
- Responsable de toda la orquestación  
- Se activa exclusivamente desde el endpoint `/chats/{chatId}/messages`  
- Recupera perfil del usuario + documentos indexados en Azure AI Search

**Agentes Secundarios (invocados por AAM)**  

- Parser Agent  
- Simplifier Agent  
- Calm Evaluator Agent (Phi-3)  
- Explainer Agent  
- Validator Agent

## Base de Datos

**Cosmos DB Container:** `users`

**Documento de ejemplo:**

```json
{
  "id": "user-uuid",
  "userId": "entra-1234",
  "readingLevel": "A2",
  "maxSentenceLength": 12,
  "tone": "calm_supportive",
  "avoidWords": ["urgente", "crítico", "debe"],
  "preset": "TDAH",
  "fatigueHistory": []
}
```

## Estructura de Carpetas (Backend)

```markdown
docsimplify/
├── src/
│   ├── main.py                          # FastAPI entrypoint
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── middleware.py
│   ├── api/
│   │   └── v1/
│   │       ├── routers/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── documents.py
│   │       │   └── chats.py
│   ├── agents/
│   │   ├── adaptation_agent.py          # AAM – orquestador principal
│   │   ├── parser_agent.py
│   │   ├── simplifier_agent.py
│   │   ├── explainer_agent.py
│   │   ├── calm_evaluator.py
│   │   └── validator_agent.py
│   ├── services/
│   │   ├── blob_service.py
│   │   ├── search_service.py            # Azure AI Search RAG
│   │   ├── profile_service.py
│   │   └── accessibility_service.py
│   └── models/
│       └── schemas.py
├── tests/
├── infrastructure/
│   └── bicep/
├── .env.example
├── requirements.txt
└── README.md
```

## Tecnologías del MVP

- **Framework**: FastAPI  
- **Agentes**: Microsoft Foundry Agent Service  
- **Almacenamiento**: Blob Storage + Azure AI Search  
- **Base de datos**: Cosmos DB  
- **Autenticación**: Entra ID  
- **Modelos**: GPT-4o + Phi-3  
