"""CLI helper for provisioning the multimodal-ready rag-v3 pipeline."""

from src.services.search.rag_v3_provisioner import RagV3Provisioner


def main() -> None:
    provisioner = RagV3Provisioner()
    provisioner.provision()
    print("RAG v3 assets created or updated.")


if __name__ == "__main__":
    main()
