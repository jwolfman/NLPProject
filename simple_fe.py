import string, nltk

def read_file(filename):
    r"""Assume the file is the format
    word \t tag
    word \t tag
    [[blank line separates sentences]]
    
    This function reads the file and returns a list of sentences.  each
    sentence is a pair (tokens, tags), each of which is a list of strings of
    the same length.
    """
    sentences = open(filename).read().strip().split("\n\n")
    ret = []
    for sent in sentences:
        lines = sent.split("\n")
        pairs = [L.split("\t") for L in lines]
        tokens = [tok for tok,tag in pairs]
        tags = [tag for tok,tag in pairs]
        ret.append( (tokens,tags) )
    return ret

def clean_str(s):
    """Clean a word string so it doesn't contain special crfsuite characters"""
    return s.replace(":","_COLON_").replace("\\", "_BACKSLASH_")

def extract_features_for_sentence1(tokens):
    N = len(tokens)
    feats_per_position = [set() for i in range(N)]
    for t in range(N):
        w = clean_str(tokens[t])
        feats_per_position[t].add("word=%s" % w)
    return feats_per_position

def extract_features_for_sentence2(tokens):
    N = len(tokens)
    feats_per_position = [set() for i in range(N)]
    PoS=nltk.pos_tag(tokens)
    for t in range(N):
        w = clean_str(tokens[t])
        tag="O"
        if "NNP" in PoS[t] or "NNPS" in PoS[t]:
            tag="B"
        if tag=="B":
            #if containsSymbol(w):
            #    tag="O"
            if isMonth(w):
                tag="O"
        feats_per_position[t].add("%s\tword=%s" %(tag,w))
    return feats_per_position
#def containsSymbol(word):

def isMonth(word):
    months={
        #"jan":True,
        "january":True,
        "feb":True,
        "february":True,
        "mar":True,
        "march":True,
        "apr":True,
        #"april":True,
        "jun":True,
        #"june":True,
        "jul":True,
        "july":True,
        "aug":True,
        "august":True,
        "sep":True,
        "september":True,
        "oct":True,
        "october":True,
        "nov":True,
        "november":True,
        "dec":True,
        "december":True
    }
    if word.lower() in months:
        return True
    return False

extract_features_for_sentence = extract_features_for_sentence2

def extract_features_for_file(input_file, output_file):
    """This runs the feature extractor on input_file, and saves the output to
    output_file."""
    sents = read_file(input_file)
    with open(output_file,'w') as output_fileobj:
        for tokens,goldtags in sents:
            feats = extract_features_for_sentence(tokens)
            for t in range(len(tokens)):
                feats_tabsep = "\t".join(feats[t])
                print>>output_fileobj, "%s" % (feats_tabsep)
            print>>output_fileobj, ""

extract_features_for_file("train.txt", "train.feats")
extract_features_for_file("dev.txt", "dev.feats")
