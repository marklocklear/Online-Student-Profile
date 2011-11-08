#!/usr/bin/python
"""jungian - Jungian typology instument tools.

This module contains classes (or a class- so far)
for scoring and representing the results for jungian typology.

This module is provided on an as is basis without warranty
and it's function with a given instrument should be verified.
There is no substitute for a competent psychiatric professional
(note, I am a programmer and _not_ a psychiatric professional).
There is also no substitute for the scientific method and lots of data.
Feel free to use at your own risk.
This tool may not produce correct or scientifically valid results.
This software is provided under the terms of the GPL
http://creativecommons.org/licenses/GPL/2.0/
"""
__author__ = "Luke Arno <luke.arno@cpcc.edu> <lda@psynrg.com>"
__date__ = "23 May 2004"
__version__ = "0.4.2"
__credits__ = """Guido van Rossum and the Python community.
Central Piedmont Community College (for supporting OSS).

The Truth is dead. Long live The Truth."""



class TypeAnalysis(object):
   """Score a jungian typology instruments and represent the results."""
   TYPES_IN_ORDER = ['E','I','S','N','F','T','J','P']

   def __init__(self, args, likert, scale=10):
      """Make type analysis from quesiton responses.

      args     - question responses - dictionary

      should be like  {'INTP1':2, 'INTP2':-1, 'ESTP1':1, ...}
      with the first four characters of the key indicating type
      and the values representing Likert scale selections
      a dictionary of form fields
      for a jungian typology instrument, for instance

      likert   - size of Likert scale - int

      the width of the likert scale,
      which must be a range of integers
      whose endpoints should be inverse
      (for a 2 to -2 scale, self.likert = 4)

      scale    - scale of results - int

      the scale of the results as an integer so...
      default is 10 for a scale of 0 to 10
      """
      self.args = args
      self.scale = scale
      self.pointsAvailable = (likert/2)*len(args)
      self.__rawScore()
      self.__compute()

   def __rawScore(self):
      """Total raw scores for each side of each dichotomy

      sets self.rawScores to a dictionary of 4 dictionary dicotomies
      with the total points as values
      based on the dict self.args (see self.__init__.__doc__)
      """
      self.rawScores = [{},{},{},{}]
      for k, v in self.args.items():
         pos = 0
         for char in k[:4]:
            try:
               self.rawScores[pos][char] += int(v)
            except:
               self.rawScores[pos][char] = int(v)
            pos+=1

   def __compute(self):
      """Compute the type for a jungian typology raw score

      [{'I':44,'E':-32},{,...},...]
      takes like [{'I':44,'E':-32},{,...},...]
      a list of 4 dictionary dicotomies
      return like [('I', 2),('N',6),('T',7),('P',9)]
      a list of tuples representing the dominant side of each dichotomy
      and its proportional dominance on a scale of 0 to self.scale
      """
      self.computedScores = []
      for dichotomy in self.rawScores:
         dich = dichotomy.items()
         if dich[0][1] > dich[1][1]:
               self.computedScores.append(
                     (dich[0][0], dich[0][1] - dich[1][1])
                  )
         else:
               self.computedScores.append(
                     (dich[1][0], dich[1][1] - dich[0][1])
                  )
      algo = lambda x: (x[0], int(
            (float(x[1])/float(self.pointsAvailable)) \
               * float(self.scale))
         )
      self.computedScores = map(algo, self.computedScores)

      # We want our graph scores to look like percentages instead of
      # "how far over 50% in one direction are you?"
      self.graphScores = [(s[0],
                           (s[1] + float(self.scale)) / (float(self.scale) * 2))
                          for s in self.computedScores]
      # for score in seven_years_ago:
      # for score in self.computedScores:
      #     new_score = (score[1] + float(self.scale)) / (float(self.scale) * 2)
      #     graph_scores.append((score[0], new_score))
      # self.graphScores = graph_scores

   def type(self):
      return "".join([t for (t, s) in self.computedScores])
   def toPyfo(self):
      raws = []
      [raws.extend(r.items()) for r in self.rawScores]
      return ('analysis',
              [('computedScores',
                [(k, str(v)) for (k, v) in self.computedScores]),
               ('rawScores', raws),
               ('scale', self.scale),
               ('dichotomy', [('aspect', x) for x in ['I', 'E']]),
               ('dichotomy', [('aspect', x) for x in ['N', 'S']]),
               ('dichotomy', [('aspect', x) for x in ['T', 'F']]),
               ('dichotomy', [('aspect', x) for x in ['P', 'J']]),
               ('type', self.type().lower()),
               ('pointAvailable', self.pointsAvailable)])

def test():
   """Test run with a 4 point likert scale, one question each type.

   Should produce [('I',10),('N',0),('T',0),('P',0)]
   """
   args = {
      'INTP':  2, 'INTJ':  2, 'INFP':  2, 'INFJ':  2,
      'ISTP':  2, 'ISTJ':  2, 'ISFP':  2, 'ISFJ':  2,
      'ENTP': -2, 'ENTJ': -2, 'ENFP': -2, 'ENFJ': -2,
      'ESTP': -2, 'ESTJ': -2, 'ESFP': -2, 'ESFJ': -2,
   }

   an = TypeAnalysis(args, 4)
   print str(an.computedScores)

if __name__== '__main__':
   test()


