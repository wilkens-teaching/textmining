# Text Mining the Novel

## Contact

[Matthew Wilkens](https://english.nd.edu/people/faculty/wilkens/), University of Notre Dame\
CDT 30380 / ENGL 30010, Spring 2019\
MW 11:00-12:15, [246 Hesburgh Library](https://cds.library.nd.edu/spaces/)\
Office hours: Th 9:00-5:00 ([reserve slots](https://bit.ly/wilkens_appointments)), 320 Decio Hall. 
>**Note:** I'm generally in my office all day on Thursdays, but I do sometimes have a conflict or need to step out. Reservations are strongly recommended.

## Summary
A technical, undergraduate-level course in quantitive and computational approaches to analyzing large bodies of text. 

## Description

Broadly speaking, the course covers text mining, content analysis, and basic machine learning, emphasizing (but not limited to) approaches with demonstrated value in literary studies. Students will learn how to clean and process textual corpora, extract information from unstructured texts, identify relevant textual and extra-textual features, assess document similarity, cluster and classify authors and texts using a variety of machine-learning methods, visualize the outputs of statistical models, and incorporate quantitative evidence into literary and humanistic analysis.

Most of the methods treated in the class are relevant in other fields. Students from all majors are welcome. No prerequisites, but some programming experience strongly recommended. Taught in Python. Counts toward the Digital Humanities track of the [Idzik Computing and Digital Technologies (CDT)](https://cdt.nd.edu/) minor and as a free elective in the [Data Science minor](https://datascienceminor.nd.edu/).  

## Texts

### Required

Bengfort, Benjamin, Rebecca Bilbro, and Tony Ojeda.[ _Applied Text Analysis with Python_](http://shop.oreilly.com/product/0636920052555.do). O'Reilly, 2018.\
See the book's [associated GitHub repo](https://github.com/foxbook/atap) for code samples and related data sets.

### Optional

Guttag, John V. [_Introduction to Computation and Programming Using Python_](https://mitpress.mit.edu/books/introduction-computation-and-programming-using-python-second-edition). 2nd. ed. MIT, 2016.\
Useful for students without a strong background in Python. See linked MIT Press site for code samples and information about the associated EdX course.

Raschka, Sebastian and Vahid Mirjalili. [_Python Machine Learning_](https://www.packtpub.com/big-data-and-business-intelligence/python-machine-learning-second-edition). 2nd ed. Packt, 2017.\
A more general-purpose textbook on machine learning. Greater emphasis on neural networks, less on working with textual data.

## Objectives

The primary objective of the course is to build proficiency in applied text analysis and data mining. Students who complete the course will have knowledge of standard approaches to text analysis and will be familiar with the humanistic ends to which those approaches might be put. Secondary objectives include acquiring basic understanding of relevant literary history, of integrating quantitative with qualitative evidence, and of best practices in data science project management.

## Work and grading

In addition to weekly problem sets, you will be required to complete one project proposal of about 1,000 words, a brief in-class presentation, and a final project that employs computational techniques covered in the course. Overall grades will be based on the problem sets (35% in sum), proposal (10%), presentation (5%), final project (30%), and class participation (20%). _You must satisfactorily complete all assignments to pass the course._


## Policy statements

### Attendance

Two absences (one week of meetings), no questions asked. Additional absences will lower your grade.

### Late work

Late work is generally not accepted. If you find yourself in exceptional circumstances, talk to me well in advance of the deadline and we may be able to find an accommodation.

### Collaboration and plagiarism

Talking to other students -- especially those in the course -- about your ideas is a good thing. Taking other people's words, code, or ideas without attribution is plagiarism and will result in honor-code-related unpleasantness. When in doubt, cite. And feel free to ask me about specific cases or problems and about the mechanics of research documentation. For references and guidelines, see the library's [plagiarism](https://libguides.library.nd.edu/friendly.php?s=scholarly-publishing/plagiarism) and [documentation](https://libguides.library.nd.edu/scholarly-publishing/writing-citing) sites and the university's [academic code of honor](https://honorcode.nd.edu/).

### Disabilities

Students with documented disabilities who need accommodations or have questions should speak with me directly and contact [Sara Bea Disability Services](https://sarabeadisabilityservices.nd.edu/).

## Schedule

Detailed assignments will be provided separately.

**Note: All dates and assignments are subject to change.** The schedule after spring break is tentative due to weather-related changes. Specific day-to-day assignments will be updated as the time draws nearer.

**Week 1** 

* Weds, 1/16. Introduction, background, mechanics.

**Week 2** 

* Mon, 1/21. **No class** (MLK Day).
* Weds, 1/23. 
  * Read Bengfort et al., chapter 1 (language and computation). 
  * Due: [Implement `parse_gender` function](https://github.com/wilkens-teaching/textmining/blob/master/exercises/01%20gender.ipynb) as described (pp. 10-12). Submit output for three literary texts from the class corpus on GitHub. [[Answer]](https://github.com/wilkens-teaching/textmining/blob/master/exercises/01%20gender%20answer.ipynb).

**Week 3** 

* Mon, 1/28. 
  * Read chapter 2 (corpora).
* Weds, 1/30. **No class** (university closed due to severe weather).
 
**Week 4** 

* Mon, 2/4. **No class** (instructor travel).
* Weds, 2/6. 
  * Due: [Write an NLTK `PlaintextCorpusReader` function that ingests the class corpus](https://github.com/wilkens-teaching/textmining/blob/master/exercises/02%20corpus%20reader.ipynb).[[Answer]](https://github.com/wilkens-teaching/textmining/blob/master/exercises/02%20corpus%20reader%20answer.ipynb).
  * Read chapter 3 (preprocessing).

**Week 5** 

* Mon, 2/11.
  * Read chapter 4 (vectorization).
* Weds, 2/13.
  * Due: [Build a processed and pickled version of the class corpus as described in the chapter, then work with the data](https://github.com/wilkens-teaching/textmining/blob/master/exercises/03%20corpus%20reader%20advanced.ipynb).

**Week 6**

* Mon, 2/18. **No class** (instructor travel).
* Weds, 2/20.
  * Read chapter 5 (classification).
  * Due: Vectorize the corpus using the Scikit-Learn `TfidfVectorizer`. Visualize output via PCA.

**Week 7**

* Mon, 2/25.
  * Read chapter 6 (clustering).
* Weds, 2/27. **No class** (instructor travel).

**Week 8**

* Mon, 3/4.
  * Due: Build and evaluate a system that classifies corpus texts as *either* male/female *or* British/American.
* Weds, 3/6.
  * Read chapter 7 (context-aware analysis).

**Week 9. Spring break.** No class meetings.

**Week 10**

* Mon, 3/18.
  * Due: Build a system that performs topic modeling on the corpus texts and clusters those texts based on their topical content.
* Weds, 3/20.
  * Read chapter 8 (visualization).
  * Read Tufte article.

**Week 11**

* Mon, 3/25.
  * Read chapter 9 (networks).
  * Due: Reimplement the gender/nationality classification system using n-gram features as described in chapter 7. Evaluate the performance of the new model relative to the unigram original.
* Weds, 3/27.
  * Read Underwood, Bamman, and Lee article.

**Week 12**

* Mon, 4/1.
  * Read chapter 11 (multiprocessing). Note that we will skip chapter 10 (chatbots).
  * Due: Visualization exercise.
* Weds, 4/3.

**Week 13**

* Mon, 4/8.
  * Read chapter 12 (neural networks).
  * Due: Implement entity resolution via graph structure to select the entities in one corpus text.
* Weds, 4/10.
  * Due: Project proposal.

**Week 14**

* Mon, 4/15. Topics and readings to be determined by class.
* Weds, 4/17. Topics and readings to be determined by class.
  * Due: Reimplement your classification system to run on multiple cores. Evaluate time improvement for classification over the corpus.

**Week 15**

* Mon, 4/22. In-class work session.
* Weds, 4/24. In-class work session.

**Week 16**

* Presentations and conclusions.

**Week 17**

Final project due in lieu of exam, Weds, 5/8, 6:15pm.
