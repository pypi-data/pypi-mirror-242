from typing import Dict,List, Tuple

from text2story.readers.token_corpus import TokenCorpus
from text2story.core.utils import join_tokens

def select_srlinks(narrative_elements:Dict[str,List[TokenCorpus]]) -> List[Tuple[str, str, str]]:
    """
    This method selects the semantic links of each narrative element

    @param narrative_elements: a dictionary of narrative components
    @return: a triplet list (text of component 1, relationship, text of component 2)
    """
    relations = select_links(narrative_elements)
    ans =  []
    for r in relations:
        t1, rel, t2 = r
        if rel.startswith('SRLINK'):
            ans.append(r)
    return ans

def select_links(narrative_elements:Dict[str,List[TokenCorpus]]) -> List[Tuple[str, str, str]]:
    rel_lst = {}
    for id_ann in narrative_elements:
        # get only the first token of the sequence of annotation
        # is enough to get the relations that this component is involved
        tok = narrative_elements[id_ann][0]

        for rel in tok.relations:
            if rel.rel_id not in rel_lst:

                tok_lst_1 = [t.text for t in narrative_elements[id_ann]]
                tok_lst_2 = [t.text for t in rel.toks]

                rel_lst[rel.rel_id] = (join_tokens(tok_lst_1), rel.rel_type,join_tokens(tok_lst_2))

    return list(rel_lst.values())