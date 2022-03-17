# Terminology Annotator

This project annotates a `.conllup` file with a given terminology in the Romanian language.

This is done by running the `annotate.py` script. For instance, using the files found in `examples`, one can annotate a `.connlup` files as follows:

```
python annotate.py --data_path examples/input.conllup --output_path examples/output.conllup --terminology_path examples/terminology.csv
```

The `data_path` parameter points to the `.conllup` file to be annotated and `output_path` is the resulted `.conllup` file. The `terminology_path` parameter contains the
terminology to be used.

One can also change the lemmas used by this script by changing the `lemma_path` parameter to point to another file. Also, the maximum number of words that can exist in
a terminology can be adjusted using the `max_terminology_words` paramter.

In addition, because a terminology can contain multiple languages, one can select the desired langauge using the `terminology_langauge` paramter.

***Important Note***: Please follow the format in the terminology file, so the script knows how to parse it. This implies using the same headers, separated by `|`, as 
exemplified in `examples/terminology.csv`:

```
E_ID|L_CODE|T_TERM|
11111|ro|Paris|
22222|ro|statului portului|
33333|ro|ordinul|
44444|ro|Monitorul Oficial|
55555|ro|Belgia|
```
The terminology file can have any number of headers, but the three presented above must be present (i.e. `E_ID`, `L_CODE`, `T_TERM`).
