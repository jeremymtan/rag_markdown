# sample questions with ground truth answers for ragas evaluation
test_questions_with_ground_truth = [
    {
        "question": "What is the minimum vacation policy?",
        "ground_truth": "Employees should take a minimum of two weeks of paid vacation per year, totaling 10 business days.",
        "source": "manual",
        "category": "benefits"
    },
    {
        "question": "How many weeks of parental leave are offered?",
        "ground_truth": "Employees are encouraged to take up to 16 weeks of maternity and paternity leave.",
        "source": "manual", 
        "category": "benefits"
    },
    {
        "question": "What are the prerequisites for using Kamal?",
        "ground_truth": "You need Docker installed on your servers and a Docker registry account for storing images.",
        "source": "docs",
        "category": "technical"
    },
    {
        "question": "What is Basecamp's sabbatical policy?",
        "ground_truth": "Every three years, employees are eligible to take a one-month-long paid sabbatical.",
        "source": "handbook",
        "category": "benefits"
    },
    {
        "question": "Can employees work remotely?",
        "ground_truth": "Yes, employees can work from anywhere. The company is fully distributed with team members working from all over the world.",
        "source": "handbook",
        "category": "work_arrangement"
    },
    {
        "question": "How do you deploy with Kamal?",
        "ground_truth": "Run 'kamal setup' for first deployment, then use 'kamal deploy' for subsequent deployments.",
        "source": "docs",
        "category": "technical"
    },
    {
        "question": "What equipment does Basecamp provide to employees?",
        "ground_truth": "Basecamp provides necessary work equipment including computers and will help with home office setup.",
        "source": "handbook",
        "category": "resources"
    },
    {
        "question": "What is the sick leave policy?",
        "ground_truth": "Employees receive sick leave as needed. There is no specific limit on sick days.",
        "source": "manual",
        "category": "benefits"
    },
    {
        "question": "How does Kamal handle environment variables?",
        "ground_truth": "Environment variables are configured in the .env file and secrets in .kamal/secrets file.",
        "source": "docs",
        "category": "technical"
    },
    {
        "question": "What are Basecamp's core values?",
        "ground_truth": "Basecamp values include being independent, profitable, and sustainable while treating employees and customers well.",
        "source": "handbook",
        "category": "culture"
    }
]