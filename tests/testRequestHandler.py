from ppp_cas.requesthandler import RequestHandler
from ppp_datamodel import Request
from ppp_datamodel.nodes.resource import Resource, MathLatexResource
from ppp_datamodel import Sentence
from unittest import TestCase

class TestRequestHandler(TestCase):

    def testNaturalMath(self):
        testCases=['derivative of cos(x)',
                   'sum of derivative of cos(x)^i',
                   'sum of derivative of cos(x)^i from 1 to n',
                   'sum derivative cos(x)^i',
                   'limit derivative cos(x)^i',
                   'integrate cos(x)^i',
                   'antiderivative cos(x)^i',
                   'approx sqrt(2)',
                  ]
        for expr in testCases:
            handler = RequestHandler(Request(0, 'math', Sentence(expr)))
            self.assertEqual(len(handler.answer()), 0)

    def testMathUnhandlable(self):
        testCases=['2f(x)b',
                  ]
        for expr in testCases:
            handler = RequestHandler(Request(0, 'math', Sentence(expr)))
            self.assertEqual(len(handler.answer()), 0)
            
    def testError(self):
        testCases = [('D(cos)'),
                    ]
        for expr in testCases:
            handler = RequestHandler(Request(0, 'math', Sentence(expr)))
            self.assertEqual(len(handler.answer()), 0)

    def testMath(self):
        testCases=['5+7',
                   '2^42',
                   'sqrt((42)**(pi))',
                   'diff(x**2,x)',
                   'Solve[x^2==1, x]',
                   'C(3.7,1.3)',
                   'lcm(n,m)hcf(n,m)',
                   'integrate(exp(-x**2), x, -infty, infty)',
                   'sqrt(2)',
                  ]
        for expr in testCases:
            handler = RequestHandler(Request(0, 'math', Sentence(expr)))
            self.assertEqual(len(handler.answer()), 1)

    def testTree(self):
        testCases=[('5+7', '12', '12'),
                   ('2^42', '4398046511104', '4398046511104'),
                   ('sqrt((42)**(pi))', '42**(pi/2)', '42^{\\frac{\pi}{2}}'),
                   ('diff(x**2,x)', '2*x', '2 x'),
                   ('Solve[x^2==1, x]', '[(-1,), (1,)]', '\left [ \left ( -1\\right ), \quad \left ( 1\\right )\\right ]'),
                   ('C(3.7,1.3)', '4.43659695748368', '4.43659695748368'),
                   ('lcm(n,m)hcf(n,m)', 'm*n', 'm n'),
                   ('integrate(exp(-x**2), x, -infty, infty)', 'sqrt(pi)', '\\sqrt{\\pi}'),
                   ('sqrt(2)', 'sqrt(2)', '\\sqrt{2}'),
                   ('Integrate[Sin[x*y], {x, 0, 1}, {y, 0, x}]', '-Ci(1)/2 + EulerGamma/2', '- \\frac{1}{2} \\operatorname{Ci}{\\left (1 \\right )} + \\frac{\\gamma}{2}'),
                  ]
        for (expr, naturalExpr, latexExpr) in testCases:
            handler = RequestHandler(Request(0, 'math', Sentence(expr)))
            self.assertEqual(handler.answer()[0].tree, MathLatexResource(naturalExpr, latex=latexExpr))

    def testNoMath(self):
        naturalLanguageSentences=[  'What is the birth date of the president of the United States?',
                                    'What is the birth date of George Washington?',
                                    'Who is the director of \"Pulp Fiction\"?',
                                    'Who is the president of France?',
                                    'What is the capital of Australia?',
                                    'Who is the author of \"Foundation\"?',
                                    'Name cities that have an Amtrak terminal.',
                                    'can you drink milk after the expiration date',
                                    'Name their songs.',
                                    'WW2',
                                    'What is the birth date of the president of the United States?',
                                    'What is the birth date of George Washington?',
                                    'Who is the director of \"Pulp Fiction\"?',
                                    'Who is the president of France?',
                                    'What is the capital of Australia?',
                                    'Who is the author of \"Foundation\"?',
                                    'Who wrote Nineteen Eighty-Four?',
                                    'When was the first Crip gang started?',
                                    'What does the name mean or come from?',
                                    'Which cities have Crip gangs?',
                                    'What ethnic group/race are Crip members?',
                                    'What is their gang color?',
                                    'What is the name of Durst\'s group?',
                                    'What record company is he with?',
                                    'What are titles of the group\'s releases?',
                                    'Where was Durst born?',
                                    'When was the comet discovered?',
                                    'How often does it approach the earth?',
                                    'In what countries was the comet visible on its last return?',
                                    'When was James Dean born?',
                                    'When did James Dean die?',
                                    'How did he die?',
                                    'What movies did he appear in?',
                                    'Which was the first movie that he was in?',
                                    'What does AARP stand for?',
                                    'When was the organization started?',
                                    'Where is its headquarters?',
                                    'Who is its top official or CEO?',
                                    'What companies has AARP endorsed?',
                                    'How long does one study as a Rhodes scholar?',
                                    'Where do Rhodes scholars study?',
                                    'Name famous people who have been Rhodes scholars.',
                                    'What countries have Rhodes scholars come from?',
                                    'What kind of animal is an agouti?',
                                    'What is their average life span?',
                                    'In what countries are they found?',
                                    'Who founded the Black Panthers organization?',
                                    'When was it founded?',
                                    'Where was it founded?',
                                    'Who have been members of the organization?',
                                    'Who are the members of this group?',
                                    'What albums have they made?',
                                    'What is their style of music?',
                                    'What is their biggest hit?',
                                    'What are prions made of?',
                                    'Who discovered prions?',
                                    'What diseases are prions associated with?',
                                    'What researchers have worked with prions?',
                                    'Who is the lead singer/musician in Nirvana?',
                                    'Who are the band members?',
                                    'When was the band formed?',
                                    'What is their biggest hit?',
                                    'What are their albums?',
                                    'What style of music do they play?',
                                    'What industry is Rohm and Haas in?',
                                    'Where is the company located?',
                                    'What is their annual revenue?',
                                    'How many employees does it have?',
                                    'What film introduced Jar Jar Binks?',
                                    'What actor is used as his voice?',
                                    'To what alien race does he belong?',
                                    'Horus is the god of what?',
                                    'What country is he associated with?',
                                    'Who was his mother?',
                                    'Who was his father?',
                                    'Who are the members of the Rat Pack?',
                                    'Who coined the name?',
                                    'What Las Vegas hotel was made famous by the Rat Pack?',
                                    'What is the primary symptom of a cataract?',
                                    'How are they treated?',
                                    'Who are doctors that have performed cataract surgery?',
                                    'When was the court established?',
                                    'What kind of cases does it try?',
                                    'Who is the sponsor of the court?',
                                    'How many justices are members of the court?',
                                    'What division (weight) did he win?',
                                    'When did he win the title?',
                                    'How old was he when he won the title?',
                                    'Who did he beat to win the title?',
                                    'Who beat him to take the title away?',
                                    'List the names of boxers he fought.',
                                    'What kind of a community is a Kibbutz?',
                                    'With what country are they associated?',
                                    'When was the first Kibbutz founded?',
                                    'Where was the first Kibbutz founded?',
                                    'How many are there now?',
                                    'In what year did the first Concorde passenger flight take place?',
                                    'What airlines have Concordes in their fleets?',
                                    'How many seats are in the cabin of a Concorde?',
                                    'How fast does the Concorde fly?',
                                    'What year was the first Concorde crash?',
                                    'How many Club Med vacation spots are there worldwide?',
                                    'List the spots in the United States.',
                                    'Where is an adults-only Club Med?',
                                    'Where was Franz Kafka born?',
                                    'When was he born?',
                                    'What is his ethnic background?',
                                    'What books did he author?',
                                    'In what film is Gordon Gekko the main character?',
                                    'Who plays the role?',
                                    'What year was the movie released?',
                                    'What was Gekko\'s profession?',
                                    'When was he born?',
                                    'What nationality is he?',
                                    'Where did he study architecture?',
                                    'What prizes or awards has he won?',
                                    'What buildings has he designed?',
                                    'What sport do they play?',
                                    'When were they founded?',
                                    'By whom were they founded?',
                                    'What countries have they played in?',
                                    'What kind of singer is Ice-T?',
                                    'What was his original name?',
                                    'When was he born?',
                                    'Where was he born?',
                                    'What are names of his albums?',
                                    'What sport does Jennifer Capriati play?',
                                    'Who is her coach?',
                                    'Where does she live?',
                                    'When was she born?',
                                    'What kind of business is Abercrombie and Fitch?',
                                    'When was it established?',
                                    'Where was it established?',
                                    'How many stores are there?',
                                    'Why is the \'Tale of Genji\' famous?',
                                    'Who wrote it?',
                                    'When was it written?',
                                    'What is Al Jolson\'s real name?',
                                    'What is his nationality?',
                                    'Where was he born?',
                                    'Who did he marry?',
                                    'What songs did he sing?',
                                    'What was Jean Harlow\'s real name?',
                                    'Where was she born?',
                                    'When did she die?',
                                    'How old was she when she died?',
                                    'What did she die of?',
                                    'Where is she buried?',
                                    'What movies did she appear in?',
                                    'What leading men did she star opposite of?',
                                    'What do practitioners of Wicca worship?',
                                    'How many followers does it have?',
                                    'Who is its leader?',
                                    'What festivals does it have?',
                                    'What is Florence Nightingale famous for?',
                                    'When was she born?',
                                    'Where was she born?',
                                    'When did she die?',
                                    'When did Amtrak begin operations?',
                                    'How many passengers does it serve annually?',
                                    'How many employees does it have?',
                                    'Who is the president or chief executive of Amtrak?',
                                    'When did Jack Welch become chairman of General Electric?',
                                    'How many years was he with GE?',
                                    'When did he retire from GE?',
                                    'How many people did he fire from GE?',
                                    'In what country did this movement take place?',
                                    'When did the Khmer Rouge come into power?',
                                    'Who was its first leader?',
                                    'Who were leaders of the Khmer Rouge?',
                                    'When was the Khmer Rouge removed from power?',
                                    'How many members are there in the singing group the Wiggles?',
                                    'Who are the members\' names?',
                                    'Where is the group from?',
                                    'List the Wiggles\' songs.',
                                    'What kind of a particle is a quark?',
                                    'Who discovered quarks?',
                                    'When were they discovered?',
                                    'What are the different types of quarks?',
                                    'What kind of music does the band play?',
                                    'In what year was their first major album recorded?',
                                    'When was Nimitz born?',
                                    'What town was he native of?',
                                    'What branch of the military did he serve in?',
                                    'During what war did he serve?',
                                    'What rank did he reach?',
                                    'What year did the Teapot Dome scandal take place?',
                                    'Who was President of the United States at the time?',
                                    'What was the main focus of the scandal?',
                                    'Who were the major players involved in the scandal?',
                                    'When was the USS Constitution commissioned?',
                                    'What conflict did she distinguish herself in?',
                                    'How many battles did she win?',
                                    'What is her nickname?',
                                    'Who established the awards?',
                                    'What are the different categories of Nobel prizes?',
                                    'When were the awards first given?',
                                    'What is the monetary value of the prize?',
                                    'What tribe did Sacajawea belong to?',
                                    'What years did she accompany Lewis and Clark on their expedition?',
                                    'When was she born?',
                                    'When did she die?',
                                    'Where is she buried?',
                                    'How much is the Sacajawea coin worth?',
                                    'When was the IFC established?',
                                    'What is its mission?',
                                    'What countries has the IFC financed projects in?',
                                    'Who was the leader of the cult?',
                                    'How many of its members committed suicide?',
                                    'When did the mass suicide occur?',
                                    'Where did it occur?',
                                    'How did they commit suicide?',
                                    'Why did they commit suicide?',
                                    'On what date was Bashar Assad inaugurated as the Syrian president?',
                                    'What is his party affiliation?',
                                    'What was his profession prior to assuming the Presidency?',
                                    'How long are Syrian presidential terms?',
                                    'What schools did he attend?',
                                    'When was Abu Nidal born?',
                                    'What was his name at birth?',
                                    'How many followers does he have?',
                                    'In what countries has he operated from?',
                                    'In what year did the PLO condemn him to death?',
                                    'What is Carlos\' real name?',
                                    'Where was he born?',
                                    'Whom did he marry?',
                                    'When was he captured?',
                                    'Where was he captured?',
                                    'When was Cassini launched?',
                                    'How much did it cost to build?',
                                    'What is its destination?',
                                    'What planets will it pass?',
                                    'What is the religious affiliation of the Kurds?',
                                    'How many Kurds live in Turkey?',
                                    'What other countries do Kurds live in?',
                                    'When was the first Burger King restaurant opened?',
                                    'Where was the first restaurant opened?',
                                    'Who founded it?',
                                    'What are Burger King\'s gross sales today?',
                                    'What countries is Burger King located in?',
                                    'Who is the CEO of the publishing company Conde Nast?',
                                    'Where are the company\'s headquarters?',
                                    'When was the company founded?',
                                    'What magazines does Conde Nast publish?',
                                    'Where was she born?',
                                    'How many siblings does she have?',
                                    'Whom did she marry?',
                                    'How many children does she have?',
                                    'Where does she live?',
                                    'What schools did she attend?',
                                    'What is her occupation?',
                                    'What branch of the service did she serve in?',
                                    'What rank did she reach?',
                                    'Where was he born?',
                                    'When was he born?',
                                    'How old was he when he began writing?',
                                    'What books has he written?',
                                    'When was the agreement made?',
                                    'What is the purpose of the agreement?',
                                    'What groups are affected by it?',
                                    'Who were the key players in negotiating the agreement?',
                                    'What kind of ship is the Liberty Bell 7?',
                                    'Who developed it?',
                                    'What is it made of?',
                                    'What happened to it?',
                                    'What is Vilar\'s nationality?',
                                    'What organizations has he donated money to?',
                                    'What is the name of the company he founded?',
                                    'What companies has he invested in?',
                                    'Who founded Public Citizen?',
                                    'When was it formed?',
                                    'What is its purpose?',
                                    'How many members does it have?',
                                    'Who is its current head?',
                                    'What state does he represent?',
                                    'When was he born?',
                                    'When was he first elected to the senate?',
                                    'What branch of the service did he serve in?',
                                    'Who founded the Muslim Brotherhood?',
                                    'When was it formed?',
                                    'What is its goal?',
                                    'What countries does it operate in?',
                                    'Name members of the group?',
                                    'Where is the center located?',
                                    'When was the center formed?',
                                    'What is its mission?',
                                    'Name members of the center.',
                                    'What kind of insect is a boll weevil?',
                                    'What type of plant does it damage?',
                                    'What states have had problems with boll weevils?',
                                    'What was Johnny Appleseed\'s real name?',
                                    'Where was he born?',
                                    'When did he die?',
                                    'What did he wear as a hat?',
                                    'In what states did he plant trees?',
                                    'What are the names of the space shuttles?',
                                    'Which was the first shuttle?',
                                    'When was the first flight?',
                                    'When was the Challenger space shuttle disaster?',
                                    'How many members were in the crew of the Challenger?',
                                    'How long did the Challenger flight last before it exploded?',
                                    'Where do the birds hide when it rains?',
                                    'Who is Gandhi?',
                                    'Qui a mangé la chèvre de monsieur Seguin?',
                                    'Who is the president of France?',
                                    'Who is the author of the Petit Prince?',
                                    'What is the weather like tomorrow?',
                                    'Why is the sky blue?',
                                    'Who is  Heisenberg?',
                                    'What is SAT problem?',
                                    'When did Steve Jobs die?',
                                    'When will Bill Gates die?',
                                    'Who is the singer of Led Zeppelin?',
                                    'What is the men average height?',
                                    'What is the speed of light ?',
                                    'Who won Roland-Garros this year?',
                                    'Did Djokovic win Roland-Garros?',
                                    'Is p=np an open problem?',
                                    'What is the birthdate of Rene Descartes?',
                                    'What is the Ecole Normale Supérieure?',
                                    'What is the birth date of the first United States president?',
                                    'When is the national day of China?',
                                    'What is the capital of Liechtenstein?',
                                    'Why does a rainbow form?',
                                    'Did Marilyn Monroe and Cary Grant ever appear in a movie together?',
                                    'Who is the King of Lesotho?',
                                    'Tell me the name of the King of Lesotho.',
                                    'how to get pregnant',
                                    'where can i find pictures of hairstyles ',
                                    'who is the richest man in the world',
                                    'what is the difference between white eggs and brown eggs',
                                    'Antoine de Saint-Exupéry',
                                    'Author of bli-bla',
                                    'Saint-Exupery',
                                   ]

        for expr in naturalLanguageSentences:
            handler = RequestHandler(Request(0, 'math', Sentence(expr)))
            self.assertEqual(len(handler.answer()), 0)

        self.assertEqual(len(RequestHandler(Request(0, 'math', Resource(''))).answer()), 0)
