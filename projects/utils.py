from datetime import date
from django.utils import timezone

def analyze_sentiment(text):
    text = text.lower()
    positive_words = ['good', 'great', 'excellent', 'done', 'perfect', 'happy', 'thanks', 'easy']
    negative_words = ['bad', 'slow', 'hard', 'difficult', 'blocker', 'issue', 'problem', 'delay', 'stuck']
    
    pos_count = sum(1 for word in positive_words if word in text)
    neg_count = sum(1 for word in negative_words if word in text)
    
    if neg_count > pos_count:
        return 'NEGATIVE'
    elif pos_count > neg_count:
        return 'POSITIVE'
    return 'NEUTRAL'

def get_ai_prioritization(tasks):
    today = date.today()
    prioritized_tasks = []
    
    for task in tasks:
        # Calculate urgency score
        days_left = (task.due_date - today).days
        urgency_score = 0
        
        # Priority mapping
        priority_map = {'CRITICAL': 100, 'HIGH': 50, 'MEDIUM': 20, 'LOW': 0}
        urgency_score += priority_map.get(task.priority, 0)
        
        # Deadline mapping
        if days_left < 0:
            urgency_score += 200 # Overdue
        elif days_left <= 2:
            urgency_score += 150 # Very urgent
        elif days_left <= 7:
            urgency_score += 50 # Coming up
            
        # Status filter
        if task.status != 'DONE':
            prioritized_tasks.append({
                'task': task,
                'score': urgency_score,
                'is_suggested_urgent': urgency_score >= 150
            })
            
    # Sort by score descending
    prioritized_tasks.sort(key=lambda x: x['score'], reverse=True)
    return prioritized_tasks
