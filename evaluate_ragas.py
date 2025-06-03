import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv

load_dotenv()

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
from rag.rag_chain import RAGChain
from test_questions_with_ground_truth import test_questions_with_ground_truth


def prepare_ragas_dataset():
    rag = RAGChain()

    questions = []
    answers = []
    contexts = []
    ground_truths = []

    print("generating answers for evaluation...")

    for i, test_case in enumerate(test_questions_with_ground_truth):
        print(
            f"processing {i+1}/{len(test_questions_with_ground_truth)}: {test_case['question'][:50]}..."
        )

        try:
            result = rag.query(test_case["question"])

            # extract context from sources
            context_list = [source["text"] for source in result["sources"]]

            questions.append(test_case["question"])
            answers.append(result["answer"])
            contexts.append(context_list)
            ground_truths.append(test_case["ground_truth"])

        except Exception as e:
            print(f"error: {e}")
            questions.append(test_case["question"])
            answers.append("Error generating answer")
            contexts.append(["No context retrieved"])
            ground_truths.append("Error")

    # create dataset dictionary
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    }

    return Dataset.from_dict(data)


def run_ragas_evaluation():
    print("preparing dataset...")
    dataset = prepare_ragas_dataset()

    print("\nrunning ragas evaluation (using openai to judge quality)...")

    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_recall,
            context_precision,
        ],
    )

    return result


def save_results(result):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # get dataframe and scores
    df = result.to_pandas()

    # calculate average scores from dataframe
    scores = {}
    for metric in [
        "faithfulness",
        "answer_relevancy",
        "context_recall",
        "context_precision",
    ]:
        if metric in df.columns:
            scores[metric] = df[metric].mean()

    csv_file = f"ragas_evaluation_{timestamp}.csv"
    df.to_csv(csv_file, index=False)

    # print summary
    print("\nevaluation results:")
    print("-" * 30)
    print(
        df[
            [
                "faithfulness",
                "answer_relevancy",
                "context_recall",
                "context_precision",
            ]
        ].mean()
    )

    print(f"\ndetails saved to: {csv_file}")


def main():
    print("ragas rag evaluation")
    print("=" * 50)

    try:
        result = run_ragas_evaluation()
        save_results(result)
    except Exception as e:
        print(f"\nerror: {e}")


if __name__ == "__main__":
    main()
