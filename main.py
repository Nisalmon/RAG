import os
import fire


os.environ["HF_HOME"] = f"/goinfre/{os.getenv('USER')}/.cache/huggingface"
os.environ["HF_HUB_CACHE"] = f"{os.environ['HF_HOME']}/hub"
os.environ["TRANSFORMERS_CACHE"] = os.environ["HF_HOME"]


def main() -> None:
    from src.CLI.cli import CLI
    prog = CLI()
    fire.Fire(prog)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        os.system("clear")
        print("RIP Me i guess 💀🥀")
