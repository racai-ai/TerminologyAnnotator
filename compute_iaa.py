import conllu
import os
import nltk
import uuid
from collections import OrderedDict
from annotate import read_terminology, read_lemmas


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


def filter_intersected_terms(list_terms):
    new_list_terms = []

    for i, (term, label, positions) in enumerate(list_terms):
        term_ok = True
        for j in range(0, i):
            for position in positions:
                if position in list_terms[j][2]:
                    term_ok = False
                    break

        if term_ok:
            new_list_terms.append([term, label, positions])

    return new_list_terms


if __name__ == "__main__":
    path = "examples/annotations"
    list_marcell_labels = []
    list_curlicat_labels = []
    set_marcell_labels_unique = []
    set_curlicat_labels_unique = []

    dict_lemmas = read_lemmas("examples/tbl.wordform.ro")
    dict_terms, dict_terms_type = read_terminology("data/IATE_export.csv", dict_lemmas)

    for filename in os.listdir(path):
        with open(os.path.join(path, filename), "r", encoding="utf-8") as in_conllu_file:
            sentences = conllu.parse(in_conllu_file.read())

        token_counter = 0
        document_name = filename.split(".")[0]

        for sentence in sentences:
            dict_marcell_terms = OrderedDict()
            dict_curlicat_terms = OrderedDict()

            for token in sentence:
                # print(parse_entity(token["marcell:iate"]), parse_entity(token["curlicat:iate"]))
                token_id = str(uuid.uuid4())
                marcell_labels = parse_entity(token["marcell:iate"])
                curlicat_labels = parse_entity(token["curlicat:iate"])

                if "_" not in marcell_labels:
                    for label_ct, label in marcell_labels:
                        if label_ct not in dict_marcell_terms:
                            dict_marcell_terms[label_ct] = [token["lemma"], label, [token_counter]]
                        else:
                            dict_marcell_terms[label_ct][0] += token["lemma"]
                            dict_marcell_terms[label_ct][2].append(token_counter)

                if "_" not in curlicat_labels:
                    for label_ct, label in curlicat_labels:
                        if label_ct not in dict_curlicat_terms:
                            dict_curlicat_terms[label_ct] = [token["lemma"], label, [token_counter]]
                        else:
                            dict_curlicat_terms[label_ct][0] += token["lemma"]
                            dict_curlicat_terms[label_ct][2].append(token_counter)

                token_counter += 1

            list_marcell_terms = [
                v for k, v in sorted(dict_marcell_terms.items(), key=lambda item: len(item[1][2]), reverse=True)
            ]
            list_curlicat_terms = [
                v for k, v in sorted(dict_curlicat_terms.items(), key=lambda item: len(item[1][2]), reverse=True)
            ]

            new_list_marcell_terms = filter_intersected_terms(list_marcell_terms)
            new_list_curlicat_terms = filter_intersected_terms(list_curlicat_terms)

            # print(list_marcell_terms)
            # print(new_list_marcell_terms)
            # print(list_curlicat_terms)
            # print(new_list_curlicat_terms)
            # print()

            set_marcell_labels_unique.extend(
                "{}_{}_{}".format(document_name, term, label) for term, label, _ in
                new_list_marcell_terms)
            set_curlicat_labels_unique.extend(
                "{}_{}_{}".format(document_name, term, label) for term, label, _ in
                new_list_curlicat_terms)

            list_marcell_labels.extend(
                "{}_{}_{}_{}".format(document_name, positions[0], term, label) for term, label, positions in new_list_marcell_terms)
            list_curlicat_labels.extend(
                "{}_{}_{}_{}".format(document_name, positions[0], term, label) for term, label, positions in new_list_curlicat_terms)

    set_marcell_labels_unique = set(set_marcell_labels_unique)
    set_curlicat_labels_unique = set(set_curlicat_labels_unique)

    start_intersection = set(list_curlicat_labels).intersection(set(list_marcell_labels))
    unique_intersection = set_curlicat_labels_unique.intersection(set_marcell_labels_unique)

    unique_diff_marcell = set_marcell_labels_unique.difference(unique_intersection)
    unique_diff_curlicat = set_curlicat_labels_unique.difference(unique_intersection)

    unique_diff_marcell_not_in_IATE_counter = 0
    for term in unique_diff_marcell:
        label = term.split("_")[-1]
        if label not in dict_terms.values():
            unique_diff_marcell_not_in_IATE_counter += 1

    print("MARCELL counter: ", len(list_marcell_labels))
    print("CURLICAT counter: ", len(list_curlicat_labels))
    print("Intersection counter: ", len(start_intersection))
    print("MARCELL counter unique: ", len(set_marcell_labels_unique))
    print("CURLICAT counter unique: ", len(set_curlicat_labels_unique))
    print("Intersection counter unique: ", len(unique_intersection))
    print("MARCELL unique terms from intersect difference not in IATE: {}/{}".format(
        unique_diff_marcell_not_in_IATE_counter, len(unique_diff_marcell)))

    with open("results/results_marcell.txt", "w", encoding="utf-8") as file:
        for label in list_marcell_labels:
            file.write(label + "\n")

    with open("results/results_curlicat.txt", "w", encoding="utf-8") as file:
        for label in list_curlicat_labels:
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

    with open("results/results_diff_unique_marcell.txt", "w", encoding="utf-8") as file:
        for label in unique_diff_marcell:
            file.write(label + "\n")

    with open("results/results_diff_unique_curlicat.txt", "w", encoding="utf-8") as file:
        for label in unique_diff_curlicat:
            file.write(label + "\n")