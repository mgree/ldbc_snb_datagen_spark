#!/usr/bin/env python3

import calendar
import codecs
import os
import random
import readfactors
import time
from datetime import datetime, timedelta
from timeparameters import *

START_DATE=datetime.strptime("2010-01-01", "%Y-%m-%d")
END_DATE=datetime.strptime("2013-01-01", "%Y-%m-%d")

def format_date(date):
   return int(time.mktime(date.timetuple())*1000)


class ParamsWriter:
   def __init__(self, outdir, number, param_names):
      self.file = codecs.open(outdir+"/bi_"+str(number)+"_param.txt", "w",encoding="utf-8")
      for i in range(0,len(param_names)):
         if i>0:
            self.file.write("|")
         self.file.write(param_names[i])
      self.file.write("\n")

   def append(self, params):
      for i, param in enumerate(params):
         if i>0:
            self.file.write("|")
         self.file.write(param)
      self.file.write("\n")


def post_date_right_open_range_params(sample, lower_bound, upper_bound):
   results = []
   for ix in range(0, len(sample)):
      start_offset = sample[ix][0]
      count_sum = 0
      for offset, count in sample[ix:]:
         count_sum += count
      if count_sum > lower_bound and count_sum < upper_bound:
         results.append([start_offset, count_sum])
   return results

def post_date_range_params(sample, lower_bound, upper_bound):
   results = []
   for ix in range(0, len(sample)):
      start_offset = sample[ix][0]
      count_sum = 0
      for offset, count in sample[ix:]:
         count_sum += count
         if count_sum > lower_bound and count_sum < upper_bound:
            results.append([[start_offset, offset], count_sum])
   return results

def post_month_params(sample, lower_bound, upper_bound):
   results = []
   for ix in range(0, len(sample)//4):
      start_ix = ix*4
      count_sum = 0
      for offset, count in sample[start_ix:start_ix+4]:
         count_sum += count
      if count_sum > lower_bound and count_sum < upper_bound:
         start_day = sample[start_ix][0]
         end_day = sample[start_ix+4][0]
         results.append([[start_day, end_day], count_sum])
   return results

def enumerate_path_bounds(minLength,maxLength,minDifference):
  results = []
  for i in range(minLength, maxLength):
     for j in range(i+minDifference,maxLength):
        results.append([i,j])
  return results

def prob_language_codes():
  results = []
  results.append(["ar"])
  for i in range(0, 2):
     results.append(["tk"])
  for i in range(0, 8):
     results.append(["uz"])
  for i in range(0, 2):
     results.append(["uz","tk"])
  return results

def prob_post_lengths():
  results = [20,40,113,97,240]
  return results

def key_params(sample, lower_bound, upper_bound):
   results = []
   for key, count in sample:
      if count > lower_bound and count < upper_bound:
         results.append([key, count])
   return results

def serialize_q1(outdir, post_weeks):
   writer = ParamsWriter(outdir, 1, ["date"])
   for week, count in post_weeks:
      writer.append([str(week)])

def serialize_q3(outdir, post_months):
   writer = ParamsWriter(outdir, 3, ["year", "month"] )
   for post_month in post_months:
      t = time.gmtime(post_month[0][0]//1000)
      writer.append([str(t.tm_year), str(t.tm_mon)])

def serialize_q4(outdir, tagclasses, countries):
   writer = ParamsWriter(outdir, 4, ["tagClass", "country"])
   for tag, count_a in tagclasses:
      for country, count_b in countries:
         writer.append([tag,country])

def serialize_q5(outdir, countries):
   writer = ParamsWriter(outdir, 5, ["country"])
   for country, count in countries:
      writer.append([country])


def serialize_q6(outdir, tags):
   writer = ParamsWriter(outdir, 6, ["tag"])
   for tag, count in tags:
      writer.append([tag])

def serialize_q7(outdir, tags):
   writer = ParamsWriter(outdir, 7, ["tag"])
   for tag, count in tags:
      writer.append([tag])

def serialize_q8(outdir, tags):
   writer = ParamsWriter(outdir, 8, ["tag"])
   for tag, count in tags:
      writer.append([tag])

def serialize_q10(outdir, tags, post_weeks):
   writer = ParamsWriter(outdir, 10, ["tag", "date"])
   for tag, count in tags:
      for week, count in post_weeks:
         writer.append([tag, str(week)])

def serialize_q14(outdir, creationdates):
   writer = ParamsWriter(outdir, 14, ["startDate", "endDate"])
   for creation, count in creationdates:
      writer.append([str(creation[0]),str(creation[1])])

def serialize_q16(outdir, persons, tagclasses, countries, path_bounds):
   writer = ParamsWriter(outdir, 16, ["person", "country", "tagClass", "minPathDistance", "maxPathDistance"])
   random.seed(1988+2)
   for country, count_b in countries:
      for tagClass, count_a in tagclasses:
         for minDist, maxDist in path_bounds:
            writer.append([str(persons[random.randint(0, len(persons))]), country, tagClass, str(minDist), str(maxDist)])

def serialize_q17(outdir, countries):
   writer = ParamsWriter(outdir, 17, ["country"])
   for country, count in countries:
      writer.append([country])

def serialize_q18(outdir, post_weeks, lengths, languages):
   writer = ParamsWriter(outdir, 18, ["date", "lengthThreshold", "languages"])
   for week, count in post_weeks:
      for length in lengths:
         for language_set in languages:
            writer.append([str(week), str(length), ";".join(language_set)])

def serialize_q21(outdir, countries):
   writer = ParamsWriter(outdir, 21, ["country", "endDate"])
   for country, count in countries:
      writer.append([country,str(format_date(END_DATE))])

def serialize_q22(outdir, countries):
   writer = ParamsWriter(outdir, 22, ["country1", "country2"])
   for ix in range(0,len(countries)):
      country_a, count_a = countries[ix]
      for country_b, count_b in countries[ix+1:]:
         writer.append([country_a, country_b])

def serialize_q25(outdir, persons, post_month_ranges):
   writer = ParamsWriter(outdir, 25, ["person1Id", "person2Id", "startDate", "endDate"])
   for day_range, count_post in post_month_ranges:
      count = min(len(persons), 10)
      for _ in range(0, count):
         person1Id = persons[random.randint(0, len(persons) - 1)]
         while True:
            person2Id = persons[random.randint(0, len(persons) - 1)]
            if person2Id != person1Id:
               writer.append([str(person1Id), str(person2Id), str(day_range[0]), str(day_range[1])])
               break


def add_months(sourcedate,months):
   month = sourcedate.month - 1 + months
   year = int(sourcedate.year + month // 12 )
   month = month % 12 + 1
   day = min(sourcedate.day,calendar.monthrange(year,month)[1])
   return sourcedate.replace(year, month, day)

def convert_posts_histo(histogram):
   week_posts = []
   month = 0
   while (month in histogram):
      monthTotal = histogram[month]
      baseDate=add_months(START_DATE,month)
      week_posts.append([format_date(baseDate), monthTotal//4])
      week_posts.append([format_date(baseDate+timedelta(days=7)), monthTotal//4])
      week_posts.append([format_date(baseDate+timedelta(days=14)), monthTotal//4])
      week_posts.append([format_date(baseDate+timedelta(days=21)), monthTotal//4])
      month = month + 1
   return week_posts

def main(argv=None):
   if argv is None:
      argv = sys.argv

   if len(argv) < 3:
      print("arguments: <input dir> <output dir>")
      return 1

   indir = argv[1]+"/"
   outdir = argv[2]+"/"
   activityFactorFiles=[]
   personFactorFiles=[]
   friendsFiles = []

   for file in os.listdir(indir):
      if file.endswith("activityFactors.txt"):
         activityFactorFiles.append(indir+file)
      if file.endswith("personFactors.txt"):
         personFactorFiles.append(indir+file)
      if file.startswith("m0friendList"):
         friendsFiles.append(indir+file)

   # read precomputed counts from files   
   (personFactors, countryFactors, tagFactors, tagClassFactors, nameFactors, givenNames, ts, postsHisto) = \
      readfactors.load(personFactorFiles,activityFactorFiles, friendsFiles)
   week_posts = convert_posts_histo(postsHisto)

   persons = []
   for key, _ in personFactors.values.items():
      persons.append(key)
   random.seed(1988)
   random.shuffle(persons)

   country_sample = countryFactors
   country_sample.sort(key=lambda x: x[1], reverse=True)

   tagclass_posts = tagClassFactors
   tagclass_posts.sort(key=lambda x: x[1], reverse=True)

   tag_posts = tagFactors
   tag_posts.sort(key=lambda x: x[1], reverse=True)

   total_posts = 0
   for day, count in tag_posts:
      total_posts += count

   person_sum = 0
   for country, count in country_sample:
      person_sum += count

   post_lower_threshold = 0.1*total_posts*0.9
   post_upper_threshold = 0.1*total_posts*1.1
   post_day_ranges = post_date_range_params(week_posts, post_lower_threshold, post_upper_threshold)
   
   #post_lower_threshold = (total_posts/(week_posts[len(week_posts)-1][0]/7/4))*0.8
   #post_upper_threshold = (total_posts/(week_posts[len(week_posts)-1][0]/7/4))*1.2
   non_empty_weeks=len(week_posts)
   for ix in range(0,len(week_posts)):
      if week_posts[ix][1]==0:
         non_empty_weeks-= 1

   post_lower_threshold = (total_posts//(non_empty_weeks//4))*0.8
   post_upper_threshold = (total_posts//(non_empty_weeks//4))*1.2
   post_months = post_month_params(week_posts, post_lower_threshold, post_upper_threshold)

   # the lower bound is inclusive and the upper bound is exclusive
   path_bounds = enumerate_path_bounds(3, 6, 2)
   language_codes = prob_language_codes()
   post_lengths = prob_post_lengths()

   serialize_q3 (outdir, post_months) #new: 2
   serialize_q14(outdir, post_months) #new: 9

   serialize_q1 (outdir,
      post_date_right_open_range_params(week_posts, 0.3*total_posts, 0.6*total_posts))
   serialize_q18(outdir,
      post_date_right_open_range_params(week_posts, 0.3*total_posts, 0.6*total_posts),
      post_lengths,
      language_codes) #new: 12
   serialize_q10(outdir,
      key_params(tag_posts, total_posts//900, total_posts//600),
      post_date_right_open_range_params(week_posts, 0.3*total_posts, 0.6*total_posts)) #new: 8

   serialize_q4 (outdir,
      key_params(tagclass_posts, total_posts//20, total_posts//10),
      key_params(country_sample, total_posts//150, total_posts//50)) #new: 3
   serialize_q5 (outdir,
      key_params(country_sample, total_posts//200, total_posts//100)) #new: 4
   serialize_q6 (outdir,
      key_params(tag_posts, total_posts//1300, total_posts//900)) #new: 5
   serialize_q7 (outdir,
      key_params(tag_posts, total_posts//900, total_posts//600)) #new: 6
   serialize_q8 (outdir,
      key_params(tag_posts, total_posts//600, total_posts//300)) #new: 7
   serialize_q16(outdir,
      persons,
      key_params(tagclass_posts, total_posts//30, total_posts//10),
      key_params(country_sample, total_posts//80, total_posts//20),
      path_bounds) #new: 10
   serialize_q17(outdir,
      key_params(country_sample, total_posts//200, total_posts//100)) #new: 11
   serialize_q21(outdir,
      key_params(country_sample, total_posts//200, total_posts//100)) #new: 13
   serialize_q22(outdir,
      key_params(country_sample, total_posts//120, total_posts//40)) #new: 14
   serialize_q25(outdir,
      persons, post_months) #new: 15


if __name__ == "__main__":
   sys.exit(main())
