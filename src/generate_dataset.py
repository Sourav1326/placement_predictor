import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_placement_dataset(n_samples=500):
    """
    Generate a realistic synthetic placement dataset for college students
    """
    
    # Define possible values for categorical variables
    branches = ['Computer Science', 'Information Technology', 'Electronics', 
               'Mechanical', 'Civil', 'Electrical', 'Chemical']
    
    programming_languages = [
        'Python, Java, C++', 'Java, JavaScript, Python', 'C++, C, Python',
        'JavaScript, React, Node.js', 'Python, SQL, R', 'Java, Spring, MySQL',
        'C++, DSA, Python', 'Python, Django, PostgreSQL', 'JavaScript, Angular, MongoDB',
        'Python, Machine Learning, TensorFlow', 'Java, Microservices, Docker',
        'C#, .NET, SQL Server', 'Python, Flask, SQLite', 'Go, Kubernetes, Docker'
    ]
    
    # Initialize lists to store generated data
    data = []
    
    for i in range(n_samples):
        # Basic Information
        student_id = f"STU{2024}{str(i+1).zfill(3)}"
        branch = random.choice(branches)
        
        # Academic Performance (correlated with placement chances)
        # Generate CGPA with some correlation to other factors
        base_cgpa = np.random.normal(7.5, 1.2)
        cgpa = max(5.0, min(10.0, base_cgpa))
        
        # 10th and 12th marks (somewhat correlated with CGPA)
        tenth_percentage = max(60, min(98, cgpa * 8.5 + np.random.normal(0, 8)))
        twelfth_percentage = max(60, min(98, cgpa * 8.2 + np.random.normal(0, 7)))
        
        # Technical Skills
        num_projects = max(0, int(np.random.poisson(2.5) + (cgpa - 7) * 0.5))
        num_internships = max(0, int(np.random.poisson(1.2) + (cgpa - 7) * 0.3))
        num_certifications = max(0, int(np.random.poisson(1.8) + (cgpa - 7) * 0.4))
        
        # Coding Platform Scores (correlated with technical skills)
        leetcode_score = max(0, min(5000, np.random.normal(1200, 800) + num_projects * 100))
        codechef_rating = max(1000, min(3000, np.random.normal(1400, 400) + num_projects * 50))
        
        # Soft Skills (1-10 scale)
        communication_score = max(1, min(10, np.random.normal(6.5, 1.8)))
        leadership_score = max(1, min(10, np.random.normal(5.8, 2.0)))
        
        # Extracurricular Activities
        num_hackathons = max(0, int(np.random.poisson(1.5) + (cgpa - 7) * 0.2))
        club_participation = random.choice([0, 1, 1, 1, 2, 2, 3])  # Number of clubs
        online_courses = max(0, int(np.random.poisson(2.0) + (cgpa - 7) * 0.3))
        
        # Technical Skills Selection
        programming_langs = random.choice(programming_languages)
        
        # Calculate placement probability based on multiple factors
        # This creates a realistic correlation between features and placement
        placement_score = (
            cgpa * 0.25 +
            (tenth_percentage / 100) * 0.15 +
            (twelfth_percentage / 100) * 0.15 +
            min(num_projects, 5) * 0.12 +
            min(num_internships, 3) * 0.15 +
            (leetcode_score / 5000) * 0.08 +
            (codechef_rating / 3000) * 0.05 +
            (communication_score / 10) * 0.10 +
            (leadership_score / 10) * 0.08 +
            min(num_hackathons, 5) * 0.05 +
            min(club_participation, 3) * 0.03 +
            min(num_certifications, 5) * 0.04 +
            random.uniform(-0.1, 0.1)  # Add some randomness
        )
        
        # Convert to probability and determine placement
        placement_probability = min(0.95, max(0.05, placement_score / 10))
        placed = 1 if random.random() < placement_probability else 0
        
        # Generate salary package for placed students
        if placed:
            # Salary correlated with skills and performance
            base_salary = 4.5 + (cgpa - 6) * 1.2 + num_projects * 0.3 + num_internships * 0.5
            salary_package = max(3.5, min(25.0, base_salary + np.random.normal(0, 1.5)))
            
            # Categorize salary
            if salary_package <= 6:
                package_category = 'Low'
            elif salary_package <= 12:
                package_category = 'Medium'
            else:
                package_category = 'High'
        else:
            salary_package = 0
            package_category = 'Not Placed'
        
        # Create student record
        student_data = {
            'student_id': student_id,
            'branch': branch,
            'cgpa': round(cgpa, 2),
            'tenth_percentage': round(tenth_percentage, 1),
            'twelfth_percentage': round(twelfth_percentage, 1),
            'num_projects': num_projects,
            'num_internships': num_internships,
            'num_certifications': num_certifications,
            'programming_languages': programming_langs,
            'leetcode_score': int(leetcode_score),
            'codechef_rating': int(codechef_rating),
            'communication_score': round(communication_score, 1),
            'leadership_score': round(leadership_score, 1),
            'num_hackathons': num_hackathons,
            'club_participation': club_participation,
            'online_courses': online_courses,
            'placed': placed,
            'salary_package': round(salary_package, 1),
            'package_category': package_category
        }
        
        data.append(student_data)
    
    return pd.DataFrame(data)

def main():
    """Generate and save the placement dataset"""
    print("Generating placement prediction dataset...")
    
    # Generate dataset
    df = generate_placement_dataset(n_samples=500)
    
    # Save to CSV
    df.to_csv('data/placement_data.csv', index=False)
    
    # Print dataset statistics
    print(f"\nDataset Generated Successfully!")
    print(f"Total Students: {len(df)}")
    print(f"Placed Students: {df['placed'].sum()} ({df['placed'].mean():.1%})")
    print(f"Average CGPA: {df['cgpa'].mean():.2f}")
    print(f"Branches: {df['branch'].nunique()}")
    
    print(f"\nPlacement Rate by Branch:")
    placement_by_branch = df.groupby('branch')['placed'].agg(['count', 'sum', 'mean']).round(3)
    placement_by_branch.columns = ['Total Students', 'Placed', 'Placement Rate']
    print(placement_by_branch)
    
    print(f"\nSalary Package Distribution:")
    print(df['package_category'].value_counts())
    
    print(f"\nDataset saved to: data/placement_data.csv")

if __name__ == "__main__":
    main()