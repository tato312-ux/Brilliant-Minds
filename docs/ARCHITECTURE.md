# Arquitectura General – DocSimplify AI (Backend)

El backend está construido con **FastAPI** como capa de API principal.  
Toda la lógica inteligente se orquesta mediante **Microsoft Foundry Agent Service** (multi-agente).  
El flujo principal es conversacional y está impulsado por un pipeline RAG automático.

## Diagrama de Arquitectura

```mermaid
flowchart TD
    subgraph FastAPI["FastAPI Backend"]
        Auth[Auth Router\n/auth]
        Users[Users Router\n/users]
        Documents[Documents Router\n/documents]
        Chats[Chats Router\n/chats]
    end

    subgraph Foundry["Microsoft Foundry Agent Service"]
        AAM["Agente de Adaptación Multimodal (AAM)"]
        AAM --> Parser[Parser Agent]
        AAM --> Simplifier[Simplifier Agent]
        AAM --> Explainer[Explainer Agent]
        AAM --> Calm[Calm Evaluator Agent]
        AAM --> Validator[Validator Agent]
    end

    subgraph Storage["Storage & RAG"]
        Blob[Blob Storage\nDocumentos originales]
        Search[Azure AI Search\nEmbeddings + Vector Store]
    end

    subgraph Data["Base de Datos"]
        Cosmos[(Cosmos DB\nusers + perfiles)]
    end

    subgraph Models["Model Catalog"]
        GPT[GPT-4o]
        Phi[Phi-3]
    end

    FastAPI --> Auth & Users & Documents & Chats
    Chats --> AAM
    Documents --> Blob
    Documents --> Search
    AAM --> Blob & Search
    AAM --> Cosmos
    AAM --> Models
```

## Componentes Principales

**FastAPI Backend**  

- Framework: FastAPI (Python 3.13+)  
- Autenticación: Entra ID + JWT  
- Routers principales: `/auth`, `/users`, `/documents`, `/chats`

**Agentes (Microsoft Foundry Agent Service)**  

- **Agente de Adaptación Multimodal (AAM)**: Orquestador principal. Recibe mensajes del chat, recupera perfil del usuario y contexto RAG, y coordina todos los agentes.  
- **Parser Agent**: Extrae y limpia texto de documentos.  
- **Simplifier Agent**: Aplica Plain Language según preset y nivel de lectura.  
- **Explainer Agent**: Genera explicaciones calmadas.  
- **Calm Evaluator Agent**: Usa Phi-3 como linter de empatía y tono.  
- **Validator Agent**: Valida WCAG 2.2, Accessibility Insights y Content Safety.

**Almacenamiento y RAG**  

- **Blob Storage**: Almacena los documentos originales (PDF/Word).  
- **Azure AI Search**: Indexa embeddings automáticamente al subir un documento (RAG pipeline).  
- **Cosmos DB**: Almacena usuarios, perfiles dinámicos y historial de fatiga.

**Model Catalog**  

- GPT-4o: Razonamiento y simplificación compleja  
- Phi-3: Evaluación de calma y corrección de tono

**Seguridad e IA Responsable**  

- Entra Agent Identity por agente  
- Content Safety Studio + Responsible AI Toolbox  
- Perfiles nunca viajan completos en prompts  
- Evaluador de Calma siempre activo
