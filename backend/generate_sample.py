"""
Sample dataset generator — creates a demo employee CSV for testing.
"""

import csv
import random
import os

NAMES = [
    "Aarav Sharma", "Priya Patel", "Rahul Singh", "Sneha Das", "Vikram Reddy",
    "Ananya Gupta", "Arjun Kumar", "Diya Nair", "Kabir Joshi", "Meera Iyer",
    "Nabil Rahman", "Fatima Begum", "Omar Hassan", "Sara Ahmed", "Tariq Ali",
    "John Smith", "Emily Johnson", "Michael Brown", "Jessica Davis", "David Wilson",
    "Lisa Anderson", "James Taylor", "Jennifer Martinez", "Robert Garcia", "Maria Lopez",
    "Wei Zhang", "Yuki Tanaka", "Chen Wei", "Akiko Suzuki", "Hiroshi Yamamoto",
    "Sophie Martin", "Lucas Dubois", "Emma Bernard", "Hugo Petit", "Chloe Moreau",
    "Liam O'Brien", "Olivia Murphy", "Noah Kelly", "Ava Walsh", "Ethan Byrne",
    "Aisha Mohammed", "Ibrahim Khan", "Zainab Abbas", "Hassan Malik", "Maryam Hussain",
    "Carlos Rivera", "Ana Fernandez", "Miguel Torres", "Isabella Rojas", "Diego Mendez"
]

DEPARTMENTS = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Product", "Operations", "Design", "Data Science", "Support"]
POSITIONS = ["Junior", "Mid-Level", "Senior", "Lead", "Manager", "Director"]


def generate_sample_csv(filepath: str, num_employees: int = 50):
    """Generate a sample employee dataset CSV."""

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Employee_Name", "Department", "Position",
            "Years_Experience", "Projects_Completed", "Training_Hours",
            "Manager_Rating", "Peer_Rating", "Self_Rating",
            "Goals_Met_Percent", "Certifications", "Leadership_Score",
            "Innovation_Score", "Communication_Score", "Adaptability_Score"
        ])

        for i in range(num_employees):
            name = NAMES[i % len(NAMES)]
            dept = random.choice(DEPARTMENTS)
            position = random.choice(POSITIONS)
            years_exp = random.randint(1, 20)
            projects = random.randint(2, 50)
            training = random.randint(10, 200)
            mgr_rating = round(random.uniform(1, 10), 1)
            peer_rating = round(random.uniform(1, 10), 1)
            self_rating = round(random.uniform(3, 10), 1)
            goals_met = random.randint(30, 100)
            certs = random.randint(0, 8)
            leadership = round(random.uniform(1, 10), 1)
            innovation = round(random.uniform(1, 10), 1)
            communication = round(random.uniform(1, 10), 1)
            adaptability = round(random.uniform(1, 10), 1)

            writer.writerow([
                name, dept, position,
                years_exp, projects, training,
                mgr_rating, peer_rating, self_rating,
                goals_met, certs, leadership,
                innovation, communication, adaptability
            ])

    print(f"Generated sample dataset: {filepath} with {num_employees} employees.")


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "sample_employees.csv")
    generate_sample_csv(output_path)
