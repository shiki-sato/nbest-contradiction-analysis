import argparse
import spacy



def make_input_dic(sentence, parser):
    input_dic = {}
    input_dic['items'] = [item for item in parser(sentence)]
    input_dic['tokens'] = [item.text for item in input_dic['items']]
    input_dic['tags'] = [item.tag_ for item in input_dic['items']]
    input_dic['lems'] = [item.lemma_ for item in input_dic['items']]
    input_dic['dep'] = [item.dep_ for item in input_dic['items']]
    return input_dic


def get_negative_question_of_str(in_str, parser):
    first_token = in_str.split()[0].lower()
    left_str = ' '.join(in_str.split()[1:])
    if first_token == "am":
        new_f = "Are n't"
    elif first_token == "was":
        new_f = "Was n't"
    elif first_token == "are":
        new_f = "Are n't"
    elif first_token == "were":
        new_f = "Were n't"
    elif first_token == "is":
        new_f = "Is n't"
    elif first_token == "do":
        new_f = "Do n't"
    elif first_token == "does":
        new_f = "Does n't"
    elif first_token == "did":
        new_f = "Did n't"
    elif first_token == "have":
        new_f = "Have n't"
    elif first_token == "has":
        new_f = "Has n't"
    elif first_token == "had":
        new_f = "Had n't"
    elif first_token == "will":
        new_f = "Wo n't"
    elif first_token == "would":
        new_f = "Would n't"
    elif first_token == "should":
        new_f = "Should n't"
    elif first_token == "could":
        new_f = "Could n't"
    elif first_token == "can":
        new_f = "Ca n't"
    elif first_token == "shall":
        new_f = "Shall n't"
    elif first_token == "must":
        new_f = "Must n't"
    elif first_token == "might":
        new_f = "Might not"
    else:
        return "[[SKIP]]"
    return new_f + ' ' + left_str



def main(args):
    parser = spacy.load("en_core_web_sm")
    with open(args.in_fname) as i_f, open(args.out_fname, 'w') as o_f:
        for i,l in enumerate(i_f):
            if args.num_process > 0 and i >= args.num_process:
                break
            context, gres, res, *label = l.strip().split("\t")
            context = context.strip()
            res = res.strip()
            gres = gres.strip()
            
            return_str = get_negative_question_of_str(res, parser)
            if len(return_str.split()) > 30 or return_str.startswith("[[SKIP]]"):
                continue
            if label:
                o_f.write('{}\t{}\t{}\t{}\t{}\n'.format(context, gres, res, return_str, label[0]))
            else:
                o_f.write('{}\t{}\t{}\t{}\n'.format(context, gres, res, return_str))


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-fname", required=True)
    parser.add_argument("--out-fname", required=True)
    parser.add_argument("--compute-jaccard", action="store_true")
    parser.add_argument("--num-process", type=int, default=-1)

    args = parser.parse_args()

    main(args)
