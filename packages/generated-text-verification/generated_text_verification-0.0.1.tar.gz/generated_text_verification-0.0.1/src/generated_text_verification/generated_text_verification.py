import os
import time
from pprint import pprint
from typing import List

import numpy as np
from nltk.tokenize import sent_tokenize
from pydash import py_
from sentence_transformers import SentenceTransformer


model_name_or_path = os.path.join("all-MiniLM-L6-v2")
embed_model = SentenceTransformer(model_name_or_path, device="cpu")


def generate_sentence_mapping(
    generated_documents: List[str],
    source_documents: List[str],
    threshold=0.55,
    max_similar_sentences=5,
):
    """
    Generate a mapping between sentences in generated documents and similar sentences in source documents based on sentence embeddings.

    Args:
        generated_documents (List[str]): List of generated documents as strings.
        source_documents (List[str]): List of source documents as strings.
        threshold (float): Similarity threshold for considering sentences as matches.

    Returns:
        List[List[dict]]: A list of lists containing mappings between generated sentences and source sentences.
            Each mapping is represented as a dictionary with the following keys:
            - "gen_sent": The generated sentence.
            - "gen_sent_idx": The index of the generated sentence within its document.
            - "mapping": A list of mappings for this generated sentence, where each mapping is represented as a dictionary with the following keys:
                - "sent": The source sentence.
                - "src_doc_idx": The index of the source document in the source_documents list.
                - "src_sent_idx": The index of the source sentence within its document.
                - "score": The similarity score between the generated and source sentences.
    """
    # Tokenize sentences in generated documents
    generated_docs_sents = [sent_tokenize(doc) for doc in generated_documents]
    generated_docs_sentence_lengths = [
        len(doc_sents) for doc_sents in generated_docs_sents
    ]

    # Tokenize sentences in source documents
    source_docs_sents = [sent_tokenize(doc) for doc in source_documents]
    source_docs_sentence_lengths = [len(doc_sents) for doc_sents in source_docs_sents]

    # Flatten the lists of sentences
    generated_sentences = py_.flatten(generated_docs_sents)
    source_sentences = py_.flatten(source_docs_sents)

    # Encode sentences using a pre-trained embedding model
    sentence_embeddings = embed_model.encode(generated_sentences + source_sentences)
    assert len(sentence_embeddings) == (
        len(generated_sentences) + len(source_sentences)
    ), "Length mismatch"

    # Split sentence embeddings into generated and source sentence embeddings
    generated_sentence_embeddings = sentence_embeddings[: len(generated_sentences)]
    source_sentence_embeddings = sentence_embeddings[-len(source_sentences) :]

    # Transpose source sentence embeddings
    source_sentence_embeddings_T = source_sentence_embeddings.T

    # Calculate similarity matrix and get top indices
    similarity_matrix = np.dot(
        generated_sentence_embeddings, source_sentence_embeddings_T
    )
    top_indices = np.argsort(-similarity_matrix, axis=1)[:, :max_similar_sentences]

    # Initialize results
    results = []
    current_generated_doc_idx = -1
    current_generated_cumulative_length = 0

    # Iterate over generated sentences and their top indices
    for flattened_generated_sent_idx, (
        generated_sent,
        source_sent_indices,
        sim_scores,
    ) in enumerate(zip(generated_sentences, top_indices, similarity_matrix)):
        if flattened_generated_sent_idx > current_generated_cumulative_length:
            raise ValueError("generated_sent_idx > current_generated_cumulative_length")
        elif flattened_generated_sent_idx == current_generated_cumulative_length:
            results.append([])
            current_generated_doc_idx += 1
            current_generated_cumulative_length += generated_docs_sentence_lengths[
                current_generated_doc_idx
            ]

        generated_sent_idx = (
            flattened_generated_sent_idx
            - current_generated_cumulative_length
            + generated_docs_sentence_lengths[current_generated_doc_idx]
        )
        mapping_sentences = []

        # Iterate over top source sentence indices and similarity scores
        for flattened_source_sent_idx, score in zip(source_sent_indices, sim_scores):
            # Map the index in source_sentences to the index of the nested list and the index in the nested list in source_docs_sents
            source_nested_list_index = 0
            source_cumulative_length = 0
            for i, length in enumerate(source_docs_sentence_lengths):
                if flattened_source_sent_idx < source_cumulative_length + length:
                    source_nested_list_index = i
                    break
                source_cumulative_length += length

            source_sent_idx = flattened_source_sent_idx - source_cumulative_length

            if score > threshold:
                mapping_sentences.append(
                    {
                        "sent": source_sentences[flattened_source_sent_idx],
                        "src_doc_idx": source_nested_list_index,
                        "src_sent_idx": source_sent_idx,
                        "score": float(score),
                    }
                )

        result_entry = {
            "gen_sent": generated_sent,
            "gen_sent_idx": generated_sent_idx,
            "mapping": mapping_sentences,
        }
        results[current_generated_doc_idx].append(result_entry)

    return results
