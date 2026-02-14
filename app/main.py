# from app.config.loader import load_config

# def main():
#     settings = load_config()

#     print("Model:", settings.llm.model)
#     print("Chunk size:", settings.chunking.chunk_size)
#     print("Inference enabled:", settings.inference.enabled)

from app.pipeline.run import main

if __name__ == "__main__":
    main()
