import conllu
import os
import nltk
import uuid


def parse_entity(entity_str):
    if "," in entity_str:
        labels = [list(label.split(":")) for label in entity_str.strip().split(",")]
    elif ";" in entity_str:
        labels = [list(label.split(":")) for label in entity_str.strip().split(";")]
    elif ":" in entity_str:
        labels = [list(entity_str.strip().split(":"))]
    else:
        labels = ["_"]

    return labels


if __name__ == "__main__":
    path = "examples/annotations"
    set_marcell_labels = []
    set_curlicat_labels = []
    set_marcell_labels_unique = set()
    set_curlicat_labels_unique = set()

    for filename in os.listdir(path):
        with open(os.path.join(path, filename), "r", encoding="utf-8") as in_conllu_file:
            sentences = conllu.parse(in_conllu_file.read())

        token_counter = 0

        for sentence in sentences:
            dict_marcell_terms = {}
            dict_curlicat_terms = {}

            for token in sentence:
                # print(parse_entity(token["marcell:iate"]), parse_entity(token["curlicat:iate"]))
                token_id = str(uuid.uuid4())
                marcell_labels = parse_entity(token["marcell:iate"])
                curlicat_labels = parse_entity(token["curlicat:iate"])

                document_name = filename.split("_")[1].split(".")[0]

                if "_" not in marcell_labels:
                    for label_ct, label in marcell_labels:
                        if label_ct not in dict_marcell_terms:
                            dict_marcell_terms[label_ct] = [token["lemma"], label]
                        else:
                            dict_marcell_terms[label_ct][0] += token["lemma"]

                if "_" not in curlicat_labels:
                    for label_ct, label in curlicat_labels:
                        if label_ct not in dict_curlicat_terms:
                            dict_curlicat_terms[label_ct] = [token["lemma"], label]
                        else:
                            dict_curlicat_terms[label_ct][0] += token["lemma"]

                token_counter += 1

            print(dict_marcell_terms)
            print(dict_curlicat_terms)
            print()

    start_intersection = set(set_curlicat_labels).intersection(set(set_marcell_labels))
    unique_intersection = set_curlicat_labels_unique.intersection(set_marcell_labels_unique)

    print("MARCELL counter: ", len(set_marcell_labels))
    print("CURLICAT counter: ", len(set_curlicat_labels))
    print("Intersection counter: ", len(start_intersection))
    print("MARCELL counter unique: ", len(set_marcell_labels_unique))
    print("CURLICAT counter unique: ", len(set_curlicat_labels_unique))
    print("Intersection counter unique: ", len(unique_intersection))

    with open("results/results_marcell.txt", "w", encoding="utf-8") as file:
        for label in set_marcell_labels:
            file.write(label + "\n")

    with open("results/results_curlicat.txt", "w", encoding="utf-8") as file:
        for label in set_curlicat_labels:
            file.write(label + "\n")

    with open("results/results_intersection.txt", "w", encoding="utf-8") as file:
        for label in start_intersection:
            file.write(label + "\n")

    with open("results/results_marcell_unique.txt", "w", encoding="utf-8") as file:
        for label in set_marcell_labels_unique:
            file.write(label + "\n")

    with open("results/results_curlicat_unique.txt", "w", encoding="utf-8") as file:
        for label in set_curlicat_labels_unique:
            file.write(label + "\n")

    with open("results/results_intersection_unique.txt", "w", encoding="utf-8") as file:
        for label in unique_intersection:
            file.write(label + "\n")