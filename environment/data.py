"""
Email dataset for the three tasks.
Each task has a set of emails with ground-truth labels.
"""

TASK_1_EMAILS = [
    # EASY: Clear, obvious emails - priority and category are unambiguous
    {
        "email": {
            "id": "t1_001",
            "subject": "URGENT: Server down - production outage",
            "sender": "ops-alerts@company.com",
            "body": "Our main production server has gone down at 2:15 PM. All customer-facing services are offline. We need immediate action. Engineering team is on standby.",
            "received_at": "2024-03-15T14:15:00Z",
            "has_attachment": False,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "urgent",
            "category": "technical_support",
            "action": "escalate",
            "assign_to": "engineering",
        },
    },
    {
        "email": {
            "id": "t1_002",
            "subject": "Congratulations! You've won a $1000 gift card",
            "sender": "prizes@win-now-fast.net",
            "body": "Dear Customer, You have been selected as the lucky winner! Click here to claim your prize. Act now before it expires! Limited time offer!!!",
            "received_at": "2024-03-15T10:00:00Z",
            "has_attachment": False,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "spam",
            "category": "spam",
            "action": "delete",
            "assign_to": None,
        },
    },
    {
        "email": {
            "id": "t1_003",
            "subject": "Invoice #4521 - Payment Overdue",
            "sender": "billing@vendor.com",
            "body": "This is a reminder that Invoice #4521 for $2,340.00 is now 30 days overdue. Please arrange payment at your earliest convenience to avoid service interruption.",
            "received_at": "2024-03-15T09:30:00Z",
            "has_attachment": True,
            "thread_length": 3,
        },
        "ground_truth": {
            "priority": "high",
            "category": "billing",
            "action": "forward",
            "assign_to": "finance",
        },
    },
    {
        "email": {
            "id": "t1_004",
            "subject": "Question about your product catalog",
            "sender": "potential.customer@gmail.com",
            "body": "Hi, I'm interested in learning more about your enterprise plan. Could you send me pricing information and a product demo? We have about 50 users.",
            "received_at": "2024-03-15T11:00:00Z",
            "has_attachment": False,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "high",
            "category": "sales",
            "action": "forward",
            "assign_to": "sales",
        },
    },
    {
        "email": {
            "id": "t1_005",
            "subject": "Team lunch this Friday",
            "sender": "manager@company.com",
            "body": "Hey team! Just a reminder about our team lunch this Friday at 12:30 PM at The Italian Place. Please RSVP by Thursday so I can make the reservation. See you there!",
            "received_at": "2024-03-15T08:00:00Z",
            "has_attachment": False,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "low",
            "category": "internal",
            "action": "archive",
            "assign_to": None,
        },
    },
]

TASK_2_EMAILS = [
    # MEDIUM: Requires reading comprehension and nuanced judgment
    {
        "email": {
            "id": "t2_001",
            "subject": "Re: Re: Re: My account has been charged incorrectly",
            "sender": "angry.customer@gmail.com",
            "body": "This is my FOURTH email about this issue. I've been charged $89.99 THREE times for a service I cancelled in January. I have the cancellation confirmation number: CXL-2024-0112. If this is not resolved TODAY I will be disputing the charges with my bank and leaving a public review. I want a full refund and an explanation.",
            "received_at": "2024-03-15T14:00:00Z",
            "has_attachment": True,
            "thread_length": 4,
        },
        "ground_truth": {
            "priority": "urgent",
            "category": "customer_complaint",
            "action": "escalate",
            "assign_to": "billing",
        },
    },
    {
        "email": {
            "id": "t2_002",
            "subject": "API rate limit questions",
            "sender": "developer@startupxyz.io",
            "body": "Hi, we're integrating your API and hitting rate limits during peak hours. Our current plan allows 1000 req/min but we're seeing 429 errors at around 800 req/min. We've tried exponential backoff. Is this a known issue? Also, we're evaluating upgrading to the enterprise plan — can you share the rate limits for that tier?",
            "received_at": "2024-03-15T10:30:00Z",
            "has_attachment": False,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "high",
            "category": "technical_support",
            "action": "reply",
            "assign_to": "technical_support",
        },
    },
    {
        "email": {
            "id": "t2_003",
            "subject": "Contract renewal discussion",
            "sender": "procurement@bigcorp.com",
            "body": "Our annual contract comes up for renewal on April 30th. We'd like to discuss terms before then. We've been happy with the service but our budget for this year has been reduced by 15%. We'd like to explore options — either a reduced tier or a multi-year discount. Who should we speak with?",
            "received_at": "2024-03-15T09:00:00Z",
            "has_attachment": False,
            "thread_length": 2,
        },
        "ground_truth": {
            "priority": "high",
            "category": "sales",
            "action": "forward",
            "assign_to": "sales",
        },
    },
    {
        "email": {
            "id": "t2_004",
            "subject": "Data export request - GDPR Article 20",
            "sender": "user@personal-email.eu",
            "body": "Under GDPR Article 20 (Right to Data Portability), I am formally requesting a full export of all personal data your company holds about me. My account email is user@personal-email.eu, registered since 2021. Please provide this within 30 days as required by law. Please confirm receipt of this request.",
            "received_at": "2024-03-15T12:00:00Z",
            "has_attachment": False,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "high",
            "category": "legal",
            "action": "escalate",
            "assign_to": "legal",
        },
    },
    {
        "email": {
            "id": "t2_005",
            "subject": "Feedback on your product",
            "sender": "user123@email.com",
            "body": "I've been using your product for 6 months. Overall it's good but the mobile app crashes sometimes when I upload photos larger than 5MB. Happens on both iOS and Android. Not urgent but thought you should know. The desktop version works great though!",
            "received_at": "2024-03-15T15:00:00Z",
            "has_attachment": False,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "normal",
            "category": "technical_support",
            "action": "forward",
            "assign_to": "engineering",
        },
    },
]

TASK_3_EMAILS = [
    # HARD: Ambiguous, multi-issue, requires complex judgment
    {
        "email": {
            "id": "t3_001",
            "subject": "Regarding our partnership",
            "sender": "ceo@potential-partner.com",
            "body": "Hi, I'm reaching out because I believe there's a strong strategic alignment between our companies. We're a Series B startup (raised $12M) in the workflow automation space. We'd love to explore a formal partnership or potential integration. I've attached our deck. I'll also mention — we've had some interest from your competitor, so timing matters. Looking forward to connecting.",
            "received_at": "2024-03-15T08:30:00Z",
            "has_attachment": True,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "high",
            "category": "sales",
            "action": "forward",
            "assign_to": "business_development",
        },
    },
    {
        "email": {
            "id": "t3_002",
            "subject": "Re: Your service caused us significant losses",
            "sender": "legal@enterprise-client.com",
            "body": "Following our call on March 10th, we are formally notifying you that the service outage on February 28th (lasting 4.5 hours) resulted in direct losses of approximately $340,000 for our operations. Per Section 8.3 of our SLA, we believe we are entitled to compensation. We have engaged outside counsel and will be sending a formal demand letter within 5 business days unless we receive a response from your legal team. Please acknowledge receipt of this email.",
            "received_at": "2024-03-15T09:00:00Z",
            "has_attachment": True,
            "thread_length": 5,
        },
        "ground_truth": {
            "priority": "urgent",
            "category": "legal",
            "action": "escalate",
            "assign_to": "legal",
        },
    },
    {
        "email": {
            "id": "t3_003",
            "subject": "Security concern with your platform",
            "sender": "security-researcher@independent.io",
            "body": "I'm an independent security researcher. I believe I've found a potential vulnerability in your authentication system that could allow unauthorized access to user accounts. I've followed responsible disclosure practices and have NOT published this. I'm giving you 90 days to patch before disclosure. I can share technical details securely. What's your responsible disclosure process? I'm also wondering if you have a bug bounty program.",
            "received_at": "2024-03-15T11:30:00Z",
            "has_attachment": False,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "urgent",
            "category": "technical_support",
            "action": "escalate",
            "assign_to": "security",
        },
    },
    {
        "email": {
            "id": "t3_004",
            "subject": "confused about my bill",
            "sender": "elderly.customer@aol.com",
            "body": "hello i got a bill for 149 dollars but i thought my plan was 49 dollars a month. my name is margaret. i have been a customer for 8 years. my son helps me sometimes but he is away. i dont understand why it went up. i am on a fixed income. can someone call me please? my number is 555-0142. thank you",
            "received_at": "2024-03-15T14:30:00Z",
            "has_attachment": False,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "high",
            "category": "billing",
            "action": "reply",
            "assign_to": "billing",
        },
    },
    {
        "email": {
            "id": "t3_005",
            "subject": "Newsletter unsubscribe + account deletion + data question",
            "sender": "user@company.org",
            "body": "Three things: 1) Please unsubscribe me from your marketing newsletter immediately. 2) I'd like to delete my account but I first need to export my data (5 years of records). 3) After deletion, under what legal basis will you retain any of my data, and for how long? I'm based in the EU. I work in data privacy law so I want complete and accurate answers. Please don't send me a generic response.",
            "received_at": "2024-03-15T16:00:00Z",
            "has_attachment": False,
            "thread_length": 1,
        },
        "ground_truth": {
            "priority": "high",
            "category": "legal",
            "action": "escalate",
            "assign_to": "legal",
        },
    },
]

ALL_TASKS = {
    "task_1_easy": {
        "name": "Basic Email Triage",
        "description": "Triage a set of clearly categorized emails. Priority and category signals are unambiguous.",
        "difficulty": "easy",
        "emails": TASK_1_EMAILS,
        "passing_threshold": 0.7,
    },
    "task_2_medium": {
        "name": "Nuanced Email Routing",
        "description": "Handle emails that require reading comprehension, multi-issue detection, and nuanced routing decisions.",
        "difficulty": "medium",
        "emails": TASK_2_EMAILS,
        "passing_threshold": 0.6,
    },
    "task_3_hard": {
        "name": "Complex & Ambiguous Triage",
        "description": "Triage high-stakes, ambiguous, or multi-dimensional emails requiring expert judgment (legal, security, escalation paths).",
        "difficulty": "hard",
        "emails": TASK_3_EMAILS,
        "passing_threshold": 0.5,
    },
}
