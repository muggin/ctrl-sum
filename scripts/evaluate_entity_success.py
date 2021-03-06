#! /usr/bin/env python

# Copyright (c) 2020, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause

import spacy
import argparse

from spacy.lang.en import English

parser = argparse.ArgumentParser(description='evalute entity success rate and hallucination rate')
parser.add_argument('src', type=str, default='test.entitysamplesource', help='source file postfix')
parser.add_argument('summary', type=str, default='', help='summary file')

args = parser.parse_args()

nlp = English()
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)

with open(args.src) as fsrc, \
    open(args.summary) as ftgt:
    total = 0
    success = 0
    total_sent = 0
    halluc_sent = 0
    total_tok = 0
    for lsrc, ltgt in zip(fsrc, ftgt):
        entity = lsrc.strip().split(' => ')[0].strip()
        doc = nlp(ltgt.strip())
        total_tok += len(doc)
        if entity in doc.text:
            success += 1

        for sent in doc.sents:
            if entity not in sent.text:
                halluc_sent += 1
            total_sent += 1

        total += 1

    print({'total example': total, 'success example': success,
        'success rate': success / total, 'total sent': total_sent,
        'avg length': total_tok /total, 'halluc sent': halluc_sent})

