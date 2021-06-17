from natasha import Segmenter, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser,Doc
import svgling

segmenter = Segmenter()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)

text = 'Понимание	смысла	трактуется как	переход	от текста к формализованному представлению его смысла.'
doc = Doc(text)

doc.segment(segmenter)
doc.tag_morph(morph_tagger)
doc.parse_syntax(syntax_parser)

print(doc.sents[0].syntax.print())


