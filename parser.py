#!/usr/bin/env python

import re, sys, lxml
from pypeg2 import *
from pypeg2.xmlast import thing2xml

not_a_reserved_word = '(?!(non|le|un|a|ab|ad|adverso|ante|apud|circum|cis|clam|con|concernente|contra|coram|cum|de|depost|desde|detra|dextra|durante|el|erga|ex|excepte|extra|for|foras|foris|in|infra|inter|intra|juxta|malgre|nonobstante|ob|per|por|post|pre|presso|preter|pro|prope|propter|re|salvo|secun|secundo|sin|sub|super|supra|sur|tra|trans|traverso|ultra|usque|verso|via|viste|adeo|amen|ancora|ave|basta|bis|bravo|guai|hallo|holla|miau|out|stop|vale|an|annon|atque|aut|comocunque|donec|dum|dunque|e|et|etsi|igitur|itaque|ma|mais|malgrado|nam|ne|nec|neque|ni|nisi|o|perque|pois|porque|postquam|proque|quam|quando|quandocunque|que|quia|quo|quod|sed|si|sinon|sive|ubi|ubicunque|utrum|vel|eze|oze|ezi|ozi|ezo|ozo|ezu|ozu|ezia|ozia|ezem|ozem|ezim|ozim|ezom|ozom|ezum|ozum|eziam|oziam|ezel|ozel|ezil|ozil|ezol|ozol|ezul|ozul|ezial|ozial|ezet|ozet|ezit|ozit|ezot|ozot|ezut|ozut|eziat|oziat|zero|uni|duo|tres|quatro|cinque|sex|septe|octo|nove|dece|vinti|trenta|quaranta|cinquanta|sexanta|septanta|octanta|novanta|cento|mille|million|milliardo|billion|billiardo|trillion|trilliardo|quatrillion|quatrilliardo|quintillion|quintilliardo|sextillion|sextilliardo|septillion|septilliardo|octillion|octilliardo|nonillion|nonilliardo|decillion|decilliardo|lu|lui|luo|luu|luia|di|plu|comma|ha|es|va|sia|era|qua)(?=\W))'

class Negation(Keyword):
    grammar = Enum(K('non'))

class PastAuxPtcp(Keyword):
    grammar = Enum(K('essita'))

class PresentAuxPtcp(Keyword):
    grammar = Enum(K('essenta'))

class Art(Keyword):
    grammar = Enum(K('le'), K('un'))

class Prep(Keyword):
    grammar = Enum(K('a'), K('ab'), K('ad'), K('adverso'), K('ante'), K('apud'), K('circum'), K('cis'), K('clam'), K('con'), K('concernente'), K('contra'), K('coram'), K('cum'), K('de'), K('depost'), K('desde'), K('detra'), K('dextra'), K('durante'), K('el'), K('erga'), K('ex'), K('excepte'), K('extra'), K('for'), K('foras'), K('foris'), K('in'), K('infra'), K('inter'), K('intra'), K('juxta'), K('malgre'), K('nonobstante'), K('ob'), K('per'), K('por'), K('post'), K('pre'), K('presso'), K('preter'), K('pro'), K('prope'), K('propter'), K('qua'), K('re'), K('salvo'), K('secun'), K('secundo'), K('sin'), K('sub'), K('super'), K('supra'), K('sur'), K('tra'), K('trans'), K('traverso'), K('ultra'), K('usque'), K('verso'), K('via'), K('viste'))

class Interj(Keyword):
    grammar = Enum(K('adeo'), K('amen'), K('ancora'), K('ave'), K('basta'), K('bis'), K('bravo'), K('guai'), K('hallo'), K('holla'), K('miau'), K('out'), K('stop'), K('vale'))

class ConjSent(Keyword):
    grammar = Enum(K('an'), K('annon'), K('atque'), K('aut'), K('comocunque'), K('donec'), K('dum'), K('dunque'), K('e'), K('et'), K('etsi'), K('igitur'), K('itaque'), K('ma'), K('mais'), K('malgrado'), K('nam'), K('ne'), K('nec'), K('neque'), K('ni'), K('nisi'), K('o'), K('perque'), K('pois'), K('porque'), K('postquam'), K('proque'), K('quam'), K('quando'), K('quandocunque'), K('que'), K('quia'), K('quo'), K('quod'), K('sed'), K('si'), K('sinon'), K('sive'), K('ubi'), K('ubicunque'), K('utrum'), K('vel'))

class ConjArg0(Keyword):
    grammar = Enum(K('eze'), K('oze'))

class ConjArg1(Keyword):
    grammar = Enum(K('ezi'), K('ozi'))

class ConjArg2(Keyword):
    grammar = Enum(K('ezo'), K('ozo'))

class ConjArg3(Keyword):
    grammar = Enum(K('ezu'), K('ozu'))

class ConjArg4(Keyword):
    grammar = Enum(K('ezia'), K('ozia'))

class ConjAdv0(Keyword):
    grammar = Enum(K('ezem'), K('ozem'))

class ConjAdv1(Keyword):
    grammar = Enum(K('ezim'), K('ozim'))

class ConjAdv2(Keyword):
    grammar = Enum(K('ezom'), K('ozom'))

class ConjAdv3(Keyword):
    grammar = Enum(K('ezum'), K('ozum'))

class ConjAdv4(Keyword):
    grammar = Enum(K('eziam'), K('oziam'))

class ConjAdj0(Keyword):
    grammar = Enum(K('ezel'), K('ozel'))

class ConjAdj1(Keyword):
    grammar = Enum(K('ezil'), K('ozil'))

class ConjAdj2(Keyword):
    grammar = Enum(K('ezol'), K('ozol'))

class ConjAdj3(Keyword):
    grammar = Enum(K('ezul'), K('ozul'))

class ConjAdj4(Keyword):
    grammar = Enum(K('ezial'), K('ozial'))

class ConjPtcp0(Keyword):
    grammar = Enum(K('ezet'), K('ozet'))

class ConjPtcp1(Keyword):
    grammar = Enum(K('ezit'), K('ozit'))

class ConjPtcp2(Keyword):
    grammar = Enum(K('ezot'), K('ozot'))

class ConjPtcp3(Keyword):
    grammar = Enum(K('ezut'), K('ozut'))

class ConjPtcp4(Keyword):
    grammar = Enum(K('eziat'), K('oziat'))

class Num0(Keyword):
    grammar = Enum(K('zero'))

class N_1_9(Keyword):
    grammar = Enum(K('uni'), K('duo'), K('tres'), K('quatro'), K('cinque'), K('sex'), K('septe'), K('octo'), K('nove'))

class N_1_9_ord(Keyword):
    grammar = Enum(K('prime'), K('secunde'), K('tertie'), K('quarte'), K('quinte'), K('sexte'), K('septime'), K('octave'), K('none'))

class N_10_90(Keyword):
    grammar = Enum(K('dece'), K('vinti'), K('trenta'), K('quaranta'), K('cinquanta'), K('sexanta'), K('septanta'), K('octanta'), K('novanta'))

class N_10_90_ord(Keyword):
    grammar = Enum(K('decime'), K('vintesime'), K('trentesime'), K('quarantesime'), K('cinquantesime'), K('sexantesime'), K('septantesime'), K('octantesime'), K('novantesime'))

class Num100(Keyword):
    grammar = Enum(K('cento'))

class Num100_ord(Keyword):
    grammar = Enum(K('centesime'))

class Num1e3(Keyword):
    grammar = Enum(K('mille'))

class Num1e3_ord(Keyword):
    grammar = Enum(K('millesime'))

class Num1e6(Keyword):
    grammar = Enum(K('million'))

class Num1e6_ord(Keyword):
    grammar = Enum(K('millionesime'))

class Num1e9(Keyword):
    grammar = Enum(K('milliardo'))

class Num1e9_ord(Keyword):
    grammar = Enum(K('milliardesime'))

class Num1e12(Keyword):
    grammar = Enum(K('billion'))

class Num1e12_ord(Keyword):
    grammar = Enum(K('billionesime'))

class Num1e15(Keyword):
    grammar = Enum(K('billiardo'))

class Num1e15_ord(Keyword):
    grammar = Enum(K('billiardesime'))

class Num1e18(Keyword):
    grammar = Enum(K('trillion'))

class Num1e18_ord(Keyword):
    grammar = Enum(K('trillionesime'))

class Num1e21(Keyword):
    grammar = Enum(K('trilliardo'))

class Num1e21_ord(Keyword):
    grammar = Enum(K('trilliardesime'))

class Num1e24(Keyword):
    grammar = Enum(K('quatrillion'))

class Num1e24_ord(Keyword):
    grammar = Enum(K('quatrillionesime'))

class Num1e27(Keyword):
    grammar = Enum(K('quatrilliardo'))

class Num1e27_ord(Keyword):
    grammar = Enum(K('quatrilliardesime'))

class Num1e30(Keyword):
    grammar = Enum(K('quintillion'))

class Num1e30_ord(Keyword):
    grammar = Enum(K('quintillionesime'))

class Num1e33(Keyword):
    grammar = Enum(K('quintilliardo'))

class Num1e33_ord(Keyword):
    grammar = Enum(K('quintilliardesime'))

class Num1e36(Keyword):
    grammar = Enum(K('sextillion'))

class Num1e36_ord(Keyword):
    grammar = Enum(K('sextillionesime'))

class Num1e39(Keyword):
    grammar = Enum(K('sextilliardo'))

class Num1e39_ord(Keyword):
    grammar = Enum(K('sextilliardesime'))

class Num1e42(Keyword):
    grammar = Enum(K('septillion'))

class Num1e42_ord(Keyword):
    grammar = Enum(K('septillionesime'))

class Num1e45(Keyword):
    grammar = Enum(K('septilliardo'))

class Num1e45_ord(Keyword):
    grammar = Enum(K('septilliardesime'))

class Num1e48(Keyword):
    grammar = Enum(K('octillion'))

class Num1e48_ord(Keyword):
    grammar = Enum(K('octillionesime'))

class Num1e51(Keyword):
    grammar = Enum(K('octilliardo'))

class Num1e51_ord(Keyword):
    grammar = Enum(K('octilliardesime'))

class Num1e54(Keyword):
    grammar = Enum(K('nonillion'))

class Num1e54_ord(Keyword):
    grammar = Enum(K('nonillionesime'))

class Num1e57(Keyword):
    grammar = Enum(K('nonilliardo'))

class Num1e57_ord(Keyword):
    grammar = Enum(K('nonilliardesime'))

class Num1e60(Keyword):
    grammar = Enum(K('decillion'))

class Num1e60_ord(Keyword):
    grammar = Enum(K('decillionesime'))

class Num1e63(Keyword):
    grammar = Enum(K('decilliardo'))

class Num1e63_ord(Keyword):
    grammar = Enum(K('decilliardesime'))

class NumDiv(Keyword):
    grammar = Enum(K('di'))

class NumPlus(Keyword):
    grammar = Enum(K('plu'))

class NumPoint(Keyword):
    grammar = Enum(K('comma'))

class V(str):
    grammar = re.compile('(ha|es|va|sia)(?=\W)|' + not_a_reserved_word + '\w+(a|e|i)(t|va|ra|rea|n)(?=\W)')

class N0(str):
    grammar = re.compile(not_a_reserved_word + '\w+e(|s)(?=\W)')

class N1(str):
    grammar = re.compile(not_a_reserved_word + '\w+i(|s)(?=\W)')

class N2(str):
    grammar = re.compile(not_a_reserved_word + '\w+o(|s)(?=\W)')

class N3(str):
    grammar = re.compile(not_a_reserved_word + '\w+u(|s)(?=\W)')

class N4(str):
    grammar = re.compile(not_a_reserved_word + '\w+ia(|s)(?=\W)')

class Inf0(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|e|i)r(?=\W)')

class Inf1(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|e|i)vur(?=\W)')

class Inf2(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|e|i)dur(?=\W)')

class Inf3(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|e|i)jur(?=\W)')

class Inf4(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|e|i)gur(?=\W)')

class App0(str):
    grammar = re.compile(not_a_reserved_word + '\w+ef(|s)(?=\W)')

class App1(str):
    grammar = re.compile(not_a_reserved_word + '\w+if(|s)(?=\W)')

class App2(str):
    grammar = re.compile(not_a_reserved_word + '\w+of(|s)(?=\W)')

class App3(str):
    grammar = re.compile(not_a_reserved_word + '\w+uf(|s)(?=\W)')

class App4(str):
    grammar = re.compile(not_a_reserved_word + '\w+iaf(|s)(?=\W)')

class Adj0(str):
    grammar = re.compile(not_a_reserved_word + '\w+el(?=\W)')

class Adj1(str):
    grammar = re.compile(not_a_reserved_word + '\w+il(?=\W)')

class Adj2(str):
    grammar = re.compile(not_a_reserved_word + '\w+ol(?=\W)')

class Adj3(str):
    grammar = re.compile(not_a_reserved_word + '\w+ul(?=\W)')

class Adj4(str):
    grammar = re.compile(not_a_reserved_word + '\w+ial(?=\W)')

class Adv0(str):
    grammar = re.compile(not_a_reserved_word + '\w+em(?=\W)')

class Adv1(str):
    grammar = re.compile(not_a_reserved_word + '\w+im(?=\W)')

class Adv2(str):
    grammar = re.compile(not_a_reserved_word + '\w+om(?=\W)')

class Adv3(str):
    grammar = re.compile(not_a_reserved_word + '\w+um(?=\W)')

class Adv4(str):
    grammar = re.compile(not_a_reserved_word + '\w+iam(?=\W)')

class PtcpPres0(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|e|ie)nta(?=\W)')

class PtcpPres1(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|e|ie)vunta(?=\W)')

class PtcpPres2(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|e|ie)dunta(?=\W)')

class PtcpPres3(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|e|ie)junta(?=\W)')

class PtcpPres4(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|e|ie)gunta(?=\W)')

class PtcpPast0(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|i)ta(?=\W)')

class PtcpPast1(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|i)vuta(?=\W)')

class PtcpPast2(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|i)duta(?=\W)')

class PtcpPast3(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|i)juta(?=\W)')

class PtcpPast4(str):
    grammar = re.compile(not_a_reserved_word + '\w+(a|i)guta(?=\W)')

class N_0_9(List):
    grammar = [Num0, N_1_9]

class N_1_999(List):
    grammar = [
        (N_1_9, Num100, N_10_90, optional(N_1_9)),
        (N_1_9, Num100, optional(N_1_9)),
        (N_10_90, optional(N_1_9)),
        N_1_9
    ]

class N_1_999_ord(List):
    grammar = [
        (N_1_9, Num100, N_10_90, N_1_9_ord),
        (N_1_9, Num100, N_10_90_ord),
        (N_1_9, Num100, N_1_9_ord),
        (N_1_9, Num100_ord),
        (N_10_90, N_1_9_ord),
        (N_10_90_ord),
        N_1_9_ord
    ]

class N_0_999(List):
    grammar = [Num0, N_1_999]

class N1e3(List):
    grammar = N_1_999, Num1e3, optional(N_1_999)

class N1e3_ord(List):
    grammar = [
        (N_1_999, Num1e3_ord),
        (N_1_999, Num1e3, N_1_999_ord)
    ]

class N1e6(List):
    grammar = N_1_999, Num1e6, [
        N1e3,
        optional(N_1_999)
    ]

class N1e6_ord(List):
    grammar = [(N_1_999, Num1e6, [
        N1e3_ord,
        N_1_999_ord
    ]), (N_1_999, Num1e6_ord)]

class N1e9(List):
    grammar = N_1_999, Num1e9, [
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e9_ord(List):
    grammar = [(N_1_999, Num1e9, [
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e9_ord)]

class N1e12(List):
    grammar = N_1_999, Num1e12, [
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e12_ord(List):
    grammar = [(N_1_999, Num1e12, [
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e12_ord)]

class N1e15(List):
    grammar = N_1_999, Num1e15, [
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e15_ord(List):
    grammar = [(N_1_999, Num1e15, [
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e15_ord)]

class N1e18(List):
    grammar = N_1_999, Num1e18, [
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e18_ord(List):
    grammar = [(N_1_999, Num1e18, [
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e18_ord)]

class N1e21(List):
    grammar = N_1_999, Num1e21, [
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e21_ord(List):
    grammar = [(N_1_999, Num1e21, [
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e21_ord)]

class N1e24(List):
    grammar = N_1_999, Num1e24, [
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e24_ord(List):
    grammar = [(N_1_999, Num1e24, [
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e24_ord)]

class N1e27(List):
    grammar = N_1_999, Num1e27, [
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e27_ord(List):
    grammar = [(N_1_999, Num1e27, [
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e27_ord)]

class N1e30(List):
    grammar = N_1_999, Num1e30, [
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e30_ord(List):
    grammar = [(N_1_999, Num1e30, [
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e30_ord)]

class N1e33(List):
    grammar = N_1_999, Num1e33, [
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e33_ord(List):
    grammar = [(N_1_999, Num1e33, [
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e33_ord)]

class N1e36(List):
    grammar = N_1_999, Num1e36, [
        N1e33,
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e36_ord(List):
    grammar = [(N_1_999, Num1e36, [
        N1e33_ord,
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e36_ord)]

class N1e39(List):
    grammar = N_1_999, Num1e39, [
        N1e36,
        N1e33,
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e39_ord(List):
    grammar = [(N_1_999, Num1e39, [
        N1e36_ord,
        N1e33_ord,
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e39_ord)]

class N1e42(List):
    grammar = N_1_999, Num1e42, [
        N1e39,
        N1e36,
        N1e33,
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e42_ord(List):
    grammar = [(N_1_999, Num1e42, [
        N1e39_ord,
        N1e36_ord,
        N1e33_ord,
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e42_ord)]

class N1e45(List):
    grammar = N_1_999, Num1e45, [
        N1e42,
        N1e39,
        N1e36,
        N1e33,
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e45_ord(List):
    grammar = [(N_1_999, Num1e45, [
        N1e42_ord,
        N1e39_ord,
        N1e36_ord,
        N1e33_ord,
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e45_ord)]

class N1e48(List):
    grammar = N_1_999, Num1e48, [
        N1e45,
        N1e42,
        N1e39,
        N1e36,
        N1e33,
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e48_ord(List):
    grammar = [(N_1_999, Num1e48, [
        N1e45_ord,
        N1e42_ord,
        N1e39_ord,
        N1e36_ord,
        N1e33_ord,
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e48_ord)]

class N1e51(List):
    grammar = N_1_999, Num1e51, [
        N1e48,
        N1e45,
        N1e42,
        N1e39,
        N1e36,
        N1e33,
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e51_ord(List):
    grammar = [(N_1_999, Num1e51, [
        N1e48_ord,
        N1e45_ord,
        N1e42_ord,
        N1e39_ord,
        N1e36_ord,
        N1e33_ord,
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e51_ord)]

class N1e54(List):
    grammar = N_1_999, Num1e54, [
        N1e51,
        N1e48,
        N1e45,
        N1e42,
        N1e39,
        N1e36,
        N1e33,
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e54_ord(List):
    grammar = [(N_1_999, Num1e54, [
        N1e51_ord,
        N1e48_ord,
        N1e45_ord,
        N1e42_ord,
        N1e39_ord,
        N1e36_ord,
        N1e33_ord,
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e54_ord)]

class N1e57(List):
    grammar = N_1_999, Num1e57, [
        N1e54,
        N1e51,
        N1e48,
        N1e45,
        N1e42,
        N1e39,
        N1e36,
        N1e33,
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e57_ord(List):
    grammar = [(N_1_999, Num1e57, [
        N1e54_ord,
        N1e51_ord,
        N1e48_ord,
        N1e45_ord,
        N1e42_ord,
        N1e39_ord,
        N1e36_ord,
        N1e33_ord,
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e57_ord)]

class N1e60(List):
    grammar = N_1_999, Num1e60, [
        N1e57,
        N1e54,
        N1e51,
        N1e48,
        N1e45,
        N1e42,
        N1e39,
        N1e36,
        N1e33,
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e60_ord(List):
    grammar = [(N_1_999, Num1e60, [
        N1e57_ord,
        N1e54_ord,
        N1e51_ord,
        N1e48_ord,
        N1e45_ord,
        N1e42_ord,
        N1e39_ord,
        N1e36_ord,
        N1e33_ord,
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e60_ord) ]

class N1e63(List):
    grammar = N_1_999, Num1e63, [
        N1e60,
        N1e57,
        N1e54,
        N1e51,
        N1e48,
        N1e45,
        N1e42,
        N1e39,
        N1e36,
        N1e33,
        N1e30,
        N1e27,
        N1e24,
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_1_999),
    ]

class N1e63_ord(List):
    grammar = [(N_1_999, Num1e63, [
        N1e60_ord,
        N1e57_ord,
        N1e54_ord,
        N1e51_ord,
        N1e48_ord,
        N1e45_ord,
        N1e42_ord,
        N1e39_ord,
        N1e36_ord,
        N1e33_ord,
        N1e30_ord,
        N1e27_ord,
        N1e24_ord,
        N1e21_ord,
        N1e18_ord,
        N1e15_ord,
        N1e12_ord,
        N1e9_ord,
        N1e6_ord,
        N1e3_ord,
        N_1_999_ord,
    ]), (N_1_999, Num1e63_ord)]

class Natural(List):
    grammar = [N1e63, N1e60, N1e57, N1e54, N1e51, N1e48, N1e45, N1e42, N1e39, N1e36, N1e33, N1e30, N1e27, N1e24, N1e21, N1e18, N1e15, N1e12, N1e9, N1e6, N1e3, N_0_999]

class Decimal(List):
    grammar = Natural, NumPoint, some(N_0_9)

class Fractional(List):
    grammar = [
        (Natural, NumPlus, Natural, NumDiv, Natural),
        (Natural, NumDiv, Natural)
    ]

class CardinalNumeral(List):
    grammar = [Fractional, Decimal, Natural]

class OrdinalNumeral(List):
    grammar = [N1e63_ord, N1e60_ord, N1e57_ord, N1e54_ord, N1e51_ord, N1e48_ord, N1e45_ord, N1e42_ord, N1e39_ord, N1e36_ord, N1e33_ord, N1e30_ord, N1e27_ord, N1e24_ord, N1e21_ord, N1e18_ord, N1e15_ord, N1e12_ord, N1e9_ord, N1e6_ord, N1e3_ord, N_1_999_ord]

class AdjP4(List):
    grammar = optional(Negation), Adj4, maybe_some(optional(ConjAdj4), Adj4)

class PtcpP4(List):
    grammar = optional(Negation), [
        (PresentAuxPtcp, PtcpPast4),
        (PastAuxPtcp, PtcpPast4),
        PtcpPres4,
        PtcpPast4
    ], maybe_some(optional(ConjPtcp4), optional(Negation), [
        (PresentAuxPtcp, PtcpPast4),
        (PastAuxPtcp, PtcpPast4),
        PtcpPres4,
        PtcpPast4
    ])

class AppP4(List):
    grammar = optional([Negation, Art, CardinalNumeral]), App4, optional(OrdinalNumeral), maybe_some(AdjP4), maybe_some(PtcpP4)

class NP4(List):
    grammar = optional([Negation, Art, CardinalNumeral]), N4, optional(OrdinalNumeral), maybe_some(AdjP4), maybe_some(PtcpP4), maybe_some(AppP4)

class InfP4(List):
    grammar = optional(Negation), Inf4

class Arg4(List):
    grammar = [NP4, InfP4], maybe_some(ConjArg4, [NP4, InfP4])

class AdvP4(List):
    grammar = optional(Negation), [Adv4, (Prep, Arg4)], maybe_some(ConjAdv4, optional(Negation), [Adv4, (Prep, Arg4)])

class AdjP3(List):
    grammar = optional(Negation), Adj3, optional(AdvP4), maybe_some(optional(ConjAdj3), Adj3, optional(AdvP4))

class PtcpP3(List):
    grammar = optional(Negation), [
        (PresentAuxPtcp, PtcpPast3),
        (PastAuxPtcp, PtcpPast3),
        PtcpPres3,
        PtcpPast3
    ], optional(Arg4), optional(AdvP4), maybe_some(optional(ConjPtcp3), optional(Negation), [
        (PresentAuxPtcp, PtcpPast3),
        (PastAuxPtcp, PtcpPast3),
        PtcpPres3,
        PtcpPast3
    ], optional(Arg4), optional(AdvP4))

class AppP3(List):
    grammar = optional([Negation, Art, CardinalNumeral]), App3, optional(OrdinalNumeral), maybe_some(AdvP4), maybe_some(AdjP3), maybe_some(PtcpP3)

class NP3(List):
    grammar = optional([Negation, Art, CardinalNumeral]), N3, optional(OrdinalNumeral), maybe_some(AdvP4), maybe_some(AdjP3), maybe_some(PtcpP3), maybe_some(AppP3)

class InfP3(List):
    grammar = optional(Negation), Inf3, optional(Arg4), maybe_some(AdvP4)

class Arg3(List):
    grammar = [NP3, InfP3], maybe_some(ConjArg3, [NP3, InfP3])

class AdvP3(List):
    grammar = optional(Negation), [Adv3, (Prep, Arg3)], optional(AdvP4), maybe_some(ConjAdv3, optional(Negation), [Adv3, (Prep, Arg3)], optional(AdvP4))

class AdjP2(List):
    grammar = optional(Negation), Adj2, optional(AdvP3), maybe_some(optional(ConjAdj2), Adj2, optional(AdvP3))

class PtcpP2(List):
    grammar = optional(Negation), [
        (PresentAuxPtcp, PtcpPast2),
        (PastAuxPtcp, PtcpPast2),
        PtcpPres2,
        PtcpPast2
    ], optional(Arg3), optional(AdvP3), maybe_some(optional(ConjPtcp2), optional(Negation), [
        (PresentAuxPtcp, PtcpPast2),
        (PastAuxPtcp, PtcpPast2),
        PtcpPres2,
        PtcpPast2
    ], optional(Arg3), optional(AdvP3))

class AppP2(List):
    grammar = optional([Negation, Art, CardinalNumeral]), App2, optional(OrdinalNumeral), maybe_some(AdvP3), maybe_some(AdjP2), maybe_some(PtcpP2)

class NP2(List):
    grammar = optional([Negation, Art, CardinalNumeral]), N2, optional(OrdinalNumeral), maybe_some(AdvP3), maybe_some(AdjP2), maybe_some(PtcpP2), maybe_some(AppP2)

class InfP2(List):
    grammar = optional(Negation), Inf2, optional(Arg3), maybe_some(AdvP3)

class Arg2(List):
    grammar = [NP2, InfP2], maybe_some(ConjArg2, [NP2, InfP2])

class AdvP2(List):
    grammar = optional(Negation), [Adv2, (Prep, Arg2)], optional(AdvP3), maybe_some(ConjAdv2, optional(Negation), [Adv2, (Prep, Arg2)], optional(AdvP3))

class AdjP1(List):
    grammar = optional(Negation), Adj1, optional(AdvP2), maybe_some(optional(ConjAdj1), Adj1, optional(AdvP2))

class PtcpP1(List):
    grammar = optional(Negation), [
        (PresentAuxPtcp, PtcpPast1),
        (PastAuxPtcp, PtcpPast1),
        PtcpPres1,
        PtcpPast1
    ], optional(Arg2), optional(AdvP2), maybe_some(optional(ConjPtcp1), optional(Negation), [
        (PresentAuxPtcp, PtcpPast1),
        (PastAuxPtcp, PtcpPast1),
        PtcpPres1,
        PtcpPast1
    ], optional(Arg2), optional(AdvP2))

class AppP1(List):
    grammar = optional([Negation, Art, CardinalNumeral]), App1, optional(OrdinalNumeral), maybe_some(AdvP2), maybe_some(AdjP1), maybe_some(PtcpP1)

class NP1(List):
    grammar = optional([Negation, Art, CardinalNumeral]), N1, optional(OrdinalNumeral), maybe_some(AdvP2), maybe_some(AdjP1), maybe_some(PtcpP1), maybe_some(AppP1)

class InfP1(List):
    grammar = optional(Negation), Inf1, optional(Arg2), maybe_some(AdvP2)

class Arg1(List):
    grammar = [NP1, InfP1], maybe_some(ConjArg1, [NP1, InfP1])

class AdvP1(List):
    grammar = optional(Negation), [Adv1, (Prep, Arg1)], optional(AdvP2), maybe_some(ConjAdv1, optional(Negation), [Adv1, (Prep, Arg1)], optional(AdvP2))

class AdjP0(List):
    grammar = optional(Negation), Adj0, optional(AdvP1), maybe_some(optional(ConjAdj0), Adj0, optional(AdvP1))

class PtcpP0(List):
    grammar = optional(Negation), [
        (PresentAuxPtcp, PtcpPast0),
        (PastAuxPtcp, PtcpPast0),
        PtcpPres0,
        PtcpPast0
    ], optional(Arg1), optional(AdvP1), maybe_some(optional(ConjPtcp0), optional(Negation), [
        (PresentAuxPtcp, PtcpPast0),
        (PastAuxPtcp, PtcpPast0),
        PtcpPres0,
        PtcpPast0
    ], optional(Arg1), optional(AdvP1))

class AppP0(List):
    grammar = optional([Negation, Art, CardinalNumeral]), App0, optional(OrdinalNumeral), maybe_some(AdvP1), maybe_some(AdjP0), maybe_some(PtcpP0)

class NP0(List):
    grammar = optional([Negation, Art, CardinalNumeral]), N0, optional(OrdinalNumeral), maybe_some(AdvP1), maybe_some(AdjP0), maybe_some(PtcpP0), maybe_some(AppP0)

class InfP0(List):
    grammar = optional(Negation), Inf0, optional(Arg1), maybe_some(AdvP1)

class Arg0(List):
    grammar = [NP0, InfP0], maybe_some(ConjArg0, [NP0, InfP0])

class AdvP0(List):
    grammar = optional(Negation), [Adv0, (Prep, Arg0)], optional(AdvP1), maybe_some(ConjAdv0, optional(Negation), [Adv0, (Prep, Arg0)], optional(AdvP1))

class PresentPerfectAuxV(Keyword):
    grammar = Enum(K('habet'), K('ha'))

class PastPerfectAuxV(Keyword):
    grammar = Enum(K('habeva'))

class FuturePerfectAuxV(Keyword):
    grammar = Enum(K('habera'))

class ConditionalPerfectAuxV(Keyword):
    grammar = Enum(K('haberea'))

class ImperativePassiveAuxV(Keyword):
    grammar = Enum(K('essen'), K('sia'))

class PresentPassiveAuxV(Keyword):
    grammar = Enum(K('esset'), K('es'))

class PastPassiveAuxV(Keyword):
    grammar = Enum(K('esseva'), K('era'))

class FuturePassiveAuxV(Keyword):
    grammar = Enum(K('essera'))

class ConditionalPassiveAuxV(Keyword):
    grammar = Enum(K('esserea'))

class VP(List):
    grammar = optional(Negation), [
        (PresentPerfectAuxV,     PastAuxPtcp, PtcpPast0), # present perfect passive
        (PastPerfectAuxV,        PastAuxPtcp, PtcpPast0), # past perfect passive
        (FuturePerfectAuxV,      PastAuxPtcp, PtcpPast0), # future perfect passive
        (ConditionalPerfectAuxV, PastAuxPtcp, PtcpPast0), # conditional perfect passive
        (ImperativePassiveAuxV,  PtcpPast0), # imperative passive
        (PresentPassiveAuxV,     PtcpPast0), # present passive
        (PastPassiveAuxV,        PtcpPast0), # past passive
        (FuturePassiveAuxV,      PtcpPast0), # future passive
        (ConditionalPassiveAuxV, PtcpPast0), # conditional passive
        (PresentPerfectAuxV,     PtcpPast0), # present perfect
        (PastPerfectAuxV,        PtcpPast0), # past perfect
        (FuturePerfectAuxV,      PtcpPast0), # future perfect
        (ConditionalPerfectAuxV, PtcpPast0), # conditional perfect
        V # simple tenses
    ]

class Sentence(List):
    grammar = [
        (optional(AdvP0), Arg0, optional(AdvP0), VP,   optional(AdvP0), Arg0, optional(AdvP0)), # SVO
        (optional(AdvP0), VP,   optional(AdvP0), Arg0, optional(AdvP0), Arg0, optional(AdvP0)), # VSO
        (optional(AdvP0), Arg0, optional(AdvP0), Arg0, optional(AdvP0), VP,   optional(AdvP0)), # SOV
        (optional(AdvP0), Arg0, optional(AdvP0), VP,   optional(AdvP0)), # SV
        (optional(AdvP0), VP,   optional(AdvP0), Arg0, optional(AdvP0)), # VS
        (optional(AdvP0), VP,   optional(AdvP0)), # V
        Arg0, # S
        Interj
    ]

class Text(List):
    grammar = optional(ConjSent), Sentence, maybe_some(ConjSent, Sentence)

if __name__ == '__main__':
    sys.stdin.reconfigure(encoding='utf-8')
    p = Parser()
    r = sys.stdin.read()
    f, s = p.parse(r, Text)
    print(thing2xml(s, pretty=True).decode())
    if f != '':
        print('ERROR! The text does not comply with grammar starting at:', f)

