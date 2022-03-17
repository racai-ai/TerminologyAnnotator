# Terminology Annotator

This project annotates a `.conllup` file with a given terminology in the Romanian language.

This is done by running the `annotate.py` script. For instance, using the files found in `examples`, one can annotate a `.connlup` files as follows:

```
python annotate.py --data_path examples/input.conllup --output_path examples/output.conllup --terminology_path examples/terminology.csv
```

The `data_path` parameter points to the `.conllup` file to be annotated and `output_path` is the resulted `.conllup` file. The `terminology_path` parameter contains the
terminology to be used. ***Important Note***: Please follow the format in the terminology file, so the script knows how to parse it.

One can also change the lemmas used by this script by changing the `lemma_path` parameter to point to another file. Also, the maximum number of words that can exist in
a terminology can be adjusted using the `max_terminology_words` paramter.
