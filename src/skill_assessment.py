"""
Advanced Skill Assessment System with Quiz-Based Evaluation
Evaluates programming language proficiency through targeted questions
"""

import json
import random
from typing import Dict, List, Tuple

class SkillAssessmentEngine:
    """
    Comprehensive skill assessment with quiz-based evaluation
    """
    
    def __init__(self):
        self.quiz_database = self._initialize_quiz_database()
        self.proficiency_levels = {
            'beginner': {'min_score': 0, 'max_score': 40, 'weight': 0.3},
            'intermediate': {'min_score': 41, 'max_score': 75, 'weight': 0.6},
            'advanced': {'min_score': 76, 'max_score': 100, 'weight': 1.0}
        }
    
    def _initialize_quiz_database(self) -> Dict:
        """Initialize comprehensive quiz database for different technologies"""
        return {
            'python': {
                'beginner': [
                    {
                        'question': 'What is the correct way to create a list in Python?',
                        'options': ['list = []', 'list = ()', 'list = {}', 'list = <>'],
                        'correct': 0,
                        'explanation': 'Square brackets [] are used to create lists in Python'
                    },
                    {
                        'question': 'Which keyword is used to define a function in Python?',
                        'options': ['function', 'def', 'func', 'define'],
                        'correct': 1,
                        'explanation': 'The "def" keyword is used to define functions in Python'
                    },
                    {
                        'question': 'What will print(type(5)) output?',
                        'options': ["<class 'int'>", "<class 'float'>", "<class 'str'>", "number"],
                        'correct': 0,
                        'explanation': '5 is an integer, so type(5) returns <class "int">'
                    },
                    {
                        'question': 'How do you add an item to a list in Python?',
                        'options': ['list.add(item)', 'list.append(item)', 'list.insert(item)', 'list.push(item)'],
                        'correct': 1,
                        'explanation': 'append() method is used to add items to the end of a list'
                    },
                    {
                        'question': 'What is the correct syntax for a for loop in Python?',
                        'options': ['for i in range(10):', 'for (i=0; i<10; i++):', 'for i=1 to 10:', 'foreach i in 10:'],
                        'correct': 0,
                        'explanation': 'Python uses "for variable in iterable:" syntax'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'What is a list comprehension in Python?',
                        'options': ['A way to compress lists', 'A concise way to create lists', 'A list method', 'A data type'],
                        'correct': 1,
                        'explanation': 'List comprehensions provide a concise way to create lists based on existing lists'
                    },
                    {
                        'question': 'What does the *args parameter do in a function?',
                        'options': ['Multiplies arguments', 'Accepts variable number of arguments', 'Creates a pointer', 'Defines required arguments'],
                        'correct': 1,
                        'explanation': '*args allows a function to accept any number of positional arguments'
                    },
                    {
                        'question': 'What is the difference between "==" and "is" in Python?',
                        'options': ['No difference', '"==" compares values, "is" compares identity', '"is" compares values, "==" compares identity', 'Both compare identity'],
                        'correct': 1,
                        'explanation': '"==" compares values for equality, "is" checks if objects are the same in memory'
                    },
                    {
                        'question': 'What is a Python decorator?',
                        'options': ['A design pattern', 'A function that modifies another function', 'A class method', 'A data structure'],
                        'correct': 1,
                        'explanation': 'Decorators are functions that modify or extend the behavior of other functions'
                    },
                    {
                        'question': 'What does the "yield" keyword do?',
                        'options': ['Stops execution', 'Creates a generator', 'Returns a value', 'Raises an exception'],
                        'correct': 1,
                        'explanation': '"yield" creates a generator function that can pause and resume execution'
                    }
                ],
                'advanced': [
                    {
                        'question': 'What is the Global Interpreter Lock (GIL) in Python?',
                        'options': ['A security feature', 'A mutex that allows only one thread to execute Python bytecode', 'A memory manager', 'A compiler optimization'],
                        'correct': 1,
                        'explanation': 'GIL prevents multiple native threads from executing Python bytecodes simultaneously'
                    },
                    {
                        'question': 'What is metaclass in Python?',
                        'options': ['A parent class', 'A class whose instances are classes', 'A module', 'An abstract class'],
                        'correct': 1,
                        'explanation': 'Metaclasses are classes whose instances are classes themselves'
                    },
                    {
                        'question': 'What is the purpose of __slots__ in Python classes?',
                        'options': ['Define methods', 'Restrict attribute creation and save memory', 'Create properties', 'Define inheritance'],
                        'correct': 1,
                        'explanation': '__slots__ restricts the attributes that can be created and reduces memory usage'
                    },
                    {
                        'question': 'What is monkey patching in Python?',
                        'options': ['Debugging technique', 'Dynamically modifying classes or modules at runtime', 'Error handling', 'Code optimization'],
                        'correct': 1,
                        'explanation': 'Monkey patching allows dynamic modification of classes or modules during runtime'
                    },
                    {
                        'question': 'What is the difference between deepcopy and shallow copy?',
                        'options': ['No difference', 'Deepcopy creates independent copy of nested objects', 'Shallow copy is faster', 'Deepcopy uses less memory'],
                        'correct': 1,
                        'explanation': 'Deepcopy creates independent copies of all nested objects, shallow copy only copies references'
                    }
                ]
            },
            'java': {
                'beginner': [
                    {
                        'question': 'What is the correct way to declare a variable in Java?',
                        'options': ['int x;', 'var x;', 'integer x;', 'number x;'],
                        'correct': 0,
                        'explanation': 'Java uses type followed by variable name: int x;'
                    },
                    {
                        'question': 'Which method is called when an object is created?',
                        'options': ['main()', 'constructor', 'init()', 'create()'],
                        'correct': 1,
                        'explanation': 'Constructor is automatically called when an object is instantiated'
                    },
                    {
                        'question': 'What is the entry point of a Java application?',
                        'options': ['start() method', 'main() method', 'begin() method', 'init() method'],
                        'correct': 1,
                        'explanation': 'main() method is the entry point of any Java application'
                    },
                    {
                        'question': 'Which keyword is used for inheritance in Java?',
                        'options': ['inherits', 'extends', 'implements', 'derives'],
                        'correct': 1,
                        'explanation': 'extends keyword is used for class inheritance in Java'
                    },
                    {
                        'question': 'What is the size of int data type in Java?',
                        'options': ['16 bits', '32 bits', '64 bits', 'Platform dependent'],
                        'correct': 1,
                        'explanation': 'int data type is always 32 bits in Java, regardless of platform'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'What is polymorphism in Java?',
                        'options': ['Multiple inheritance', 'Same method behaving differently', 'Data hiding', 'Code reusability'],
                        'correct': 1,
                        'explanation': 'Polymorphism allows the same method to behave differently based on the object type'
                    },
                    {
                        'question': 'What is the difference between ArrayList and LinkedList?',
                        'options': ['No difference', 'ArrayList uses array, LinkedList uses nodes', 'ArrayList is faster', 'LinkedList uses less memory'],
                        'correct': 1,
                        'explanation': 'ArrayList uses dynamic arrays while LinkedList uses doubly-linked list structure'
                    },
                    {
                        'question': 'What is exception handling in Java?',
                        'options': ['Error prevention', 'Graceful handling of runtime errors', 'Code optimization', 'Memory management'],
                        'correct': 1,
                        'explanation': 'Exception handling allows graceful handling of runtime errors using try-catch blocks'
                    },
                    {
                        'question': 'What is the purpose of synchronized keyword?',
                        'options': ['Speed optimization', 'Thread safety', 'Memory management', 'Exception handling'],
                        'correct': 1,
                        'explanation': 'synchronized keyword ensures thread safety by allowing only one thread at a time'
                    },
                    {
                        'question': 'What is the difference between == and equals() method?',
                        'options': ['No difference', '== compares references, equals() compares content', 'equals() is faster', '== compares content'],
                        'correct': 1,
                        'explanation': '== compares object references while equals() compares actual content'
                    }
                ],
                'advanced': [
                    {
                        'question': 'What is Java Memory Model?',
                        'options': ['Garbage collection', 'Defines how threads interact through memory', 'Heap structure', 'Stack allocation'],
                        'correct': 1,
                        'explanation': 'Java Memory Model defines how threads interact through memory and what behaviors are allowed'
                    },
                    {
                        'question': 'What is the purpose of volatile keyword?',
                        'options': ['Memory optimization', 'Ensures variable visibility across threads', 'Prevents inheritance', 'Declares constants'],
                        'correct': 1,
                        'explanation': 'volatile ensures that variable changes are visible to all threads immediately'
                    },
                    {
                        'question': 'What is reflection in Java?',
                        'options': ['Code mirroring', 'Runtime inspection and modification of classes', 'Design pattern', 'Memory management'],
                        'correct': 1,
                        'explanation': 'Reflection allows runtime inspection and modification of classes, methods, and fields'
                    },
                    {
                        'question': 'What is the difference between ConcurrentHashMap and HashMap?',
                        'options': ['No difference', 'ConcurrentHashMap is thread-safe', 'HashMap is faster', 'ConcurrentHashMap uses less memory'],
                        'correct': 1,
                        'explanation': 'ConcurrentHashMap is thread-safe and designed for concurrent access'
                    },
                    {
                        'question': 'What is JVM bytecode?',
                        'options': ['Source code', 'Intermediate code executed by JVM', 'Machine code', 'Assembly language'],
                        'correct': 1,
                        'explanation': 'Bytecode is intermediate code that JVM executes, making Java platform-independent'
                    }
                ]
            },
            'javascript': {
                'beginner': [
                    {
                        'question': 'How do you declare a variable in JavaScript?',
                        'options': ['var x;', 'variable x;', 'declare x;', 'int x;'],
                        'correct': 0,
                        'explanation': 'var, let, or const keywords are used to declare variables in JavaScript'
                    },
                    {
                        'question': 'What is the correct way to create a function in JavaScript?',
                        'options': ['function myFunc() {}', 'def myFunc() {}', 'func myFunc() {}', 'create myFunc() {}'],
                        'correct': 0,
                        'explanation': 'function keyword followed by function name and parentheses'
                    },
                    {
                        'question': 'How do you add an element to an array in JavaScript?',
                        'options': ['array.add()', 'array.push()', 'array.append()', 'array.insert()'],
                        'correct': 1,
                        'explanation': 'push() method adds elements to the end of an array'
                    },
                    {
                        'question': 'What does DOM stand for?',
                        'options': ['Document Object Model', 'Data Object Management', 'Dynamic Object Model', 'Document Oriented Model'],
                        'correct': 0,
                        'explanation': 'DOM represents the page structure as a tree of objects'
                    },
                    {
                        'question': 'How do you select an element by ID in JavaScript?',
                        'options': ['document.selectById()', 'document.getElementById()', 'document.getElement()', 'document.findById()'],
                        'correct': 1,
                        'explanation': 'getElementById() method selects elements by their ID attribute'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'What is a closure in JavaScript?',
                        'options': ['A loop structure', 'Function with access to outer scope variables', 'A data type', 'An event handler'],
                        'correct': 1,
                        'explanation': 'Closures allow functions to access variables from their outer scope even after the outer function returns'
                    },
                    {
                        'question': 'What is the difference between let and var?',
                        'options': ['No difference', 'let has block scope, var has function scope', 'var is newer', 'let is faster'],
                        'correct': 1,
                        'explanation': 'let provides block scope while var provides function scope'
                    },
                    {
                        'question': 'What is event bubbling?',
                        'options': ['Event creation', 'Events propagating from child to parent', 'Event deletion', 'Event optimization'],
                        'correct': 1,
                        'explanation': 'Event bubbling is when events propagate from the target element up to the document'
                    },
                    {
                        'question': 'What is a Promise in JavaScript?',
                        'options': ['A guarantee', 'Object representing eventual completion of async operation', 'A data type', 'A function type'],
                        'correct': 1,
                        'explanation': 'Promises represent the eventual completion (or failure) of asynchronous operations'
                    },
                    {
                        'question': 'What is the purpose of async/await?',
                        'options': ['Speed optimization', 'Writing asynchronous code synchronously', 'Error handling', 'Memory management'],
                        'correct': 1,
                        'explanation': 'async/await provides a way to write asynchronous code that looks and behaves like synchronous code'
                    }
                ],
                'advanced': [
                    {
                        'question': 'What is the JavaScript Event Loop?',
                        'options': ['A for loop', 'Mechanism for handling asynchronous operations', 'Event creation process', 'DOM manipulation'],
                        'correct': 1,
                        'explanation': 'Event loop manages the execution of multiple pieces of code, handling async operations'
                    },
                    {
                        'question': 'What is prototype inheritance?',
                        'options': ['Class inheritance', 'Objects inheriting from other objects', 'Function inheritance', 'Variable inheritance'],
                        'correct': 1,
                        'explanation': 'JavaScript uses prototype-based inheritance where objects can inherit directly from other objects'
                    },
                    {
                        'question': 'What is hoisting in JavaScript?',
                        'options': ['Variable elevation', 'Moving declarations to the top of scope', 'Memory optimization', 'Error handling'],
                        'correct': 1,
                        'explanation': 'Hoisting moves variable and function declarations to the top of their containing scope'
                    },
                    {
                        'question': 'What is a WeakMap in JavaScript?',
                        'options': ['Slow map', 'Map with weak references to keys', 'Small map', 'Temporary map'],
                        'correct': 1,
                        'explanation': 'WeakMap holds weak references to keys, allowing garbage collection of unused keys'
                    },
                    {
                        'question': 'What is the difference between call, apply, and bind?',
                        'options': ['No difference', 'Different ways to set function context', 'Different performance', 'Different syntax only'],
                        'correct': 1,
                        'explanation': 'call, apply, and bind are different methods to explicitly set the "this" context of functions'
                    }
                ]
            },
            'cpp': {
                'beginner': [
                    {
                        'question': 'Which header file is needed for input/output operations?',
                        'options': ['<stdio.h>', '<iostream>', '<input.h>', '<output.h>'],
                        'correct': 1,
                        'explanation': '<iostream> header provides input/output stream functionality in C++'
                    },
                    {
                        'question': 'What is the correct way to declare a pointer?',
                        'options': ['int ptr;', 'int *ptr;', 'int &ptr;', 'pointer int ptr;'],
                        'correct': 1,
                        'explanation': 'Asterisk (*) is used to declare pointers in C++'
                    },
                    {
                        'question': 'Which operator is used to access class members through pointer?',
                        'options': ['.', '->', '::', '*'],
                        'correct': 1,
                        'explanation': 'Arrow operator (->) is used to access members through pointers'
                    },
                    {
                        'question': 'What is the size of char data type in C++?',
                        'options': ['1 byte', '2 bytes', '4 bytes', 'Platform dependent'],
                        'correct': 0,
                        'explanation': 'char is always 1 byte in C++ by definition'
                    },
                    {
                        'question': 'Which keyword is used to define a class?',
                        'options': ['struct', 'class', 'object', 'define'],
                        'correct': 1,
                        'explanation': 'class keyword is used to define classes in C++'
                    }
                ],
                'intermediate': [
                    {
                        'question': 'What is polymorphism in C++?',
                        'options': ['Multiple inheritance', 'Same interface, different implementations', 'Data hiding', 'Memory management'],
                        'correct': 1,
                        'explanation': 'Polymorphism allows objects of different types to be treated as instances of the same type'
                    },
                    {
                        'question': 'What is the difference between new and malloc?',
                        'options': ['No difference', 'new calls constructor, malloc does not', 'malloc is faster', 'new uses less memory'],
                        'correct': 1,
                        'explanation': 'new allocates memory and calls constructor, malloc only allocates memory'
                    },
                    {
                        'question': 'What is RAII in C++?',
                        'options': ['Algorithm', 'Resource Acquisition Is Initialization', 'Data structure', 'Design pattern'],
                        'correct': 1,
                        'explanation': 'RAII binds resource lifetime to object lifetime for automatic resource management'
                    },
                    {
                        'question': 'What is a virtual function?',
                        'options': ['Abstract function', 'Function that can be overridden', 'Template function', 'Static function'],
                        'correct': 1,
                        'explanation': 'Virtual functions enable runtime polymorphism through dynamic dispatch'
                    },
                    {
                        'question': 'What is the purpose of const keyword?',
                        'options': ['Speed optimization', 'Prevents modification', 'Memory allocation', 'Error handling'],
                        'correct': 1,
                        'explanation': 'const prevents modification of variables, ensuring immutability'
                    }
                ],
                'advanced': [
                    {
                        'question': 'What is template metaprogramming?',
                        'options': ['Runtime programming', 'Compile-time computation using templates', 'Design pattern', 'Memory optimization'],
                        'correct': 1,
                        'explanation': 'Template metaprogramming performs computations at compile time using template instantiation'
                    },
                    {
                        'question': 'What is SFINAE in C++?',
                        'options': ['Algorithm', 'Substitution Failure Is Not An Error', 'Data structure', 'Compiler optimization'],
                        'correct': 1,
                        'explanation': 'SFINAE allows template specialization to fail gracefully without causing compilation errors'
                    },
                    {
                        'question': 'What is move semantics in C++11?',
                        'options': ['Object movement', 'Transferring resources without copying', 'Memory allocation', 'Thread synchronization'],
                        'correct': 1,
                        'explanation': 'Move semantics allows efficient transfer of resources from temporary objects'
                    },
                    {
                        'question': 'What is the purpose of std::unique_ptr?',
                        'options': ['Shared ownership', 'Exclusive ownership with automatic cleanup', 'Reference counting', 'Memory optimization'],
                        'correct': 1,
                        'explanation': 'unique_ptr provides exclusive ownership with automatic resource cleanup'
                    },
                    {
                        'question': 'What is perfect forwarding?',
                        'options': ['Error forwarding', 'Preserving value category when forwarding arguments', 'Memory forwarding', 'Exception forwarding'],
                        'correct': 1,
                        'explanation': 'Perfect forwarding preserves the value category (lvalue/rvalue) of forwarded arguments'
                    }
                ]
            }
        }
    
    def conduct_skill_assessment(self, languages: List[str], questions_per_level: int = 3) -> Dict:
        """
        Conduct comprehensive skill assessment for given languages
        """
        assessment_results = {}
        
        for language in languages:
            language_lower = language.lower().strip()
            if language_lower in self.quiz_database:
                print(f"\n🧪 Starting {language.title()} Assessment")
                print("=" * 40)
                
                language_result = self._assess_single_language(language_lower, questions_per_level)
                assessment_results[language] = language_result
            else:
                # For languages not in quiz database, use general programming assessment
                assessment_results[language] = self._general_assessment(language)
        
        return assessment_results
    
    def _assess_single_language(self, language: str, questions_per_level: int) -> Dict:
        """Assess proficiency in a specific language"""
        total_score = 0
        total_questions = 0
        level_scores = {}
        
        for level in ['beginner', 'intermediate', 'advanced']:
            questions = self.quiz_database[language][level]
            selected_questions = random.sample(questions, min(questions_per_level, len(questions)))
            
            level_score = 0
            print(f"\n📚 {level.title()} Level Questions:")
            print("-" * 30)
            
            for i, question in enumerate(selected_questions, 1):
                print(f"\nQ{i}. {question['question']}")
                for j, option in enumerate(question['options']):
                    print(f"   {j+1}. {option}")
                
                # Simulate user answer (in real app, get from user input)
                # For demo, we'll simulate based on difficulty
                if level == 'beginner':
                    simulated_correct_rate = 0.8
                elif level == 'intermediate':
                    simulated_correct_rate = 0.6
                else:
                    simulated_correct_rate = 0.4
                
                is_correct = random.random() < simulated_correct_rate
                
                if is_correct:
                    level_score += 1
                    print(f"   ✅ Correct! {question['explanation']}")
                else:
                    print(f"   ❌ Incorrect. {question['explanation']}")
            
            level_percentage = (level_score / len(selected_questions)) * 100
            level_scores[level] = {
                'score': level_score,
                'total': len(selected_questions),
                'percentage': level_percentage
            }
            
            total_score += level_score
            total_questions += len(selected_questions)
            
            print(f"\n{level.title()} Score: {level_score}/{len(selected_questions)} ({level_percentage:.1f}%)")
        
        overall_percentage = (total_score / total_questions) * 100
        proficiency_level = self._determine_proficiency_level(overall_percentage)
        
        return {
            'overall_score': total_score,
            'total_questions': total_questions,
            'overall_percentage': overall_percentage,
            'proficiency_level': proficiency_level,
            'level_breakdown': level_scores,
            'weighted_score': self._calculate_weighted_score(level_scores)
        }
    
    def _general_assessment(self, language: str) -> Dict:
        """General assessment for languages not in quiz database"""
        # Simulate assessment based on common programming concepts
        simulated_score = random.uniform(40, 85)
        proficiency_level = self._determine_proficiency_level(simulated_score)
        
        return {
            'overall_score': int(simulated_score * 0.1),  # Out of 10
            'total_questions': 10,
            'overall_percentage': simulated_score,
            'proficiency_level': proficiency_level,
            'level_breakdown': {
                'note': f'General assessment for {language} - detailed quiz not available'
            },
            'weighted_score': simulated_score / 100
        }
    
    def _determine_proficiency_level(self, percentage: float) -> str:
        """Determine proficiency level based on percentage score"""
        if percentage >= 76:
            return 'advanced'
        elif percentage >= 41:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _calculate_weighted_score(self, level_scores: Dict) -> float:
        """Calculate weighted score giving more weight to higher levels"""
        weighted_sum = 0
        total_weight = 0
        
        for level, scores in level_scores.items():
            if level in self.proficiency_levels:
                weight = self.proficiency_levels[level]['weight']
                contribution = (scores['percentage'] / 100) * weight
                weighted_sum += contribution
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0
    
    def generate_skill_report(self, assessment_results: Dict) -> Dict:
        """Generate comprehensive skill assessment report"""
        report = {
            'total_languages_assessed': len(assessment_results),
            'language_proficiencies': {},
            'overall_technical_score': 0,
            'strengths': [],
            'improvement_areas': [],
            'recommended_focus': []
        }
        
        total_weighted_score = 0
        language_count = 0
        
        for language, results in assessment_results.items():
            proficiency = results['proficiency_level']
            score = results['overall_percentage']
            
            report['language_proficiencies'][language] = {
                'proficiency_level': proficiency,
                'score_percentage': score,
                'weighted_score': results.get('weighted_score', score/100)
            }
            
            # Categorize as strength or improvement area
            if score >= 70:
                report['strengths'].append(f"{language} ({proficiency})")
            elif score < 50:
                report['improvement_areas'].append(f"{language} (needs focus)")
            
            total_weighted_score += results.get('weighted_score', score/100)
            language_count += 1
        
        # Calculate overall technical score
        if language_count > 0:
            report['overall_technical_score'] = (total_weighted_score / language_count) * 100
        
        # Generate recommendations
        report['recommended_focus'] = self._generate_focus_recommendations(report)
        
        return report
    
    def _generate_focus_recommendations(self, report: Dict) -> List[str]:
        """Generate personalized focus recommendations"""
        recommendations = []
        
        # Analyze proficiency distribution
        beginner_count = sum(1 for lang_data in report['language_proficiencies'].values() 
                           if lang_data['proficiency_level'] == 'beginner')
        intermediate_count = sum(1 for lang_data in report['language_proficiencies'].values() 
                               if lang_data['proficiency_level'] == 'intermediate')
        advanced_count = sum(1 for lang_data in report['language_proficiencies'].values() 
                           if lang_data['proficiency_level'] == 'advanced')
        
        if beginner_count > intermediate_count + advanced_count:
            recommendations.append("Focus on mastering fundamentals in your strongest language")
            recommendations.append("Complete structured courses for basic programming concepts")
        
        if advanced_count == 0:
            recommendations.append("Aim to achieve advanced proficiency in at least one language")
            recommendations.append("Work on complex projects to deepen technical understanding")
        
        if len(report['improvement_areas']) > 2:
            recommendations.append("Consider focusing on fewer languages with deeper expertise")
        
        return recommendations

def test_skill_assessment():
    """Test the skill assessment system"""
    print("🧪 Skill Assessment System Test")
    print("=" * 40)
    
    engine = SkillAssessmentEngine()
    
    # Test with sample languages
    test_languages = ['Python', 'Java', 'JavaScript']
    
    # Conduct assessment
    results = engine.conduct_skill_assessment(test_languages, questions_per_level=2)
    
    # Generate report
    report = engine.generate_skill_report(results)
    
    print(f"\n📊 ASSESSMENT REPORT")
    print("=" * 40)
    print(f"Overall Technical Score: {report['overall_technical_score']:.1f}%")
    print(f"Languages Assessed: {report['total_languages_assessed']}")
    
    print(f"\n💪 Strengths:")
    for strength in report['strengths']:
        print(f"  - {strength}")
    
    print(f"\n📈 Improvement Areas:")
    for area in report['improvement_areas']:
        print(f"  - {area}")
    
    print(f"\n🎯 Recommendations:")
    for rec in report['recommended_focus']:
        print(f"  - {rec}")

if __name__ == "__main__":
    test_skill_assessment()