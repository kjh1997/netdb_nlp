import nltk
stemmer2 = nltk.stem.PorterStemmer()
def stem2(word):
    print(word)
    data = []
    for i in word: data.append(stemmer2.stem(i))
    print(stemmer2.stem("working"),stemmer2.stem("Working"))
    return data


a ='''abs we present a calculus for processing semistructured data that spans differences of application area among several novel query languages, broadly categorized as "nosql". this calculus lets users define their own operators, capturing a wider range of data processing capabilities, whilst providing a typing precision so far typical only of primitive hard-coded operators. the type inference algorithm is based on semantic type checking, resulting in type information that is both precise, and flexible enough to handle structured and semistructured data. we illustrate the use of this calculus by encoding a large fragment of jaql, including operations and iterators over json, embedded sql expressions, and co-grouping, and show how the encoding directly yields a typing discipline for jaql as it is, namely without the addition of any type definition or type annotation in the code. © 2013 acm.'''
punct = set(u''':!),©.:;?.]}¢'"、。〉》」』〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：#@；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､￠
々‖•·ˇˉ―′’”([{£¥'"‵〈《「『〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘_…/''')

def clean_sentence(text, stemming=False):
    for token in punct:
        text = text.replace(token, "")
    words = text.split()
    if stemming:
        stemmed_words = []
        for w in words:
            stemmed_words.append(stem2(w))
        words = stemmed_words
    return words

print(stem2(clean_sentence(a)))