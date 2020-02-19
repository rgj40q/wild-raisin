#!/usr/bin/env python

import re, sys, lxml
from pypeg2 import *
from pypeg2.xmlast import thing2xml

not_a_reserved_word = '(?!(non|le|un|a|ab|ad|adverso|ante|apud|circum|cis|clam|con|concernente|contra|coram|cum|de|depost|desde|detra|dextra|durante|el|erga|ex|excepte|extra|for|foras|foris|in|infra|inter|intra|juxta|malgre|nonobstante|ob|per|por|post|pre|presso|preter|pro|prope|propter|re|salvo|secun|secundo|sin|sub|super|supra|sur|tra|trans|traverso|ultra|usque|verso|via|viste|adeo|amen|ancora|ave|basta|bis|bravo|guai|hallo|holla|miau|out|stop|vale|an|annon|atque|aut|comocunque|donec|dum|dunque|e|et|etsi|igitur|itaque|ma|mais|malgrado|nam|ne|nec|neque|ni|nisi|o|perque|pois|porque|postquam|proque|quam|quando|quandocunque|que|quia|quo|quod|sed|si|sinon|sive|ubi|ubicunque|utrum|vel|ega|eba|iga|iba|oga|oba|uga|uba|iaga|aiba|emga|emba|imga|imba|omga|omba|umga|umba|iamga|iamba|elga|elba|ilga|ilba|olga|olba|ulga|ulba|ialga|ialba|etga|etba|itga|itba|otga|otba|udga|utba|iatga|iatba|zero|uni|duo|tres|quatro|cinque|sex|septe|octo|nove|dece|vinti|trenta|quaranta|cinquanta|sexanta|septanta|octanta|novanta|cento|mille|million|milliardo|billion|billiardo|trillion|trilliardo|quatrillion|quatrilliardo|quintillion|quintilliardo|sextillion|sextilliardo|septillion|septilliardo|octillion|octilliardo|nonillion|nonilliardo|decillion|decilliardo|lu|lui|luo|luu|luia|di|plus|comma|ha|es|va|sia|era)(?=\W))'

class Negation(Keyword):
    grammar = Enum(K('non'))

class PastAuxPtcp(Keyword):
    grammar = Enum(K('essita'))

class PresentAuxPtcp(Keyword):
    grammar = Enum(K('essenta'))

class Art(Keyword):
    grammar = Enum(K('le'), K('un'))

class Prep(Keyword):
    grammar = Enum(K('a'), K('ab'), K('ad'), K('adverso'), K('ante'), K('apud'), K('circum'), K('cis'), K('clam'), K('con'), K('concernente'), K('contra'), K('coram'), K('cum'), K('de'), K('depost'), K('desde'), K('detra'), K('dextra'), K('durante'), K('el'), K('erga'), K('ex'), K('excepte'), K('extra'), K('for'), K('foras'), K('foris'), K('in'), K('infra'), K('inter'), K('intra'), K('juxta'), K('malgre'), K('nonobstante'), K('ob'), K('per'), K('por'), K('post'), K('pre'), K('presso'), K('preter'), K('pro'), K('prope'), K('propter'), K('re'), K('salvo'), K('secun'), K('secundo'), K('sin'), K('sub'), K('super'), K('supra'), K('sur'), K('tra'), K('trans'), K('traverso'), K('ultra'), K('usque'), K('verso'), K('via'), K('viste'))

class Interj(Keyword):
    grammar = Enum(K('adeo'), K('amen'), K('ancora'), K('ave'), K('basta'), K('bis'), K('bravo'), K('guai'), K('hallo'), K('holla'), K('miau'), K('out'), K('stop'), K('vale'))

class ConjSent(Keyword):
    grammar = Enum(K('an'), K('annon'), K('atque'), K('aut'), K('comocunque'), K('donec'), K('dum'), K('dunque'), K('e'), K('et'), K('etsi'), K('igitur'), K('itaque'), K('ma'), K('mais'), K('malgrado'), K('nam'), K('ne'), K('nec'), K('neque'), K('ni'), K('nisi'), K('o'), K('perque'), K('pois'), K('porque'), K('postquam'), K('proque'), K('quam'), K('quando'), K('quandocunque'), K('que'), K('quia'), K('quo'), K('quod'), K('sed'), K('si'), K('sinon'), K('sive'), K('ubi'), K('ubicunque'), K('utrum'), K('vel'))

class ConjArg0(Keyword):
    grammar = Enum(K('ega'), K('eba'))

class ConjArg1(Keyword):
    grammar = Enum(K('iga'), K('iba'))

class ConjArg2(Keyword):
    grammar = Enum(K('oga'), K('oba'))

class ConjArg3(Keyword):
    grammar = Enum(K('uga'), K('uba'))

class ConjArg4(Keyword):
    grammar = Enum(K('iaga'), K('aiba'))

class ConjAdv0(Keyword):
    grammar = Enum(K('emga'), K('emba'))

class ConjAdv1(Keyword):
    grammar = Enum(K('imga'), K('imba'))

class ConjAdv2(Keyword):
    grammar = Enum(K('omga'), K('omba'))

class ConjAdv3(Keyword):
    grammar = Enum(K('umga'), K('umba'))

class ConjAdv4(Keyword):
    grammar = Enum(K('aimga'), K('iamba'))

class ConjAdj0(Keyword):
    grammar = Enum(K('elga'), K('elba'))

class ConjAdj1(Keyword):
    grammar = Enum(K('ilga'), K('ilba'))

class ConjAdj2(Keyword):
    grammar = Enum(K('olga'), K('olba'))

class ConjAdj3(Keyword):
    grammar = Enum(K('ulga'), K('ulba'))

class ConjAdj4(Keyword):
    grammar = Enum(K('ialga'), K('ialba'))

class ConjPtcp0(Keyword):
    grammar = Enum(K('etga'), K('etba'))

class ConjPtcp1(Keyword):
    grammar = Enum(K('itga'), K('itba'))

class ConjPtcp2(Keyword):
    grammar = Enum(K('otga'), K('otba'))

class ConjPtcp3(Keyword):
    grammar = Enum(K('udga'), K('utba'))

class ConjPtcp4(Keyword):
    grammar = Enum(K('iatga'), K('iatba'))

class Num0(Keyword):
    grammar = Enum(K('zero'))

class N_1_9(Keyword):
    grammar = Enum(K('uni'), K('duo'), K('tres'), K('quatro'), K('cinque'), K('sex'), K('septe'), K('octo'), K('nove'))

class N_10_90(Keyword):
    grammar = Enum(K('dece'), K('vinti'), K('trenta'), K('quaranta'), K('cinquanta'), K('sexanta'), K('septanta'), K('octanta'), K('novanta'))

class Num100(Keyword):
    grammar = Enum(K('cento'))

class Num1e3(Keyword):
    grammar = Enum(K('mille'))

class Num1e6(Keyword):
    grammar = Enum(K('million'))

class Num1e9(Keyword):
    grammar = Enum(K('milliardo'))

class Num1e12(Keyword):
    grammar = Enum(K('billion'))

class Num1e15(Keyword):
    grammar = Enum(K('billiardo'))

class Num1e18(Keyword):
    grammar = Enum(K('trillion'))

class Num1e21(Keyword):
    grammar = Enum(K('trilliardo'))

class Num1e24(Keyword):
    grammar = Enum(K('quatrillion'))

class Num1e27(Keyword):
    grammar = Enum(K('quatrilliardo'))

class Num1e30(Keyword):
    grammar = Enum(K('quintillion'))

class Num1e33(Keyword):
    grammar = Enum(K('quintilliardo'))

class Num1e36(Keyword):
    grammar = Enum(K('sextillion'))

class Num1e39(Keyword):
    grammar = Enum(K('sextilliardo'))

class Num1e42(Keyword):
    grammar = Enum(K('septillion'))

class Num1e45(Keyword):
    grammar = Enum(K('septilliardo'))

class Num1e48(Keyword):
    grammar = Enum(K('octillion'))

class Num1e51(Keyword):
    grammar = Enum(K('octilliardo'))

class Num1e54(Keyword):
    grammar = Enum(K('nonillion'))

class Num1e57(Keyword):
    grammar = Enum(K('nonilliardo'))

class Num1e60(Keyword):
    grammar = Enum(K('decillion'))

class Num1e63(Keyword):
    grammar = Enum(K('decilliardo'))

class NumArt0(Keyword):
    grammar = Enum(K('lu'))

class NumArt1(Keyword):
    grammar = Enum(K('lui'))

class NumArt2(Keyword):
    grammar = Enum(K('luo'))

class NumArt3(Keyword):
    grammar = Enum(K('luu'))

class NumArt4(Keyword):
    grammar = Enum(K('luia'))

class NumDiv(Keyword):
    grammar = Enum(K('di'))

class NumPlus(Keyword):
    grammar = Enum(K('plus'))

class NumPoint(Keyword):
    grammar = Enum(K('comma'))

class V(str):
    grammar = re.compile('(ha|es|va|sia)(?=\W)|' + not_a_reserved_word + '\w+(a|e|i)(t|va|ra|rea|n)(?=\W)')

class N0(str):
    grammar = re.compile(not_a_reserved_word + '\w+e(|s)(?=\W)')

class N1(str):
    grammar = re.compile('\w+i(|s)(?=\W)')

class N2(str):
    grammar = re.compile('\w+o(|s)(?=\W)')

class N3(str):
    grammar = re.compile('\w+u(|s)(?=\W)')

class N4(str):
    grammar = re.compile('\w+ia(|s)(?=\W)')

class Inf0(str):
    grammar = re.compile('\w+(a|e|i)r(?=\W)')

class Inf1(str):
    grammar = re.compile('\w+(a|e|i)vur(?=\W)')

class Inf2(str):
    grammar = re.compile('\w+(a|e|i)dur(?=\W)')

class Inf3(str):
    grammar = re.compile('\w+(a|e|i)jur(?=\W)')

class Inf4(str):
    grammar = re.compile('\w+(a|e|i)gur(?=\W)')

class App0(str):
    grammar = re.compile('\w+ef(|s)(?=\W)')

class App1(str):
    grammar = re.compile('\w+if(|s)(?=\W)')

class App2(str):
    grammar = re.compile('\w+of(|s)(?=\W)')

class App3(str):
    grammar = re.compile('\w+uf(|s)(?=\W)')

class App4(str):
    grammar = re.compile('\w+iaf(|s)(?=\W)')

class Adj0(str):
    grammar = re.compile('\w+el(?=\W)')

class Adj1(str):
    grammar = re.compile('\w+il(?=\W)')

class Adj2(str):
    grammar = re.compile('\w+ol(?=\W)')

class Adj3(str):
    grammar = re.compile('\w+ul(?=\W)')

class Adj4(str):
    grammar = re.compile('\w+ial(?=\W)')

class Adv0(str):
    grammar = re.compile('\w+em(?=\W)')

class Adv1(str):
    grammar = re.compile('\w+im(?=\W)')

class Adv2(str):
    grammar = re.compile('\w+om(?=\W)')

class Adv3(str):
    grammar = re.compile('\w+um(?=\W)')

class Adv4(str):
    grammar = re.compile('\w+iam(?=\W)')

class PtcpPres0(str):
    grammar = re.compile('\w+(a|e|ie)nta(?=\W)')

class PtcpPres1(str):
    grammar = re.compile('\w+(a|e|ie)vunta(?=\W)')

class PtcpPres2(str):
    grammar = re.compile('\w+(a|e|ie)dunta(?=\W)')

class PtcpPres3(str):
    grammar = re.compile('\w+(a|e|ie)junta(?=\W)')

class PtcpPres4(str):
    grammar = re.compile('\w+(a|e|ie)gunta(?=\W)')

class PtcpPast0(str):
    grammar = re.compile('\w+(a|i)ta(?=\W)')

class PtcpPast1(str):
    grammar = re.compile('\w+(a|i)vuta(?=\W)')

class PtcpPast2(str):
    grammar = re.compile('\w+(a|i)duta(?=\W)')

class PtcpPast3(str):
    grammar = re.compile('\w+(a|i)juta(?=\W)')

class PtcpPast4(str):
    grammar = re.compile('\w+(a|i)guta(?=\W)')

class N_0_9(List):
    grammar = [Num0, N_1_9]

class N_1_999(List):
    grammar = [
        (N_1_9, Num100, N_10_90, optional(N_0_9)),
        (N_1_9, Num100, optional(N_0_9)),
        (N_10_90, optional(N_0_9)),
        N_1_9
    ]

class N_0_999(List):
    grammar = [Num0, N_1_999]

class N1e3(List):
    grammar = N_1_999, Num1e3, optional(N_0_999)

class N1e6(List):
    grammar = N_1_999, Num1e6, [
        N1e3,
        optional(N_0_999)
    ]

class N1e9(List):
    grammar = N_1_999, Num1e9, [
        N1e6,
        N1e3,
        optional(N_0_999),
    ]

class N1e12(List):
    grammar = N_1_999, Num1e12, [
        N1e9,
        N1e6,
        N1e3,
        optional(N_0_999),
    ]

class N1e15(List):
    grammar = N_1_999, Num1e15, [
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_0_999),
    ]

class N1e18(List):
    grammar = N_1_999, Num1e18, [
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_0_999),
    ]

class N1e21(List):
    grammar = N_1_999, Num1e21, [
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_0_999),
    ]

class N1e24(List):
    grammar = N_1_999, Num1e24, [
        N1e21,
        N1e18,
        N1e15,
        N1e12,
        N1e9,
        N1e6,
        N1e3,
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

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
        optional(N_0_999),
    ]

class Natural(List):
    grammar = [N1e63, N1e60, N1e57, N1e54, N1e51, N1e48, N1e45, N1e42, N1e39, N1e36, N1e33, N1e30, N1e27, N1e24, N1e21, N1e18, N1e15, N1e12, N1e9, N1e6, N1e3, N_0_999]

class Decimal(List):
    grammar = Natural, NumPoint, some(N_0_9)

class Fractional(List):
    grammar = [
        (Natural, NumPlus, Natural, NumDiv, Natural),
        (Natural, NumDiv, Natural)
    ]

class Numeral0(List):
    grammar = NumArt0, [Fractional, Decimal, Natural]

class Numeral1(List):
    grammar = NumArt1, [Fractional, Decimal, Natural]

class Numeral2(List):
    grammar = NumArt2, [Fractional, Decimal, Natural]

class Numeral3(List):
    grammar = NumArt3, [Fractional, Decimal, Natural]

class Numeral4(List):
    grammar = NumArt4, [Fractional, Decimal, Natural]

class AdjP4(List):
    grammar = Adj4, maybe_some(optional(ConjAdj4), Adj4)

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
    grammar = some(App4, maybe_some(AdjP4), maybe_some(PtcpP4))

class NP4(List):
    grammar = N4, maybe_some(AdjP4), maybe_some(PtcpP4), maybe_some(AppP4)

class InfP4(List):
    grammar = optional(Negation), Inf4

class Arg4(List):
    grammar = [(Art, NP4), NP4, InfP4, Numeral4], maybe_some(ConjArg4, [(Art, NP4), NP4, InfP4, Numeral4])

class AdvP4(List):
    grammar = [Adv4, (Prep, Arg4)], maybe_some(ConjAdv4, [Adv4, (Prep, Arg4)])

class AdjP3(List):
    grammar = Adj3, optional(AdvP4), maybe_some(optional(ConjAdj3), Adj3, optional(AdvP4))

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
    grammar = some(App3, maybe_some(AdvP4), maybe_some(AdjP3), maybe_some(PtcpP3))

class NP3(List):
    grammar = N3, maybe_some(AdvP4), maybe_some(AdjP3), maybe_some(PtcpP3), maybe_some(AppP3)

class InfP3(List):
    grammar = optional(Negation), Inf3, optional(Arg4), maybe_some(AdvP4)

class Arg3(List):
    grammar = [(Art, NP3), NP3, InfP3, Numeral3], maybe_some(ConjArg3, [(Art, NP3), NP3, InfP3, Numeral3])

class AdvP3(List):
    grammar = [Adv3, (Prep, Arg3)], optional(AdvP4), maybe_some(ConjAdv3, [Adv3, (Prep, Arg3)], optional(AdvP4))

class AdjP2(List):
    grammar = Adj2, optional(AdvP3), maybe_some(optional(ConjAdj2), Adj2, optional(AdvP3))

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
    grammar = some(App2, maybe_some(AdvP3), maybe_some(AdjP2), maybe_some(PtcpP2))

class NP2(List):
    grammar = N2, maybe_some(AdvP3), maybe_some(AdjP2), maybe_some(PtcpP2), maybe_some(AppP2)

class InfP2(List):
    grammar = optional(Negation), Inf2, optional(Arg3), maybe_some(AdvP3)

class Arg2(List):
    grammar = [(Art, NP2), NP2, InfP2, Numeral2], maybe_some(ConjArg2, [(Art, NP2), NP2, InfP2, Numeral2])

class AdvP2(List):
    grammar = [Adv2, (Prep, Arg2)], optional(AdvP3), maybe_some(ConjAdv2, [Adv2, (Prep, Arg2)], optional(AdvP3))

class AdjP1(List):
    grammar = Adj1, optional(AdvP2), maybe_some(optional(ConjAdj1), Adj1, optional(AdvP2))

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
    grammar = some(App1, maybe_some(AdvP2), maybe_some(AdjP1), maybe_some(PtcpP1))

class NP1(List):
    grammar = N1, maybe_some(AdvP2), maybe_some(AdjP1), maybe_some(PtcpP1), maybe_some(AppP1)

class InfP1(List):
    grammar = optional(Negation), Inf1, optional(Arg2), maybe_some(AdvP2)

class Arg1(List):
    grammar = [(Art, NP1), NP1, InfP1, Numeral1], maybe_some(ConjArg1, [(Art, NP1), NP1, InfP1, Numeral1])

class AdvP1(List):
    grammar = [Adv1, (Prep, Arg1)], optional(AdvP2), maybe_some(ConjAdv1, [Adv1, (Prep, Arg1)], optional(AdvP2))

class AdjP0(List):
    grammar = Adj0, optional(AdvP1), maybe_some(optional(ConjAdj0), Adj0, optional(AdvP1))

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
    grammar = some(App0, maybe_some(AdvP1), maybe_some(AdjP0), maybe_some(PtcpP0))

class NP0(List):
    grammar = N0, maybe_some(AdvP1), maybe_some(AdjP0), maybe_some(PtcpP0), maybe_some(AppP0)

class InfP0(List):
    grammar = optional(Negation), Inf0, optional(Arg1), maybe_some(AdvP1)

class Arg0(List):
    grammar = [(Art, NP0), NP0, InfP0, Numeral0], maybe_some(ConjArg0, [(Art, NP0), NP0, InfP0, Numeral0])

class AdvP0(List):
    grammar = [Adv0, (Prep, Arg0)], optional(AdvP1), maybe_some(ConjAdv0, [Adv0, (Prep, Arg0)], optional(AdvP1))

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