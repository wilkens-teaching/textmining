DOC_PATTERN = r'.+\.txt'        # Documents are just files that end in '.txt'
PKL_PATTERN = r'.+\.pickle'     # Pickled files end in .pickle
CAT_PATTERN = r'([a-z_\s]+)/.*' # We won't use this, but fall back to directory-based labels
                                # if no other labels are supplied

import codecs
import nltk
import os
import pickle
import time
import unicodedata
from   glob import glob
from   nltk import pos_tag, sent_tokenize, wordpunct_tokenize
from   nltk.corpus import wordnet as wn
from   nltk.corpus.reader.api import CorpusReader
from   nltk.corpus.reader.api import CategorizedCorpusReader
from   nltk.stem.wordnet import WordNetLemmatizer

def make_cat_map(path, extension):
    """
    Takes a directory path and file extension (e.g., 'txt').
    Returns a dictionary of file:category mappings from standard file names:
      nation-author-title-year-gender
    """
    file_paths = glob(os.path.join(path, f'*.{extension}'))
    file_names = [os.path.split(i)[1] for i in file_paths]
    category_map = {} # Dict to hold filename:[categories] mappings
    for file in file_names:
        parsed = file.rstrip(f'.{extension}').split('-') # strip extension and split on hyphens
        nation = parsed[0]
        gender = parsed[4]
        category_map[file] = [nation, gender, nation+gender]
    return category_map

class TMNCorpusReader(CategorizedCorpusReader, CorpusReader):
    """
    A corpus reader for categorized text documents to enable preprocessing.
    """
    
    def __init__(
        self, 
        root, 
        fileids=DOC_PATTERN,
        encoding='utf8', 
        **kwargs
    ):
        """
        Initialize the corpus reader.  Categorization arguments
        (``cat_pattern``, ``cat_map``, and ``cat_file``) are passed to
        the ``CategorizedCorpusReader`` constructor.  The remaining
        arguments are passed to the ``CorpusReader`` constructor.
        """
        # Add the default category pattern if not passed into the class.
        if not any(key.startswith('cat_') for key in kwargs.keys()):
            # First, try to build a cat_map from standard-style filenames
            try: 
                kwargs['cat_map'] = make_cat_map(root, 'txt')
            # On error, fall back to dir names for categories    
            except Exception as e:
                print(type(e), e, "\nUnable to build category map from file names.\nFalling back to categories by directory name.")
                kwargs['cat_pattern'] = CAT_PATTERN

        # Initialize the NLTK corpus reader objects
        CategorizedCorpusReader.__init__(self, kwargs)
        CorpusReader.__init__(self, root, fileids, encoding)
        
    def resolve(self, fileids, categories):
            """
            Returns a list of fileids or categories depending on what is passed
            to each internal corpus reader function. Implemented similarly to
            the NLTK ``CategorizedPlaintextCorpusReader``.
            """
            if fileids is not None and categories is not None:
                raise ValueError("Specify fileids or categories, not both")

            if categories is not None:
                return self.fileids(categories)
            return fileids

    def docs(self, fileids=None, categories=None):
        """
        Returns the complete text of a document, closing the document
        after we are done reading it and yielding it in a memory safe fashion.
        """
        # Resolve the fileids and the categories
        fileids = self.resolve(fileids, categories)

        # Create a generator, loading one document into memory at a time.
        for path, encoding in self.abspaths(fileids, include_encoding=True):
            with codecs.open(path, 'r', encoding=encoding) as f:
                yield f.read()

    def sizes(self, fileids=None, categories=None):
        """
        Returns a list of tuples, the fileid and size on disk of the file.
        This function is used to detect oddly large files in the corpus.
        """
        # Resolve the fileids and the categories
        fileids = self.resolve(fileids, categories)

        # Create a generator, getting every path and computing filesize
        for path in self.abspaths(fileids):
            yield os.path.getsize(path)
            
    def paras(self, fileids=None, categories=None):
        """
        Uses splitlines() to parse the paragraphs from plain text.
        """
        # Resolve the fileids and the categories
        fileids = self.resolve(fileids, categories)
        
        for doc in self.docs(fileids):
            for par in doc.splitlines():
                if len(par) > 0:
                    yield par

    def sents(self, fileids=None, categories=None):
        """
        Uses the built in sentence tokenizer to extract sentences from the
        paragraphs.
        """
        # Resolve the fileids and the categories
        fileids = self.resolve(fileids, categories)
        
        for paragraph in self.paras(fileids):
            for sentence in sent_tokenize(paragraph):
                yield sentence

    def words(self, fileids=None, categories=None):
        """
        Uses the built in word tokenizer to extract tokens from sentences.
        """
        # Resolve the fileids and the categories
        fileids = self.resolve(fileids, categories)
        
        for sentence in self.sents(fileids):
            for token in wordpunct_tokenize(sentence):
                yield token

    def describe(self, fileids=None, categories=None):
        """
        Performs a single pass of the corpus and
        returns a dictionary with a variety of metrics
        concerning the state of the corpus.
        """
        started = time.time()

        # Structures to perform counting.
        counts  = nltk.FreqDist()
        tokens  = nltk.FreqDist()

        # Perform single pass over paragraphs, tokenize and count
        for para in self.paras(fileids, categories):
            counts['paras'] += 1

            for sent in sent_tokenize(para):
                counts['sents'] += 1

                for word in wordpunct_tokenize(sent):
                    counts['words'] += 1
                    tokens[word] += 1

        # Compute the number of files and categories in the corpus
        n_fileids = len(self.resolve(fileids, categories) or self.fileids())
        n_topics  = len(self.categories(self.resolve(fileids, categories)))

        # Return data structure with information
        return {
            'files':  n_fileids,
            'categories': n_topics,
            'paragraphs':  counts['paras'],
            'sentences':  counts['sents'],
            'words':  counts['words'],
            'vocabulary_size':  len(tokens),
            'lexical_diversity': float(counts['words']) / float(len(tokens)),
            'paras_per_doc':  float(counts['paras']) / float(n_fileids),
            'words_per_doc':  float(counts['words']) / float(n_fileids),
            'sents_per_para':  float(counts['sents']) / float(counts['paras']),
            'secs':   time.time() - started,
        }
    
class PickledCorpusReader(CategorizedCorpusReader, CorpusReader):

    def __init__(self, root, fileids=PKL_PATTERN, **kwargs):
        """
        Initialize the corpus reader.  Categorization arguments
        (``cat_pattern``, ``cat_map``, and ``cat_file``) are passed to
        the ``CategorizedCorpusReader`` constructor.  The remaining arguments
        are passed to the ``CorpusReader`` constructor.
        """
        # Add the default category pattern if not passed into the class.
        if not any(key.startswith('cat_') for key in kwargs.keys()):
            # First, try to build a cat_map from standard-style filenames
            try: 
                kwargs['cat_map'] = make_cat_map(root, 'pickle')
            # On error, fall back to dir names for categories    
            except Exception as e:
                print(type(e), e, "\nUnable to build category map from file names.\nFalling back to categories by directory name.")
                kwargs['cat_pattern'] = CAT_PATTERN

        CategorizedCorpusReader.__init__(self, kwargs)
        CorpusReader.__init__(self, root, fileids)

    def resolve(self, fileids, categories):
        """
        Returns a list of fileids or categories depending on what is passed
        to each internal corpus reader function. This primarily bubbles up to
        the high level ``docs`` method, but is implemented here similar to
        the nltk ``CategorizedPlaintextCorpusReader``.
        """
        if fileids is not None and categories is not None:
            raise ValueError("Specify fileids or categories, not both")

        if categories is not None:
            return self.fileids(categories)
        return fileids

    def docs(self, fileids=None, categories=None):
        """
        Returns the document loaded from a pickled object for every file in
        the corpus. Similar to the BaleenCorpusReader, this uses a generator
        to acheive memory safe iteration.
        """
        # Resolve the fileids and the categories
        fileids = self.resolve(fileids, categories)

        # Create a generator, loading one document into memory at a time.
        for path, enc, fileid in self.abspaths(fileids, True, True):
            with open(path, 'rb') as f:
                yield pickle.load(f)

    def paras(self, fileids=None, categories=None):
        """
        Returns a generator of paragraphs where each paragraph is a list of
        sentences, which is in turn a list of (token, tag) tuples.
        """
        for doc in self.docs(fileids, categories):
            for paragraph in doc:
                yield paragraph

    def sents(self, fileids=None, categories=None):
        """
        Returns a generator of sentences where each sentence is a list of
        (token, tag) tuples.
        """
        for paragraph in self.paras(fileids, categories):
            for sentence in paragraph:
                yield sentence

    def tagged(self, fileids=None, categories=None):
        for sent in self.sents(fileids, categories):
            for token in sent:
                yield token

    def words(self, fileids=None, categories=None):
        """
        Returns a generator of (token, tag) tuples.
        """
        for token in self.tagged(fileids, categories):
            yield token[0]
            
class Preprocessor(object):
    """
    The preprocessor wraps a corpus object (usually a `TMNCorpusReader`)
    and manages the stateful tokenization and part of speech tagging into a
    directory that is stored in a format that can be read by the
    `PickledCorpusReader`.
    """

    def __init__(self, corpus, target=None, **kwargs):
        """
        The corpus is the `TMNCorpusReader` to preprocess and pickle.
        The target is the directory on disk to output the pickled corpus to.
        """
        self.corpus = corpus
        self.target = target

    def fileids(self, fileids=None, categories=None):
        """
        Helper function access the fileids of the corpus
        """
        fileids = self.corpus.resolve(fileids, categories)
        if fileids:
            return fileids
        return self.corpus.fileids()

    def abspath(self, fileid):
        """
        Returns the absolute path to the target fileid from the corpus fileid.
        """
        # Find the directory, relative from the corpus root.
        parent = os.path.relpath(
            os.path.dirname(self.corpus.abspath(fileid)), self.corpus.root
        )

        # Compute the name parts to reconstruct
        basename  = os.path.basename(fileid)
        name, ext = os.path.splitext(basename)

        # Create the pickle file extension
        basename  = name + '.pickle'

        # Return the path to the file relative to the target.
        return os.path.normpath(os.path.join(self.target, parent, basename))

    def tokenize(self, fileid, chunksize=0):
        """
        Segments, tokenizes, and tags a document in the corpus. Returns a
        generator of paragraphs, which are lists of sentences, which in turn
        are lists of part of speech tagged words.
        """
        if chunksize==0:
            for paragraph in self.corpus.paras(fileids=fileid):
                yield [
                    pos_tag(wordpunct_tokenize(sent))
                    for sent in sent_tokenize(paragraph)
                ]
        else:
            wc=0 # running count of tokens in current chunk
            chunk = []
            for paragraph in self.corpus.paras(fileids=fileid):
                if wc<chunksize:
                    tagged_par = [
                            pos_tag(wordpunct_tokenize(sent))
                            for sent in sent_tokenize(paragraph)
                        ]
                    wc += sum(len(tagged_sent) for tagged_sent in tagged_par)
                    chunk.append(tagged_par)
                else:
                    yield chunk
                    wc=0
                    chunk=[]
                    tagged_par = [
                            pos_tag(wordpunct_tokenize(sent))
                            for sent in sent_tokenize(paragraph)
                        ]
                    wc += sum(len(tagged_sent) for tagged_sent in tagged_par)
                    chunk.append(tagged_par)
            yield chunk
          
    def is_punct(self, token):
        return all(
            unicodedata.category(char).startswith('P') for char in token
        )

    def wn_lemmatize(self, token, pos_tag):
        tag = {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }.get(pos_tag[0], wn.NOUN)
        return WordNetLemmatizer().lemmatize(token, tag) 

    def normalize(self, sentence):
        """
        Given a wordpunct tokenized sentence, return same as list of lemmas,
        lowercased and with punctuation removed.
        """
        
        return [
            self.wn_lemmatize(token, tag).lower()
            for (token, tag) in pos_tag(sentence)
            if not self.is_punct(token)
        ]
        
    
    def tokenize_norm(self, fileid, chunksize=0):
        """
        Segments, tokenizes, normalizes, and lemmatizes a document in the corpus. 
        Returns a generator of paragraphs, which are lists of sentences, 
        which in turn are lists of lemmatized words.
        """
        if chunksize==0:
            for paragraph in self.corpus.paras(fileids=fileid):
                yield [
                    self.normalize(wordpunct_tokenize(sent))
                    for sent in sent_tokenize(paragraph)
                ]
        else:
            wc=0 # running count of tokens in current chunk
            chunk = []
            for paragraph in self.corpus.paras(fileids=fileid):
                if wc<chunksize:
                    tagged_par = [
                            self.normalize(wordpunct_tokenize(sent))
                            for sent in sent_tokenize(paragraph)
                        ]
                    wc += sum(len(tagged_sent) for tagged_sent in tagged_par)
                    chunk.append(tagged_par)
                else:
                    yield chunk
                    wc=0
                    chunk=[]
                    tagged_par = [
                            self.normalize(wordpunct_tokenize(sent))
                            for sent in sent_tokenize(paragraph)
                        ]
                    wc += sum(len(tagged_sent) for tagged_sent in tagged_par)
                    chunk.append(tagged_par)
            yield chunk
   

    def process(self, fileid, chunksize=0, norm=False):
        """
        For a single file does the following preprocessing work:
            1. Checks the location on disk to make sure no errors occur.
            2. Gets all paragraphs for the given text.
            3. Segements the paragraphs with the sent_tokenizer
            4. Tokenizes the sentences with the wordpunct_tokenizer
            5. Tags the sentences using the default pos_tagger
            6. Writes the document as a pickle to the target location.
        This method is called multiple times from the transform runner.
        """
        # Compute the outpath to write the file to.
        target = self.abspath(fileid)
        parent = os.path.dirname(target)

        # Make sure the directory exists
        if not os.path.exists(parent):
            os.makedirs(parent)

        # Make sure that the parent is a directory and not a file
        if not os.path.isdir(parent):
            raise ValueError(
                "Please supply a directory to write preprocessed data to."
            )

        # Create a data structure for the pickle
        if norm:
            document = list(self.tokenize_norm(fileid, chunksize))
        else:
            document = list(self.tokenize(fileid, chunksize))

        # Open and serialize the pickle to disk
        if chunksize==0: # Document not chunked
            with open(target, 'wb') as f:
                pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)
        else: # Document chunked
            for seq, chunk in enumerate(document):
                name, ext = os.path.splitext(target)
                out_file = name + '-' + str(seq).zfill(5) + ext
                with open(out_file, 'wb') as f:
                    pickle.dump(chunk, f, pickle.HIGHEST_PROTOCOL)
            

        # Clean up the document
        del document

        # Return the target fileid
        return target

    def transform(self, fileids=None, categories=None, chunksize=0, norm=False):
        """
        Transform the wrapped corpus, writing out the segmented, tokenized,
        and part of speech tagged corpus as a pickle to the target directory.
        This method will also directly copy files that are in the corpus.root
        directory that are not matched by the corpus.fileids().
        """
        # Make the target directory if it doesn't already exist
        if not os.path.exists(self.target):
            os.makedirs(self.target)

        # Resolve the fileids to start processing and return the list of 
        # target file ids to pass to downstream transformers. 
        return [
            self.process(fileid, chunksize=chunksize, norm=norm)
            for fileid in self.fileids(fileids, categories)
        ]