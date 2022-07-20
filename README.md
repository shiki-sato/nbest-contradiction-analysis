# N-best Response-based Analysis of Contradiction-awareness in Neural Response Generation Models
This repository has the code to construct the test set we developed in:

Shiki Sato, Reina Akama, Hiroki Ouchi, Ryoko Tokuhisa, Jun Suzuki and Kentaro Inui. N-best Response-based Analysis of Contradiction-awareness in Neural Response Generation Models.

## Construction
You can construct our test set by running all cells of `construct_yesno_dataset.ipynb`.

## Format
Each line of all files corresponds to a stimulus input. Utterances are splitted by "\t".

```
[history_utterance]\t[original_nli_hypothesis_sentence]\t[yesno_question_positive_form]\t[yesno_question_negative_form]
```


## Citation
If you use this test set, please cite the following:

> Shiki Sato, Reina Akama, Hiroki Ouchi, Ryoko Tokuhisa, Jun Suzuki and Kentaro Inui. N-best Response-based Analysis of Contradiction-awareness in Neural Response Generation Models. In Proceedings of the 23rd Annual Meeting of the Special Interest Group on Discourse and Dialogue (SIGDIAL 2022), Sep 2022.