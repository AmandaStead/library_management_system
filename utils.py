import random


def generate_book():
    adjectives = ['The Secret', 'Hidden', 'Forgotten', 'Lost', 'Mysterious', 'Magical', 'Enchanted']
    nouns = ['Book', 'Tome', 'Scroll', 'Codex', 'Manuscript', 'Chronicle', 'Volume']
    themes = ['Adventure', 'Mystery', 'Fantasy', 'Romance', 'Science Fiction', 'Thriller', 'Historical']
    book_name = f"{random.choice(adjectives)} {random.choice(nouns)} of {random.choice(themes)}"
    return {"name": book_name}
