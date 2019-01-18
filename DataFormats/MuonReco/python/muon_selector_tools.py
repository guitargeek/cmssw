import re
import os

def between(s, a, b):
    s = s[s.find(a)+len(a):]
    s = s[:s.find(b)]
    return s

def remove_cpp_comments(code):
    """
    Remove comments from C++ code
    From https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
    """
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, code)

def muon_selector_bitflag(selection):

    filepath = os.path.join(os.environ['CMSSW_BASE'], "src/DataFormats/MuonReco/interface/Muon.h")

    with open(filepath, 'r') as f:
        muon_code = f.read()

    muon_code = remove_cpp_comments(muon_code)
    muon_code = muon_code.replace(" ", "").replace("\n", "")

    if not "enumSelector{" in muon_code:
        raise ValueError("The pat::Muon declaration for commit %s does not contain an enum named Selector! " + \
                         "Maybe something changed in the source code?")

    selector_code = between(muon_code, "enumSelector{", "}")

    muon_selectors = {}

    for name, bit in [x.split("=1UL<<") for x in selector_code.split(",")]:
        muon_selectors[name] = str(1 << int(bit))

    for name, bit in muon_selectors.items():
        selection = selection.replace(name, bit)

    selection = selection.replace(" ", "").split("and")

    try:
        for i in range(len(selection)):
            selection[i] = int(selection[i])
    except:
        raise ValueError('Your muon selector string either contains ID names that are not in the selection bitflag' + \
                         'or uses an operator other than "and".\n' + "Possible ID names are:\n    " + \
                         "\n    ".join(muon_selectors.keys()))

    bitset = reduce(lambda a, b: a | b, selection)

    return bitset
