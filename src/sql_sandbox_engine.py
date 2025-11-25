"""
🗃️ SQL SANDBOX ENGINE
Interactive SQL query execution and verification system
"""

import sqlite3
import tempfile
import os
import json
import hashlib
import time
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import pandas as pd

class SQLSandboxEngine:
    """
    Secure SQL execution environment for database skill verification
    """
    
    def __init__(self):
        self.database_schemas = self._load_database_schemas()
        self.query_timeout = 10  # seconds
        self.max_result_rows = 1000
        
        # SQL injection prevention patterns
        self.dangerous_patterns = [
            r'\b(drop|delete|truncate|alter|create|insert|update)\s+(table|database|schema)',
            r';\s*(drop|delete|truncate)',
            r'--.*',  # SQL comments that might hide malicious code
            r'/\*.*\*/',  # Multi-line comments
            r'\bexec\b',
            r'\bexecute\b',
            r'\bsp_\w+',  # Stored procedures
            r'\bxp_\w+',  # Extended procedures
        ]
    
    def create_test_database(self, schema_name: str) -> str:
        """
        Create a temporary database with test data
        """
        schema = self.database_schemas.get(schema_name)
        if not schema:
            raise ValueError(f"Schema '{schema_name}' not found")
        
        # Create temporary database file
        db_fd, db_path = tempfile.mkstemp(suffix='.db')
        os.close(db_fd)
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Create tables
                for table_name, table_info in schema['tables'].items():
                    create_sql = self._build_create_table_sql(table_name, table_info)
                    cursor.execute(create_sql)
                    
                    # Insert sample data
                    if 'data' in table_info:
                        self._insert_sample_data(cursor, table_name, table_info['data'])
                
                conn.commit()
                
        except Exception as e:
            os.unlink(db_path)
            raise Exception(f"Failed to create test database: {str(e)}")
        
        return db_path
    
    def execute_sql_query(self, query: str, database_path: str) -> Dict[str, Any]:
        """
        Execute SQL query safely and return results
        """
        start_time = time.time()
        
        # Security validation
        security_check = self._validate_sql_security(query)
        if not security_check['safe']:
            return {
                'success': False,
                'error': f"Security violation: {security_check['reason']}",
                'execution_time': 0
            }
        
        try:
            with sqlite3.connect(database_path) as conn:
                conn.row_factory = sqlite3.Row  # Enable column access by name
                cursor = conn.cursor()
                
                # Set query timeout (SQLite doesn't support timeout directly)
                # We'll implement this with threading if needed
                
                cursor.execute(query)
                
                # Fetch results
                if query.strip().upper().startswith('SELECT'):
                    rows = cursor.fetchmany(self.max_result_rows)
                    columns = [description[0] for description in cursor.description]
                    
                    # Convert to list of dictionaries
                    results = []
                    for row in rows:
                        results.append({col: row[col] for col in columns})
                    
                    execution_time = time.time() - start_time
                    
                    return {
                        'success': True,
                        'results': results,
                        'columns': columns,
                        'row_count': len(results),
                        'execution_time': execution_time,
                        'query_type': 'SELECT'
                    }
                else:
                    # For non-SELECT queries (though we generally don't allow them in verification)
                    rows_affected = cursor.rowcount
                    execution_time = time.time() - start_time
                    
                    return {
                        'success': True,
                        'rows_affected': rows_affected,
                        'execution_time': execution_time,
                        'query_type': 'MODIFICATION'
                    }
                    
        except sqlite3.Error as e:
            return {
                'success': False,
                'error': f"SQL Error: {str(e)}",
                'execution_time': time.time() - start_time
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Execution Error: {str(e)}",
                'execution_time': time.time() - start_time
            }
    
    def verify_sql_challenge(self, user_query: str, expected_result: List[Dict], schema_name: str) -> Dict[str, Any]:
        """
        Verify SQL challenge by comparing user query results with expected results
        """
        # Create test database
        try:
            db_path = self.create_test_database(schema_name)
            
            # Execute user query
            user_result = self.execute_sql_query(user_query, db_path)
            
            if not user_result['success']:
                return {
                    'verification_passed': False,
                    'score': 0,
                    'feedback': [f"Query execution failed: {user_result['error']}"],
                    'user_result': user_result
                }
            
            # Compare results
            comparison = self._compare_query_results(
                user_result.get('results', []), 
                expected_result
            )
            
            # Calculate score
            score = self._calculate_sql_score(comparison, user_query)
            
            # Generate feedback
            feedback = self._generate_sql_feedback(comparison, user_result, user_query)
            
            return {
                'verification_passed': comparison['exact_match'] and score >= 70,
                'score': score,
                'comparison': comparison,
                'feedback': feedback,
                'user_result': user_result,
                'expected_result': expected_result,
                'query_analysis': self._analyze_sql_query(user_query)
            }
            
        except Exception as e:
            return {
                'verification_passed': False,
                'score': 0,
                'feedback': [f"Verification error: {str(e)}"],
                'error': str(e)
            }
        finally:
            # Clean up temporary database
            try:
                os.unlink(db_path)
            except:
                pass
    
    def get_sql_challenge(self, difficulty: str = 'medium', topic: str = 'general') -> Dict[str, Any]:
        """
        Get SQL challenge based on difficulty and topic
        """
        challenges = self._load_sql_challenges()
        
        challenge_key = f"{difficulty}_{topic}"
        challenge = challenges.get(challenge_key, challenges.get(f"medium_general"))
        
        if not challenge:
            raise ValueError(f"No challenge found for {difficulty} {topic}")
        
        return {
            'challenge_id': hashlib.md5(f"{difficulty}_{topic}_{time.time()}".encode()).hexdigest()[:12],
            'title': challenge['title'],
            'description': challenge['description'],
            'schema_name': challenge['schema_name'],
            'schema_info': self.database_schemas[challenge['schema_name']],
            'expected_result': challenge['expected_result'],
            'difficulty': difficulty,
            'topic': topic,
            'time_limit': challenge.get('time_limit', 8),
            'hints': challenge.get('hints', []),
            'starter_query': challenge.get('starter_query', '-- Write your SQL query here\nSELECT ')
        }
    
    def _validate_sql_security(self, query: str) -> Dict[str, Any]:
        """
        Validate SQL query for security issues
        """
        query_lower = query.lower().strip()
        
        # Only allow SELECT statements for verification
        if not query_lower.startswith('select'):
            return {
                'safe': False,
                'reason': 'Only SELECT queries are allowed for verification'
            }
        
        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                return {
                    'safe': False,
                    'reason': f'Potentially dangerous SQL pattern detected'
                }
        
        # Check query length (prevent extremely complex queries)
        if len(query) > 2000:
            return {
                'safe': False,
                'reason': 'Query too long'
            }
        
        # Check for excessive subqueries
        if query_lower.count('select') > 5:
            return {
                'safe': False,
                'reason': 'Too many subqueries'
            }
        
        return {'safe': True, 'reason': 'Query passed security validation'}
    
    def _compare_query_results(self, user_results: List[Dict], expected_results: List[Dict]) -> Dict[str, Any]:
        """
        Compare user query results with expected results
        """
        # Convert to pandas DataFrames for easier comparison
        try:
            user_df = pd.DataFrame(user_results) if user_results else pd.DataFrame()
            expected_df = pd.DataFrame(expected_results) if expected_results else pd.DataFrame()
            
            # Check if DataFrames are equal
            if user_df.empty and expected_df.empty:
                exact_match = True
            elif user_df.empty or expected_df.empty:
                exact_match = False
            else:
                # Sort both DataFrames to handle order differences
                if not user_df.empty and not expected_df.empty:
                    try:
                        user_sorted = user_df.sort_values(by=user_df.columns.tolist()).reset_index(drop=True)
                        expected_sorted = expected_df.sort_values(by=expected_df.columns.tolist()).reset_index(drop=True)
                        exact_match = user_sorted.equals(expected_sorted)
                    except:
                        # If sorting fails, compare without sorting
                        exact_match = user_df.equals(expected_df)
                else:
                    exact_match = False
            
            # Calculate similarity metrics
            row_count_match = len(user_results) == len(expected_results)
            
            column_match = True
            if user_results and expected_results:
                user_columns = set(user_results[0].keys()) if user_results else set()
                expected_columns = set(expected_results[0].keys()) if expected_results else set()
                column_match = user_columns == expected_columns
            
            # Content similarity (approximate)
            content_similarity = 0.0
            if exact_match:
                content_similarity = 1.0
            elif row_count_match and column_match and user_results and expected_results:
                # Calculate approximate similarity
                matching_rows = 0
                for user_row in user_results:
                    if user_row in expected_results:
                        matching_rows += 1
                content_similarity = matching_rows / len(expected_results)
            
            return {
                'exact_match': exact_match,
                'row_count_match': row_count_match,
                'column_match': column_match,
                'content_similarity': content_similarity,
                'user_row_count': len(user_results),
                'expected_row_count': len(expected_results),
                'user_columns': list(user_results[0].keys()) if user_results else [],
                'expected_columns': list(expected_results[0].keys()) if expected_results else []
            }
            
        except Exception as e:
            return {
                'exact_match': False,
                'error': f"Comparison error: {str(e)}",
                'content_similarity': 0.0
            }
    
    def _calculate_sql_score(self, comparison: Dict, user_query: str) -> float:
        """
        Calculate score based on query results and quality
        """
        base_score = 0
        
        # Result accuracy (70% of score)
        if comparison['exact_match']:
            base_score += 70
        else:
            # Partial credit
            if comparison['row_count_match']:
                base_score += 20
            if comparison['column_match']:
                base_score += 20
            base_score += comparison.get('content_similarity', 0) * 30
        
        # Query quality (30% of score)
        quality_score = self._assess_query_quality(user_query)
        base_score += quality_score * 0.3
        
        return min(100, base_score)
    
    def _assess_query_quality(self, query: str) -> float:
        """
        Assess SQL query quality
        """
        quality_score = 100
        query_lower = query.lower()
        
        # Check for good practices
        if 'where' in query_lower:
            quality_score += 10  # Uses filtering
        
        if 'join' in query_lower:
            quality_score += 15  # Uses joins appropriately
        
        if 'group by' in query_lower:
            quality_score += 10  # Uses aggregation
        
        if 'order by' in query_lower:
            quality_score += 5  # Uses sorting
        
        # Check for inefficient patterns
        if 'select *' in query_lower:
            quality_score -= 10  # Avoid SELECT *
        
        # Check query length and complexity
        if len(query) < 20:
            quality_score -= 20  # Too simple
        elif len(query) > 500:
            quality_score -= 10  # Overly complex
        
        return max(0, min(100, quality_score))
    
    def _generate_sql_feedback(self, comparison: Dict, user_result: Dict, user_query: str) -> List[str]:
        """
        Generate helpful feedback for SQL queries
        """
        feedback = []
        
        if comparison['exact_match']:
            feedback.append("🎉 Perfect! Your query returned the correct results.")
        else:
            if not comparison['row_count_match']:
                feedback.append(f"❌ Row count mismatch: You returned {comparison['user_row_count']} rows, expected {comparison['expected_row_count']}")
            
            if not comparison['column_match']:
                feedback.append(f"❌ Column mismatch: You returned {comparison['user_columns']}, expected {comparison['expected_columns']}")
            
            if comparison.get('content_similarity', 0) > 0.5:
                feedback.append("⚠️ Your results are partially correct but not exactly matching")
        
        # Query quality feedback
        query_lower = user_query.lower()
        
        if 'select *' in query_lower:
            feedback.append("💡 Tip: Avoid 'SELECT *' - specify only the columns you need")
        
        if 'where' not in query_lower and 'join' in query_lower:
            feedback.append("💡 Consider adding WHERE clauses to filter results more precisely")
        
        if user_result.get('execution_time', 0) > 2:
            feedback.append("⏱️ Your query took a while to execute - consider optimizing it")
        
        return feedback
    
    def _analyze_sql_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze SQL query structure and complexity
        """
        query_lower = query.lower()
        
        analysis = {
            'query_length': len(query),
            'uses_joins': 'join' in query_lower,
            'uses_aggregation': any(func in query_lower for func in ['count(', 'sum(', 'avg(', 'max(', 'min(']),
            'uses_grouping': 'group by' in query_lower,
            'uses_filtering': 'where' in query_lower,
            'uses_ordering': 'order by' in query_lower,
            'uses_subqueries': query_lower.count('select') > 1,
            'complexity_level': 'basic'
        }
        
        # Determine complexity level
        complexity_score = 0
        if analysis['uses_joins']:
            complexity_score += 2
        if analysis['uses_aggregation']:
            complexity_score += 2
        if analysis['uses_grouping']:
            complexity_score += 2
        if analysis['uses_subqueries']:
            complexity_score += 3
        
        if complexity_score <= 2:
            analysis['complexity_level'] = 'basic'
        elif complexity_score <= 5:
            analysis['complexity_level'] = 'intermediate'
        else:
            analysis['complexity_level'] = 'advanced'
        
        return analysis
    
    def _build_create_table_sql(self, table_name: str, table_info: Dict) -> str:
        """
        Build CREATE TABLE SQL statement
        """
        columns = table_info['columns']
        column_definitions = []
        
        for col_name, col_type in columns.items():
            column_definitions.append(f"{col_name} {col_type}")
        
        sql = f"CREATE TABLE {table_name} ({', '.join(column_definitions)})"
        return sql
    
    def _insert_sample_data(self, cursor, table_name: str, data: List[Dict]):
        """
        Insert sample data into table
        """
        if not data:
            return
        
        columns = list(data[0].keys())
        placeholders = ', '.join(['?' for _ in columns])
        
        insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        
        for row in data:
            values = [row[col] for col in columns]
            cursor.execute(insert_sql, values)
    
    def _load_database_schemas(self) -> Dict[str, Dict]:
        """
        Load database schemas for different challenge scenarios
        """
        return {
            'student_courses': {
                'description': 'University student and course management system',
                'tables': {
                    'students': {
                        'columns': {
                            'id': 'INTEGER PRIMARY KEY',
                            'name': 'TEXT NOT NULL',
                            'email': 'TEXT UNIQUE',
                            'age': 'INTEGER',
                            'major': 'TEXT'
                        },
                        'data': [
                            {'id': 1, 'name': 'John Doe', 'email': 'john@university.edu', 'age': 20, 'major': 'Computer Science'},
                            {'id': 2, 'name': 'Jane Smith', 'email': 'jane@university.edu', 'age': 21, 'major': 'Mathematics'},
                            {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@university.edu', 'age': 19, 'major': 'Computer Science'},
                            {'id': 4, 'name': 'Alice Brown', 'email': 'alice@university.edu', 'age': 22, 'major': 'Physics'},
                            {'id': 5, 'name': 'Charlie Wilson', 'email': 'charlie@university.edu', 'age': 20, 'major': 'Mathematics'}
                        ]
                    },
                    'courses': {
                        'columns': {
                            'id': 'INTEGER PRIMARY KEY',
                            'name': 'TEXT NOT NULL',
                            'credits': 'INTEGER',
                            'instructor': 'TEXT'
                        },
                        'data': [
                            {'id': 101, 'name': 'Data Structures', 'credits': 3, 'instructor': 'Dr. Smith'},
                            {'id': 102, 'name': 'Algorithms', 'credits': 4, 'instructor': 'Dr. Johnson'},
                            {'id': 103, 'name': 'Database Systems', 'credits': 3, 'instructor': 'Dr. Williams'},
                            {'id': 104, 'name': 'Calculus I', 'credits': 4, 'instructor': 'Dr. Davis'},
                            {'id': 105, 'name': 'Physics I', 'credits': 4, 'instructor': 'Dr. Miller'}
                        ]
                    },
                    'enrollments': {
                        'columns': {
                            'student_id': 'INTEGER',
                            'course_id': 'INTEGER',
                            'grade': 'TEXT',
                            'semester': 'TEXT',
                            'FOREIGN KEY (student_id)': 'REFERENCES students(id)',
                            'FOREIGN KEY (course_id)': 'REFERENCES courses(id)'
                        },
                        'data': [
                            {'student_id': 1, 'course_id': 101, 'grade': 'A', 'semester': 'Fall 2023'},
                            {'student_id': 1, 'course_id': 102, 'grade': 'B+', 'semester': 'Fall 2023'},
                            {'student_id': 2, 'course_id': 104, 'grade': 'A-', 'semester': 'Fall 2023'},
                            {'student_id': 3, 'course_id': 101, 'grade': 'B', 'semester': 'Fall 2023'},
                            {'student_id': 3, 'course_id': 103, 'grade': 'A', 'semester': 'Spring 2024'},
                            {'student_id': 4, 'course_id': 105, 'grade': 'A+', 'semester': 'Fall 2023'}
                        ]
                    }
                }
            },
            'company_employees': {
                'description': 'Company employee and department management',
                'tables': {
                    'employees': {
                        'columns': {
                            'id': 'INTEGER PRIMARY KEY',
                            'name': 'TEXT NOT NULL',
                            'department_id': 'INTEGER',
                            'salary': 'REAL',
                            'hire_date': 'TEXT'
                        },
                        'data': [
                            {'id': 1, 'name': 'John Manager', 'department_id': 1, 'salary': 75000, 'hire_date': '2020-01-15'},
                            {'id': 2, 'name': 'Jane Developer', 'department_id': 2, 'salary': 65000, 'hire_date': '2021-03-10'},
                            {'id': 3, 'name': 'Bob Analyst', 'department_id': 2, 'salary': 60000, 'hire_date': '2021-06-01'},
                            {'id': 4, 'name': 'Alice Designer', 'department_id': 3, 'salary': 58000, 'hire_date': '2022-02-14'}
                        ]
                    },
                    'departments': {
                        'columns': {
                            'id': 'INTEGER PRIMARY KEY',
                            'name': 'TEXT NOT NULL',
                            'manager_id': 'INTEGER'
                        },
                        'data': [
                            {'id': 1, 'name': 'Management', 'manager_id': 1},
                            {'id': 2, 'name': 'Engineering', 'manager_id': 2},
                            {'id': 3, 'name': 'Design', 'manager_id': 4}
                        ]
                    }
                }
            }
        }
    
    def _load_sql_challenges(self) -> Dict[str, Dict]:
        """
        Load SQL challenge database
        """
        return {
            'easy_general': {
                'title': 'Student Names in Course',
                'description': 'Write a query to find the names of all students enrolled in "Data Structures".',
                'schema_name': 'student_courses',
                'expected_result': [
                    {'name': 'John Doe'},
                    {'name': 'Bob Johnson'}
                ],
                'time_limit': 8,
                'hints': [
                    'You need to JOIN students and enrollments tables',
                    'Filter by course name using the courses table',
                    'Use WHERE clause to specify the course name'
                ],
                'starter_query': '-- Find student names enrolled in Data Structures\nSELECT s.name\nFROM students s\n-- Add your JOIN and WHERE clauses here'
            },
            'medium_general': {
                'title': 'Top Performing Students',
                'description': 'Find students with average grade points above 3.5 (A=4.0, A-=3.7, B+=3.3, B=3.0).',
                'schema_name': 'student_courses',
                'expected_result': [
                    {'name': 'John Doe', 'avg_gpa': 3.65},
                    {'name': 'Alice Brown', 'avg_gpa': 4.0}
                ],
                'time_limit': 12,
                'hints': [
                    'Use CASE statement to convert letter grades to numbers',
                    'Use GROUP BY to calculate averages per student',
                    'Use HAVING clause to filter by average'
                ]
            },
            'medium_joins': {
                'title': 'Department Employee Count',
                'description': 'Show each department name with the number of employees and average salary.',
                'schema_name': 'company_employees',
                'expected_result': [
                    {'department': 'Management', 'employee_count': 1, 'avg_salary': 75000.0},
                    {'department': 'Engineering', 'employee_count': 2, 'avg_salary': 62500.0},
                    {'department': 'Design', 'employee_count': 1, 'avg_salary': 58000.0}
                ],
                'time_limit': 10,
                'hints': [
                    'JOIN departments and employees tables',
                    'Use COUNT() and AVG() aggregate functions',
                    'GROUP BY department'
                ]
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize SQL sandbox
    sandbox = SQLSandboxEngine()
    
    # Test getting a challenge
    challenge = sandbox.get_sql_challenge(difficulty='easy', topic='general')
    print("🗃️ SQL Challenge:")
    print(f"Title: {challenge['title']}")
    print(f"Description: {challenge['description']}")
    print(f"Schema: {challenge['schema_name']}")
    
    # Test SQL execution
    test_query = """
    SELECT s.name
    FROM students s
    JOIN enrollments e ON s.id = e.student_id
    JOIN courses c ON e.course_id = c.id
    WHERE c.name = 'Data Structures'
    """
    
    print(f"\n🧪 Testing Query:")
    print(test_query)
    
    verification_result = sandbox.verify_sql_challenge(
        test_query, 
        challenge['expected_result'],
        challenge['schema_name']
    )
    
    print(f"\n✅ Verification Result:")
    print(f"Passed: {verification_result['verification_passed']}")
    print(f"Score: {verification_result['score']:.1f}%")
    print(f"Feedback: {verification_result['feedback']}")
    
    print("\n🎯 SQL Sandbox Engine ready for integration!")