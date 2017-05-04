#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import unicodedata
import unittest

import epitran

logging.basicConfig(level=logging.ERROR)


def map_slice(xs, start, end):
    return [x[start:end] for x in xs]


def assemble_ipa(xs):
    return ''.join([x[3] for x in xs])


class TestTurkish(unittest.TestCase):
    def setUp(self):
        self.epi = epitran.Epitran(u'tur-Latn')

    def test_transliterate1(self):
        self.assertEqual(self.epi.transliterate(u'Haziran\'da'), u'haziɾan\'da')
        self.assertEqual(self.epi.transliterate(u'Hazeran’da'), u'hazeɾan’da')
        self.assertEqual(self.epi.transliterate(u'otoparkın'), u'otopaɾkɯn')

    def test_transliterate2(self):
        self.assertEqual(self.epi.transliterate(u'"'), u'"')
        self.assertEqual(self.epi.transliterate(u'\''), u'\'')
        self.assertEqual(self.epi.transliterate(u'’'), u'’')
        self.assertEqual(self.epi.transliterate(u'‘'), u'‘')

    def test_transliterate_norm_punc1(self):
        self.assertEqual(self.epi.transliterate(u'Haziran\'da', normpunc=True), u'haziɾan\'da')
        self.assertEqual(self.epi.transliterate(u'Hazeran’da', normpunc=True), u'hazeɾan\'da')
        self.assertEqual(self.epi.transliterate(u'otoparkın', normpunc=True), u'otopaɾkɯn')

    def test_transliterate_norm_punc2(self):
        self.assertEqual(self.epi.transliterate(u'"', normpunc=True), u'"')
        self.assertEqual(self.epi.transliterate(u'\'', normpunc=True), u'\'')
        self.assertEqual(self.epi.transliterate(u'’', normpunc=True), u'\'')
        self.assertEqual(self.epi.transliterate(u'‘', normpunc=True), u'\'')

    def test_word_to_tuples1(self):
        target = [(u'L', 1, u'H', u'h'),
                  (u'L', 0, u'a', u'a'),
                  (u'L', 0, u'z', u'z'),
                  (u'L', 0, u'i', u'i'),
                  (u'L', 0, u'r', u'ɾ'),
                  (u'L', 0, u'a', u'a'),
                  (u'L', 0, u'n', u'n'),
                  (u'L', 0, u'ʼ', u''),
                  (u'L', 0, u'd', u'd'),
                  (u'L', 0, u'a', u'a')]
        word = u'Haziranʼda'
        test = map_slice(self.epi.word_to_tuples(word), 0, 4)
        self.assertEqual(test, target)

    def test_word_to_tuples2(self):
        target = [(u'L', 1, u'H', u'h'),
                  (u'L', 0, u'a', u'a'),
                  (u'L', 0, u'z', u'z'),
                  (u'L', 0, u'i', u'i'),
                  (u'L', 0, u'r', u'ɾ'),
                  (u'L', 0, u'a', u'a'),
                  (u'L', 0, u'n', u'n'),
                  (u'P', 0, u"'", u''),
                  (u'L', 0, u'd', u'd'),
                  (u'L', 0, u'a', u'a')]
        word = u'Haziranʼda'
        test = map_slice(self.epi.word_to_tuples(word, normpunc=True), 0, 4)
        self.assertEqual(test, target)


class TestUzbek(unittest.TestCase):
    def setUp(self):
        self.epi = epitran.Epitran(u'uzb-Latn')

    def _derivation(self, orth, correct):
        attempt = assemble_ipa(self.epi.word_to_tuples(orth))
        # logging.debug(u'{} ?= {}'.format(attempt, correct).encode('utf-8'))
        self.assertEqual(attempt, correct)

    def test_uppercase_e_diaeresis(self):
        self._derivation(u'Ë', u'ja')

    def test_ozini1(self):
        # MODIFIER LETTER TURNED COMMA
        target = [(u'L', 0, u'oʻ', u'o'),
                  (u'L', 0, u'z', u'z'),
                  (u'L', 0, u'i', u'i'),
                  (u'L', 0, u'n', u'n'),
                  (u'L', 0, u'i', u'i')
                  ]
        test = self.epi.word_to_tuples(u'oʻzini')
        self.assertEqual(map_slice(test, 0, 4), target)

    def test_ozini2(self):
        target = [(u'L', 0, u"o'", u'o'),
                  (u'L', 0, u'z', u'z'),
                  (u'L', 0, u'i', u'i'),
                  (u'L', 0, u'n', u'n'),
                  (u'L', 0, u'i', u'i'),
                  ]
        test = self.epi.word_to_tuples(u"o'zini", normpunc=True)
        self.assertEqual(map_slice(test, 0, 4), target)

    def test_word_to_tuples2(self):
        target = [(u'L', 1, u'B', u'b'),
                  (u'L', 0, u'a', u'a'),
                  (u'L', 0, u'l', u'l'),
                  (u'L', 0, u'o', u'ɒ'),
                  (u'L', 0, u'gʻ', u'ʁ'),
                  (u'L', 0, u'a', u'a'),
                  (u'L', 0, u't', u't̪')]
        test = self.epi.word_to_tuples(u'Balogʻat')
        self.assertEqual(map_slice(test, 0, 4), target)


class TestDutch(unittest.TestCase):
    def setUp(self):
        self.epi = epitran.Epitran(u'nld-Latn')

    def _derivation(self, orth, correct):
        attempt = assemble_ipa(self.epi.word_to_tuples(orth))
        # logging.debug(u'{} ?= {}'.format(attempt, correct).encode('utf-8'))
        self.assertEqual(attempt, correct)

    def test_bernhard(self):
        self._derivation(u'Bernhard', u'bɛrnhɑrt')

    def test_utrecht(self):
        self._derivation(u'Utrecht', u'ʏtrɛxt')

    def test_lodewijk(self):
        self._derivation(u'Lodewijk', u'loːdeːʋɛjk')

    def test_random(self):
        self._derivation(u'ertogenbosch', u'ɛrtoːɣɛnbɔs')


class TestGerman(unittest.TestCase):
    def setUp(self):
        self.epi = epitran.Epitran(u'deu-Latn')

    def _derivation(self, orth, correct):
        attempt = self.epi.transliterate(orth)
        self.assertEqual(attempt, correct)

    def test_wasser(self):
        self._derivation(u'wasser', u'vasər')

    def test_geben(self):
        self._derivation(u'ɡeben', u'ɡeːbən')

    def test_scheisse(self):
        self._derivation(u'scheiẞe', u'ʃajsə')

    def test_nietzsche(self):
        self._derivation(u'Nietzsche', u'niːt͡ʃə')

    def test_immer(self):
        self._derivation(u'immer', u'imər')

    def test_ahre(self):
        self._derivation(u'Ähre', u'eːrə')

    def test_abdanken(self):
        self._derivation(u'abdanken', u'apdaŋkən')

    def test_rotgelb(self):
        self._derivation(u'rotɡelb', u'rotɡelp')


class TestGermanNP(unittest.TestCase):
    def setUp(self):
        self.epi = epitran.Epitran(u'deu-Latn-np')

    def _derivation(self, orth, correct):
        attempt = assemble_ipa(self.epi.word_to_tuples(orth))
        # logging.debug(u'{} ?= {}'.format(attempt, correct).encode('utf-8'))
        self.assertEqual(attempt, correct)

    def test_wasser(self):
        self._derivation(u'wasser', u'vasər')

    def test_ahre(self):
        self._derivation(u'Ähre', u'eːrə')

    def test_abdanken(self):
        self._derivation(u'abdanken', u'abdaŋkən')

    def test_rotgelb(self):
        self._derivation(u'rotɡelb', u'rotɡelb')


class TestSpanish(unittest.TestCase):
    def setUp(self):
        self.epi = epitran.Epitran(u'spa-Latn')

    def _derivation(self, orth, correct):
        attempt = assemble_ipa(self.epi.word_to_tuples(orth))
        # logging.debug(u'{} ?= {}'.format(attempt, correct).encode('utf-8'))
        self.assertEqual(attempt, correct)

    def test_queso(self):
        self._derivation(u'queso', u'keso')

    def test_general(self):
        self._derivation(u'general', u'xeneɾal')

    def test_cuestion(self):
        self._derivation(u'cuestión', u'kwestjon')

    def test_sabado(self):
        self._derivation(u'sábado', u'sabado')
