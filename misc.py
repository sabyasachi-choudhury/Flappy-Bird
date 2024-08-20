import translate

CODES = 'ab aa af ak am an ar as av ay az ba be bg bi bm bn bo br bs ca ce ch co cr cus cu cv cy da de dv dz ee el eo es et eu fa ff fi fj fo fr fy ga gl gn gu gv hr ht hu ia id ie ja jv ka kl km kn ko li ln lo na nb nd ne oc oj pa pi ps pt qu sa sc sd se sq sr ss st ta te tg th ti wa ve ur ty xh zh zu wo'.split(' ')
for code in CODES:
    try:
        T = translate.Translator(to_lang=code)
        res1 = T.translate('peace')
        res2 = T.translate('hate')
        if res1[0] == "'":
            pass
        else:
            print(res1, "         ", res2)
    except:
        pass