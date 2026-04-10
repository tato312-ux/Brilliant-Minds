"""CLI helper to provision knowledge source, knowledge base, and optional MCP connection."""

from src.services.search.rag_pipeline import run_pipeline


def main() -> None:
    """CLI entry point to run the agentic retrieval asset provisioning pipeline."""
    run_pipeline()
    print("Agentic retrieval assets synchronized.")


if __name__ == "__main__":
    main()
