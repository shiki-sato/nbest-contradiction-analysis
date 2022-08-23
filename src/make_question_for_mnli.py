import argparse
import spacy
import copy
from tqdm import tqdm


vtag_types = [
    "VB",
    "VBP",
    "VBZ",
    "VBD",
    "MD", 
    ]

obj_tags = {
    "iobj",
    "obj",
    "dobj",
    "pobj",
    "attr",
    "oprd",
    "dative",
    }

subj_tags = {
    "csubj",
    "nsubj",
    "csubjpass",
    "nsubj",
    "nsubjpass",
    }

c_req_tags = {
    "csubj",
    "nsubj",
    "csubjpass",
    "nsubj",
    "nsubjpass",
    "expl",
    }

shorten_be_dic = {
    "'s": "is",
    "'m": "am",
    "'re": "are",
    }

shorten_md_dic = {
    "'d": "would",
    "'ll": "will"
    }

shorten_hv_dic = {
    "'d": "had",
    "'ve": "have"
    }

noun_tags = {
    "NOUN",
    "PRON",
    "PROPN",
    }

init_tags = {
    "ADJ",
    "DET",
    "NOUN",
    "NUM",
    "PRON",
    "PROPN",
    "CD",
    "DT",
    "EX",
    "JJ",
    "JJR",
    "JJS",
    "NN",
    "NNP",
    "NNPS",
    "NNS",
    "PDT",
    "PRP",
    "PRP$",
    "VBG"
    }


def f2s(str):
    str = " " + str + " "
    return (
        str
        .replace(" i am ", " @@@you are@@@ ")
        .replace(" i 'm ", " @@@you 're@@@ ")
        .replace(" i ' m ", " @@@you 're@@@ ")
        .replace(" am i ", " @@@are you@@@ ")
        .replace(" I am ", " @@@you are@@@ ")
        .replace(" I 'm ", " @@@you 're@@@ ")
        .replace(" I ' m ", " @@@you 're@@@ ")
        .replace(" am I ", " @@@are you@@@ ")
        .replace(" Am I ", " @@@are you@@@ ")
        .replace(" i was ", " @@@you were@@@ ")
        .replace(" was i ", " @@@were you@@@ ")
        .replace(" I was ", " @@@you were@@@ ")
        .replace(" was I ", " @@@were you@@@ ")
        .replace(" Was I ", " @@@were you@@@ ")
        .replace(" I ", " @@@you@@@ ")
        .replace(" i ", " @@@you@@@ ")
        .replace(" My ", " @@@your@@@ ")
        .replace(" my ", " @@@your@@@ ")
        .replace(" @o@Me ", " @@@you@@@ ")
        .replace(" @o@me ", " @@@you@@@ ")
        .replace(" Am ", " @@@are@@@ ")
        .replace(" am ", " @@@are@@@ ")
        .replace(" myself ", " @@@yourself@@@ ")
        .replace(" Myself ", " @@@yourself@@@ ")
        .replace(" @o@myself ", " @@@yourself@@@ ")
        .replace(" @o@Myself ", " @@@yourself@@@ ")
        .replace(" mine ", " @@@yours@@@ ")
        .replace(" @o@mine ", " @@@yours@@@ ")
        .replace(" we are ", " @@@you are@@@ ")
        .replace(" we 're ", " @@@you 're@@@ ")
        .replace(" are we ", " @@@are you@@@ ")
        .replace(" We are ", " @@@you are@@@ ")
        .replace(" We 're ", " @@@you 're@@@ ")
        .replace(" are We ", " @@@are you@@@ ")
        .replace(" Are we ", " @@@were you@@@ ")
        .replace(" we were ", " @@@you were@@@ ")
        .replace(" were we ", " @@@were you@@@ ")
        .replace(" We were ", " @@@you were@@@ ")
        .replace(" were We ", " @@@were you@@@ ")
        .replace(" Were we ", " @@@were you@@@ ")
        .replace(" We ", " @@@you@@@ ")
        .replace(" we ", " @@@you@@@ ")
        .replace(" Our ", " @@@your@@@ ")
        .replace(" our ", " @@@your@@@ ")
        .replace(" @o@Us ", " @@@you@@@ ")
        .replace(" @o@us ", " @@@you@@@ ")
        .replace(" ourselves ", " @@@yourselves@@@ ")
        .replace(" Ourselves ", " @@@yourselves@@@ ")
        .replace(" @o@ourselves ", " @@@yourselves@@@ ")
        .replace(" @o@Ourselves ", " @@@yourselves@@@ ")
        .replace(" ours ", " @@@yours@@@ ")
        .replace(" @o@ours ", " @@@yours@@@ ")
        )


def s2f(str):
    str = " " + str + " "
    return (
        str
        .replace(" you are ", " @@@I am@@@ ")
        .replace(" you 're ", " @@@I 'm@@@ ")
        .replace(" You are ", " @@@I am@@@ ")
        .replace(" You 're ", " @@@I 'm@@@ ")
        .replace(" are you ", " @@@am I@@@ ")
        .replace(" Are you ", " @@@am I@@@ ")
        .replace(" you were ", " @@@I was@@@ ")
        .replace(" You were ", " @@@I was@@@ ")
        .replace(" were you ", " @@@was I@@@ ")
        .replace(" Were you ", " @@@was I@@@ ")
        .replace(" Your ", " @@@my@@@ ")
        .replace(" your ", " @@@my@@@ ")
        .replace(" you ", " @@@I@@@ ")
        .replace(" You ", " @@@I@@@ ")
        .replace(" @o@you ", " @@@me@@@ ")
        .replace(" @o@You ", " @@@me@@@ ")
        .replace(" @o@yourself ", " @@@myself@@@ ")
        .replace(" @o@Yourself ", " @@@myself@@@ ")
        .replace(" @o@yourselves ", " @@@myself@@@ ")
        .replace(" @o@Yourselves ", " @@@myself@@@ ")
        .replace(" yours ", " @@@mine@@@ ")
        .replace(" @o@yours ", " @@@mine@@@ ")
        )


def make_input_dic(sentence, parser):
    input_dic = {}
    input_dic['items'] = [item for item in parser(sentence)]
    input_dic['tokens'] = [item.text for item in input_dic['items']]
    input_dic['tags'] = [item.tag_ for item in input_dic['items']]
    input_dic['lems'] = [item.lemma_ for item in input_dic['items']]
    input_dic['dep'] = [item.dep_ for item in input_dic['items']]
    return input_dic


def make_question(input_dic, in_str):
    cap_flg = not in_str.islower()
    v_indice = []
    for tag in vtag_types:
        try:
            v_indice.append(input_dic['tags'].index(tag))
        except:
            pass
    first_verb_id = min(v_indice)
    processed_tokens = copy.copy(input_dic['tokens'])
    if not input_dic['tags'][0] in ['NNP', 'NNPS'] and \
       not input_dic['tokens'][0] in ['I']:
        processed_tokens[0] = input_dic['tokens'][0].lower()
    processed_tokens = [
        "@o@{}".format(processed_tokens[tid]) if input_dic["dep"][tid] in obj_tags else processed_tokens[tid]
        for tid in range(len(processed_tokens))
        ]
    first_verb_lem = input_dic['lems'][first_verb_id]
    first_verb_tag = input_dic['tags'][first_verb_id]
    first_verb = input_dic['tokens'][first_verb_id]
    
    if first_verb.lower() == "'s" and len(input_dic['tokens'])-1 > first_verb_id \
            and input_dic['tokens'][first_verb_id+1].lower() == 'been':
        first_token = 'has'
        processed_tokens = [first_token] + processed_tokens[:first_verb_id] + \
                           processed_tokens[first_verb_id+1:]
        processed_tokens = ["ever" if token=="never" else token for token in processed_tokens]
    
    elif first_verb_lem == 'be':
        first_token = processed_tokens[first_verb_id]
        if first_token in shorten_be_dic:
            first_token = shorten_be_dic[first_token]
        processed_tokens = [first_token] + processed_tokens[:first_verb_id] + \
                           processed_tokens[first_verb_id+1:]
    
    elif first_verb_tag == 'MD':
        first_token = processed_tokens[first_verb_id]
        if first_token in shorten_md_dic:
            first_token = shorten_md_dic[first_token]
        processed_tokens = [first_token] + processed_tokens[:first_verb_id] + \
                           processed_tokens[first_verb_id+1:]
    
    elif (first_verb_lem == 'have' or first_verb_lem == "'ve") and 'VBN' in input_dic['tags']:
        first_token = processed_tokens[first_verb_id]
        if first_token in shorten_hv_dic:
            first_token = shorten_hv_dic[first_token]
        processed_tokens = [first_token] + processed_tokens[:first_verb_id] + \
                           processed_tokens[first_verb_id+1:]
        processed_tokens = ["ever" if token=="never" else token for token in processed_tokens]     

    elif first_verb_tag == 'VBD':
        processed_tokens = ['Did'] + processed_tokens[:first_verb_id] + \
                           [first_verb_lem] + processed_tokens[first_verb_id+1:]
    
    elif first_verb_tag == 'VBZ':
        processed_tokens = ['Does'] + processed_tokens[:first_verb_id] + \
                           [first_verb_lem] + processed_tokens[first_verb_id+1:]
    
    elif first_verb_tag == 'VB' or first_verb_tag == 'VBP':
        processed_tokens = ['Do'] + processed_tokens
    
    else:
        return 'CANNOT MAKE QUESTION: {}'.format(input_dic['tags'])
    
    return_str = ' '.join(processed_tokens).strip().rstrip('.').strip() + ' ?'
    return_str = (s2f(f2s(' {}'.format(return_str)))
        .replace("@@@", "").replace("@o@", "").strip())
    return_str = return_str[0].upper() + return_str[1:] if cap_flg else return_str.lower()
    return return_str


def should_skip(input_dic, in_str):
    v_indice = []
    for tag in vtag_types:
        try:
            v_indice.append(input_dic['tags'].index(tag))
        except:
            pass
    if len(v_indice) < 1:
        return True
    if any([True if tag in noun_tags else False for tag in input_dic["tags"]]):
        return True
    if '?' in in_str or '!' in in_str:
        return True              
    if "n't" in input_dic['tokens'] or "not" in input_dic['tokens']:
        return True
    if "no" in input_dic['tokens'] or "No" in input_dic['tokens']:
        return True
    if "never" in input_dic['tokens'] or "Never" in input_dic['tokens']:
        return True
    if len(in_str.split()) > 30:
        return True
    if any([True if token.lower() in {","} else False for token in input_dic['tokens']]):
        return True
    if "CC" in input_dic['tags']:
        return True
    if not input_dic['tags'][0] in init_tags:
        return True
    if "." in input_dic['tokens'] and input_dic['tokens'].index(".") != len(input_dic['tokens'])-1:
        return True
    if [i for i,le in enumerate(input_dic['lems']) if (le=='here' or le=='there') and input_dic['tags'][i]=='RB']:
        return True

    first_verb_id = min(v_indice)

    if sum([1. if dep in subj_tags else 0. for dep in input_dic['dep'][:first_verb_id]]) > 1:
        return True    

    return False


def simplify_str(in_str):
    l = ' '.join(in_str.strip().split())
    l = ' ' + l + ' '
    return (
        l.lower()
        .replace(' . ',' ')
        .replace(" ? ",' ')
        .replace(' , '," ")
        .replace(' um ',' ')
        .replace(' uh ',' ')
        .replace(' . ',' ')
        .replace(' yeah ',' ')
        .strip()
        )


def have_duplicate(in_str):
    in_tokens = simplify_str(in_str).lower().split()
    n_token = len(in_tokens)
    for n in range(1,n_token//2+1):
        for strt in range(n,n_token-n+1):
            orig = in_tokens[strt-n:strt]
            cmpr = in_tokens[strt:strt+n]
            if orig == cmpr:
                return True
    return False


def count_flen(fname):
    with open(fname) as f:
        for i, _ in enumerate(f):
            pass
    return i+1


def main(args):
    flen = count_flen(args.in_fname)
    parser = spacy.load("en_core_web_sm")
    with open(args.in_fname) as i_f, open(args.out_fname, 'w') as o_f, tqdm(total=flen) as pbar:
        for i,l in enumerate(i_f):
            pbar.update(1)
            if args.num_process > 0 and i >= args.num_process:
                break
            context, res, *label = l.strip().split("\t")
            context, res = context.strip(), res.strip()
            if label and label[0] == 'neutral':
                continue

            # determine whether to skip samples based on premise text 
            c_dic = make_input_dic(context, parser)
            if not any([True if dep in c_req_tags else False for dep in c_dic['dep']]):
                continue
            elif '?' in context:
                continue
            elif not any([True if tag in vtag_types else False for tag in c_dic['tags']]):
                continue
            elif "'" in c_dic['tokens'] or '"' in c_dic['tokens']:
                continue
            
            input_dic = make_input_dic(res, parser)
            if not should_skip(input_dic, res):                
                return_str = make_question(input_dic, res)
                context_str = ' '.join(c_dic['tokens']).strip()
                if context_str[-1] != '.' and context_str[-1] != '!':
                    context_str += ' .'
                if len(context_str.split()) > 30 or len(return_str.split()) > 30:
                    continue
                if have_duplicate(context_str):
                    continue
                res_str = ' '.join(input_dic['tokens']).strip()
                if res_str[-1] != '.' and res_str[-1] != '!':
                    res_str += ' .'
                if label:
                    o_f.write('{}\t{}\t{}\t{}\n'.format(context_str, res_str, return_str, label[0]))
                else:
                    o_f.write('{}\t{}\t{}\n'.format(context_str, res_str, return_str))


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-fname", required=True)
    parser.add_argument("--out-fname", required=True)
    parser.add_argument("--num-process", type=int, default=-1)

    args = parser.parse_args()

    main(args)