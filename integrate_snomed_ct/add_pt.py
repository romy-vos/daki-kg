import pandas as pd

# Add your own paths to your SNOMED CT dir
path_descr_en = "SnomedCT_ManagedServiceNL_PRODUCTION_NL1000146_20241031T120000Z/Snapshot/Terminology/sct2_Description_Snapshot-en_NL1000146_20241031.txt"
path_lang_en = "SnomedCT_ManagedServiceNL_PRODUCTION_NL1000146_20241031T120000Z/Snapshot/Refset/Language/der2_cRefset_LanguageSnapshot-en_NL1000146_20241031.txt"

output_path = "sct_pt_en.tsv"

def filter_concepts(path_descr, path_lang):
    """Filter snomed file on active, PT concepts.
    Returns df with active, PT concepts, terms, language."""

    descr = pd.read_csv(path_descr, sep = "\t", dtype = str)
    lang = pd.read_csv(path_lang, sep = "\t", dtype = str)

    # filter active concepts 
    lang_a = lang[lang.active == "1"].copy()
    descr_a = descr[descr.active == "1"].copy()

    # filter preferred terms
    PT = "900000000000548007"
    lang_pt = lang_a[lang_a.acceptabilityId == PT].copy()

    # merge
    terms_ac_pt = descr_a.merge(lang_pt, right_on = "referencedComponentId", left_on = "id")[["conceptId", "term"]].drop_duplicates(subset = "conceptId", keep = "first")
    return terms_ac_pt

res_en = filter_concepts(path_descr_en, path_lang_en)

# subset the concepts relevant to DAKI-KG
rel_concepts = pd.read_csv("all_relevant_sct_concepts.tsv", dtype = "str", sep = "\t")
rel_concepts.rename(columns = {"?conceptId": "conceptId"}, inplace = True)

pt_en = rel_concepts.merge(res_en, on = "conceptId", how = "left")

pt_en.to_csv("sct_pt_en.tsv", sep = "\t", index = False)
#pt_nl.to_csv("sct_pt_nl.tsv", sep = "\t", index = False)