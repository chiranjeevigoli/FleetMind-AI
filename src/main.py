from retriever import retrieve
from llm import generate_answer


def main():
    print("=" * 70)
    print("FleetMind AI")
    print("=" * 70)

    while True:

        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        print("\nSearching manuals...")

        retrieved = retrieve(question)

        print("Generating answer...\n")

        answer = generate_answer(question, retrieved)

        print(answer)


if __name__ == "__main__":
    main()